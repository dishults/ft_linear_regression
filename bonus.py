'''
Extras
'''
import matplotlib.pyplot as plt

from estimate import Price

def cost_function(mileage, price, m, theta):
    'Program that calculates algorithm precision. Less is better, 0 is best'
    est = [0] * m
    for i in range(m):
        est[i] = (Price.estimate(Price, mileage[i], theta) - price[i])**2
    cost = sum(est)/(2 * m)
    return cost

def plot(theta, mileage, price, m):
    'Plot data on the graph'
    plt.scatter(mileage.mileage, price.price, label='Original data')
    plt.xlabel('Mileage')
    plt.ylabel('Price')
    price_est = [0] * m
    for i in range(m):
        price.e.normalized = price.e.estimate(mileage.normalized[i], theta)
        price_est[i] = int(price.max_minus_min * price.e.normalized + price.average)
    plt.plot(mileage.mileage, price_est, color='r', label='Trained model')
    plt.legend()
    plt.show()
