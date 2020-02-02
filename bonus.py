'''
Extras
'''
import matplotlib.pyplot as plt

import estimate as e

def cost_function(mileage, price, m, theta):
    'Program that calculates algorithm precision. Less is better, 0 is best'
    est = [0] * m
    for i in range(m):
        est[i] = (e.estimate_price(mileage[i], theta) - price[i])**2
    cost = sum(est)/(2 * m)
    return cost

def plot(mileage, price, m):
    'Plot data on the graph'
    plt.scatter(mileage, price, label='Original data')
    plt.xlabel('Mileage')
    plt.ylabel('Price')
    price_est = [0] * m
    for i in range(m):
        price_est[i] = int(e.process(mileage[i]))
    plt.plot(mileage, price_est, color='r', label='Trained model')
    plt.legend()
    plt.show()
