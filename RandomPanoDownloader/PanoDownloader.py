import streetview
from cropper import fix_cropping
# panoids = streetview.panoids(lat=40.75388056, lon=-73.99697222)
# panoid = panoids[0]['panoid']

#panoid = '4F8SFVVtpaiILI36dPa0wQ' #Working small, old
#panoid = 'CAoSLEFGMVFpcFBJRlk2RVNsdVk3cjhKZ2lza0k4a0pGaHhRcHRTV0tNSFBoYnFl' #Not working new long
# panoid = 'AF1QipPjYNzZtVFpw3-s10tD6UNS1bJcxG2GM2VJK33M' # New long, transformed
# panoid = 'AF1QipOIL6HKNUUnQcf0ofxVfI2VqWGYLh7gUJRr3HWy'
# panoid = 'GudWKQqeYveN-0QkBkP03w'

def download_pano(panoid, filename):
    panorama = streetview.download_panorama_v3(panoid, zoom=3, disp=False, filename=filename, alternate=False)
    if panorama: # Worked downloading
        pass
    else:
        panorama = streetview.download_panorama_v3(panoid, zoom=3, disp=False, filename=filename, alternate=True)
        if not panorama:
            raise(ValueError('Could not fetch Panorama with the given ID'))
        fix_cropping(filename)
