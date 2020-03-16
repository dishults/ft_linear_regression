'''
Extras
'''
import matplotlib.pyplot as plt

from estimate import price_estimate

def cost_function(data, theta):
    'Program that calculates algorithm precision. Less is better, 0 is best'
    mileage = data.mileage.normalized
    price = data.price.normalized
    m = data.m
    est = [(price_estimate(mileage, theta) - price)**2 for mileage, price in zip(mileage, price)]
    cost = sum(est)/(2 * m)
    return cost

def plot(theta, mileage, price):
    'Plot data on the graph'
    plt.scatter(mileage.mileage, price.price, label='Original data')
    plt.xlabel('Mileage')
    plt.ylabel('Price')
    price.normalized = [price_estimate(n_mileage, theta) for n_mileage in mileage.normalized]
    price_est = [price.max_minus_min * n_price + price.average for n_price in price.normalized]
    plt.plot(mileage.mileage, price_est, color='r', label='Trained model')
    plt.legend()
    plt.show()

def show(data, theta):
    'Executes cost_function and plot after successful model training'
    print('Training successful.\n',\
        '\nAlgorithm precision (less is better, 0 is best):\n',\
        '\n- with default thetas [0, 0]:',\
        f'\n\t{cost_function(data, [0, 0])}\n',\
        f'\n- with trained thetas {theta}:',\
        f'\n\t{cost_function(data, theta)}\n')
    plot(theta, data.mileage, data.price)
