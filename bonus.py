'''
Extras
'''
import matplotlib.pyplot as plt

def cost_function(data, theta):
    'Program that calculates algorithm precision. Less is better, 0 is best'
    mileage = data.mileage.normalized
    price = data.price.normalized
    estimate = data.price.e.estimate
    m = data.m
    est = [0] * m
    for i in range(m):
        est[i] = (estimate(mileage[i], theta) - price[i])**2
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

def show(data):
    'Executes cost_function and plot after successful model training'
    print('Training successful.\n',\
        '\nAlgorithm precision (less is better, 0 is best):\n',\
        '\n- with default thetas [0, 0]:',\
        f'\n\t{cost_function(data, [0, 0])}\n',\
        f'\n- with trained thetas {data.theta}:',\
        f'\n\t{cost_function(data, data.theta)}\n')

    plot(data.theta, data.mileage, data.price, data.m)
