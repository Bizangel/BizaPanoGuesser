from random import choice
from json import loads as jsonifier
import requests

countriesid = {
    "1": "Canada",
    "2": "Cz Rep.",
    "3": "Denmark",
    "4": "Finland",
    "5": "France",
    "6": "H. Kong",
    "7": "Italy",
    "8": "Japan",
    "9": "Macau",
    "10": "Holland",
    "11": "Norway",
    "12": "NZ",
    "13": "Portugal",
    "14": "S. Africa",
    "15": "Singapore",
    "16": "Spain",
    "17": "Sweden",
    "18": "Switzerland",
    "19": "Taiwan",
    "20": "UK",
    "21": "USA",
    "22": "Australia",
    "23": "Brazil",
    "24": "Ireland",
    "25": "Antarctica",
    "26": "Mexico",
    "27": "Germany",
    "28": "Romania",
    "29": "Belgium",
    "30": "S. Korea",
    "31": "Russia",
    "32": "Poland",
    "33": "Thailand",
    "34": "Israel",
    "35": "Ukraine",
    "36": "Estonia",
    "37": "Latvia",
    "38": "Andorra",
    "39": "Chile",
    "40": "Croatia",
    "41": "Slovakia",
    "42": "Botswana",
    "43": "Lithuania",
    "44": "Bulgaria",
    "45": "Hungary",
    "46": "Lesotho",
    "47": "Peru",
    "48": "Colombia",
    "49": "Ecuador",
    "50": "Iceland",
    "51": "Swaziland",
    "52": "Islands",
    "53": "Slovenia",
    "54": "Greece",
    "55": "Serbia",
    "56": "Indonesia",
    "57": "Cambodia",
    "58": "Argentina",
    "59": "Malaysia",
    "60": "Bhutan",
    "61": "Luxembourg",
    "62": "UAE",
    "63": "Bangladesh",
    "64": "Greenland",
    "65": "Madagascar",
    "66": "Mongolia",
    "67": "Bermuda",
    "68": "Philippines",
    "69": "Macedonia",
    "70": "Uganda",
    "71": "Turkey",
    "72": "Bolivia",
    "73": "Uruguay",
    "74": "Sri Lanka",
    "75": "Kyrgyz",
    "76": "Laos",
    "77": "Albania",
    "78": "Montenegro",
    "79": "Ghana",
    "80": "Senegal",
    "81": "Tunisia",
    "82": "Malta",
    "83": "Guatemala"
}

def getRandomPanorama(urban=True,indoors=False, countryNumber = None):
    if countryNumber is None:
        countryNumber = choice(list(countriesid.keys()))

    if urban:
        d = '1'
    else:
        d = '0'
        
    if indoors:
        i = '1'
    else:
        i = '0'
    
    while True:
        r = requests.get('https://www.mapcrunch.com/_r/?c={}&d={}&i={}'.format(countryNumber,d,i))
        
        if r.status_code == 200:
            toparse = r.text
            toparse = toparse[9:]
            latitudes = jsonifier(toparse)
            
            for point in latitudes['points']:
            
                lat, long = point
                radius = 100
                fetchurl = 'https://maps.googleapis.com/maps/api/js/GeoPhotoService.SingleImageSearch?pb=!1m5!1sapiv3!5sUS!11m2!1m1!1b0!2m4!1m2!3d{0}!4d{1}!2d{2}!3m18!2m2!1sen!2sUS!9m1!1e2!11m12!1m3!1e2!2b1!3e2!1m3!1e3!2b1!3e2!1m3!1e10!2b1!3e2!4m6!1e1!1e2!1e3!1e4!1e8!1e6&callback=initialize'.format(lat,long,radius)
                
                
                res = requests.get(fetchurl)
                response = res.text[:-1]
                response = response[29:]
                
                jsonified = jsonifier(response)
                
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
                    
                    return panoid,lat,long,loc_name, countriesid[countryNumber]
                else:
                    continue
            
        else:
            continue





