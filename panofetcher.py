from RandomPanoDownloader.goodFetcher import getRandomPanorama
from RandomPanoDownloader.PanoDownloader import download_pano

panoid,lat,long,loc_name,countryname  = getRandomPanorama(urban=True,indoors=False, countryNumber = None)

print(panoid,lat,long,loc_name,countryname)
download_pano(panoid,'downloaded.png')
