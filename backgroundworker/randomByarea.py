from RandomPanoDownloader.countryFilter import getRandomLatLing,getRandomCountryByAreaProbability
from RandomPanoDownloader.goodFetcher import countriesid

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
        
countriestoid = {
    'Albania': 77,
    'Argentina':58,
    'Australia':22,
    'Bermuda':67,
    'Bangladesh':63,
    'Bolivia':72,
    'Brazil':23,
    'Bulgaria': 44,
    'Canada':1,
    'Cambodia': 57,
    'Sri Lanka':74,
    'Bhutan':60,
    'Chile':39,
    'Colombia':48,
    'Denmark':3,
    'Ecuador':49,
    'Ireland':24,
    'Estonia':36,
    'Czech Republic': 2,
    'Finland':4,
    'France':5,
    'Ghana':79,
    'Greenland':64,
    'Germany':27,
    'Greece':54,
    'Guatemala':83,
    'Croatia':40,
    'Hungary':45,
    'Iceland':50,
    'Israel':34,
    'Italy':7,
    'Japan':8,
    'Kyrgyzstan':75,
    'Korea, Republic of': 30,
    'Lao People\'s Democratic Republic':76,
    'Latvia': 37,
    'Lithuania':43,
    'Slovakia':41,
    'Madagascar':65,
    'The former Yugoslav Republic of Macedonia': 69,
    'Mongolia':66,
    'Malta':82, 
    'Mexico':26,
    'Malaysia':59,
    'Belgium':29,
    'Hong Kong':6,
    'Andorra':38,
    'Luxembourg':61,
    'Macau':9,
    'Montenegro':78,
    'Antarctica':25,
    'Netherlands':10,
    'Norway':11,
    'New Zealand':12,
    'Peru':47,
    'Poland':32,
    'Portugal':13,
    'Romania':28,
    'Philippines':68,
    'Russia':31,
    'South Africa':14,
    'Lesotho':46,
    'Botswana':42,
    'Senegal':80,
    'Slovenia':53,
    'Singapore':15,
    'Spain':16,
    'Sweden':17,
    'Switzerland':18,
    'Thailand':33,
    'Tunisia':81,
    'Turkey':71,
    'Uganda':70,
    'United Kingdom':20,
    'Ukraine':35,
    'United States':21,
    'Uruguay':73,
    'Swaziland':51,
    'Indonesia':56,
    'United Arab Emirates':62,
    'Serbia':55,
    'Taiwan':19,

}

def getRandomValidCountryByArea():
    prevantarctica = 0
    preventNZ = 0
    preventRussia = False
    
    while True:
        x = getRandomCountryByAreaProbability()
        if x in countriestoid:
            if x == 'Antarctica':
                if prevantarctica > 2:
                    return countriestoid[x]
                else:
                    prevantarctica += 1
                    continue
                    
            if x == 'New Zealand':
                if preventNZ > 1:
                    return countriestoid[x]
                else:
                    preventNZ += 1
                    continue
                    
            if x == 'Russia':
                if preventRussia:
                    return countriestoid[x]
                else:
                    preventRussia = True
                    continue
                    
            return countriestoid[x]


# N = 100
# counter = 0
# dictcounter = {}

# printProgressBar(0, N, prefix = 'Progress:', suffix = 'Complete', length = 50)
# for i in range(N):
    # x = getRandomValidCountryByArea()
    # dictcounter[x] = dictcounter.get(x,0) + 1
    
    # printProgressBar(i, N, prefix = 'Progress:', suffix = 'Complete', length = 50)
        
# print(dictcounter)
# dictprob = { country : dictcounter[country]/N for country in dictcounter }

# for country in sorted(dictprob, key=dictprob.get, reverse=True):
    # print(country,'-->',dictprob[country])

# for name in sorted(countriestoid, key=countriestoid.get):
        # print(name, countriestoid[name])
        
# for name in countriestoid:
    # cid = str(countriestoid[name])
    # if name != countriesid[cid]:
        # print(name, '-->',countriesid[cid])

