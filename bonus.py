'''
Extras
'''
import estimate as e

def cost_function(mileage, price, m, theta):
    'Program that calculates algorithm precision. Less is better, 0 is best'
    est = [0] * m
    for i in range(m):
        est[i] = (e.estimate_price(mileage[i], theta) - price[i])**2
    cost = sum(est)/(2 * m)
    return cost
