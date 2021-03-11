import os
import random
import sys
import shapefile  # pip install pyshp
from pathlib import Path

def getRandomLatLing(country=None, disp=False):
    def point_inside_polygon(x, y, poly):
        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    if disp:
        print("Loading borders")
    shape_file = str(( (Path(__file__).parent / 'WorldBorders') / 'TM_WORLD_BORDERS-0.3.shp').absolute())
    if not os.path.exists(shape_file):
        print(
            "Cannot find " + shape_file + ". Please download it from "
            "http://thematicmapping.org/downloads/world_borders.php"
        )
        sys.exit()

    sf = shapefile.Reader(shape_file, encoding="latin1")
    shapes = sf.shapes()

    countryfound = False
    if disp:
        print("Finding country")
    for i, record in enumerate(sf.records()):
        if record[2] == country:
            if disp:
                print(record[2], record[4])
            # print(shapes[i].bbox)
            min_lon = shapes[i].bbox[0]
            min_lat = shapes[i].bbox[1]
            max_lon = shapes[i].bbox[2]
            max_lat = shapes[i].bbox[3]
            borders = shapes[i].points
            countryfound = True
            break
    
    if country is None:
        min_lat = -90
        max_lat = 90
        min_lon = -180
        max_lon = 180
        
    if not countryfound and country is not None:
        print("Invalid Country Code")
        sys.exit(0)

    if disp:
        print("Getting images")

    while True:
        rand_lat = random.uniform(min_lat, max_lat)
        rand_lon = random.uniform(min_lon, max_lon)
        # print attempts, rand_lat, rand_lon
        # Is (lat,lon) inside borders?
        if country is not None:
            if point_inside_polygon(rand_lon, rand_lat, borders):
                return (rand_lat, rand_lon)
                break
        else:
            for i, record in enumerate(sf.records()):
                if point_inside_polygon(rand_lon, rand_lat, shapes[i].points): 
                    return(rand_lat,rand_lon)
