from vincenty import vincenty as geodistance
boston = (42.3541165, -71.0693514)
newyork = (40.7791472, -73.9680804)
x = geodistance(boston, newyork)
