import requests,json,ast,shapefile
from RandomPanoDownloader.countryFilter import getRandomLatLing
from RandomPanoDownloader.PanoDownloader import download_pano
from random import choice as randomChoice

def getPanoFromCountryCode(countryCode=None,outdoors=False):
    failedtries = 0
    while True:
        lat, long = getRandomLatLing(countryCode)
        radius = 1000
        
        if failedtries > 100: #Extend radius
            radius = 10000
            
        fetchurl = 'https://maps.googleapis.com/maps/api/js/GeoPhotoService.SingleImageSearch?pb=!1m5!1sapiv3!5sUS!11m2!1m1!1b0!2m4!1m2!3d{0}!4d{1}!2d{2}!3m18!2m2!1sen!2sUS!9m1!1e2!11m12!1m3!1e2!2b1!3e2!1m3!1e3!2b1!3e2!1m3!1e10!2b1!3e2!4m6!1e1!1e2!1e3!1e4!1e8!1e6&callback=initialize'.format(lat,long,radius)
        
        if outdoors:
            fetchurl = 'https://maps.googleapis.com/maps/api/js/GeoPhotoService.SingleImageSearch?pb=!1m5!1sapiv3!5sUS!11m2!1m1!1b0!2m4!1m2!3d{0}!4d{1}!2d{2}!3m20!1m1!3b1!2m2!1sen!2sUS!9m1!1e2!11m12!1m3!1e2!2b1!3e2!1m3!1e3!2b1!3e2!1m3!1e10!2b1!3e2!4m6!1e1!1e2!1e3!1e4!1e8!1e6&callback=initialize'.format(lat,long,radius)
            res = requests.get(fetchurl) 
            
            # response = res.text[:-1]
            # response = response[29:]
        res = requests.get(fetchurl)
        response = res.text[:-1]
        response = response[29:]
        
        jsonified = json.loads(response)
        
        if len(jsonified) > 1:
            panoid = jsonified[1][1][1]
            
            metadata = None
            if len(jsonified[1][3]):
                metadata = jsonified[1][3][2] #No metadata attached
            
            coords = jsonified[1][5][0][1][0]
            lat, long = coords[2],coords[3]
            
            loc_name = None
            if metadata is not None:
                loc_name = metadata[-1][0]
            break
        else:
            failedtries += 1
            continue
    return panoid,lat,long,loc_name


    

# panoid,lat,long,loc_name = getPanoFromCountryCode(countryCode=None,outdoors=True) #Truly Fully random, no filters
# print(panoid,lat,long,loc_name)
# download_pano(panoid,'downloaded.png')







