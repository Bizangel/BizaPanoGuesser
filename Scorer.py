from math import exp
'''
The closest player gets the biggest score.
Score should be from 0 to 100 Every round.
Score should allow players to "catch up" even if they make big mistakes.
Score should be based on everyone's input.
If someone obtains a 0km distance and someone else obtains a 6000km then,
the farthest should be about 0 score and the closest should get 100.

So if everyone is close, then everyone should get a similar score
And not simply 0 the farthest and 100 the closest.
'''
SIGMOID_A = -0.001
SIGMOID_C = 3000


def scorequantifier(distances):  # dict that maps username -> distance
    # Adjusted Sigmoid function
    # Returns dict that maps username -> score
    newdict = {}
    for user in distances:
        x = distances[user]
        newdict[user] = round(100/(1+exp(-(x-SIGMOID_C)*SIGMOID_A)))

    return newdict

# MAX_SCORE_THRESHOLD = 100
# MIN_SCORE_THRESHOLD = 6000
#
# scoretest1 = [100, 150, 200, 350, 1000]
# scoretest2 = [50, 2000, 7000, 1000, 150]
# scoretest3 = [150, 150, 150, 150, 150]
# scoretest4 = [145, 150, 200, 180, 157]
#
# scoretest5 = [400, 500, 2000, 3000]

# x = scorequantifier(scoretest5)
# print(x)
