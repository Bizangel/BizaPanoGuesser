from RandomPanoDownloader.goodFetcher import getRandomPanorama
from RandomPanoDownloader.PanoDownloader import download_pano

panoid, lat, long, loc_name, cname = getRandomPanorama()
download_pano(panoid, 'compleja.png', zoom=3)