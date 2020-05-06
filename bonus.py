"""
Extras
"""

import matplotlib.pyplot as plt

from estimate import Price as p

def cost_function(mileage, price, m, theta=[0, 0]):
    """Calculate algorithm precision with given thetas.
    Less is better. However, 0 is not always best, you might have overfitting.
    """

    est = [(p.estimate(mileage, theta) - price)**2 for mileage, price in zip(mileage, price)]
    cost = sum(est)/(2 * m)
    return cost

def plot(mileage, price, theta):
    """Plot Original and Trained Model data on the graph."""

    plt.scatter(mileage.mileage, price.price, label='Original data')
    plt.xlabel('Mileage')
    plt.ylabel('Price')

    normalized_est = [p.estimate(n_mileage, theta) for n_mileage in mileage.normalized]
    price_est = [price.range_ * n_price + price.average for n_price in normalized_est]
    
    plt.plot(mileage.mileage, price_est, color='r', label='Trained model')
    plt.legend()
    plt.show()

def show(mileage, price, data):
    """Calculate cost and show plot after successful model training."""

    default_cost = cost_function(
            mileage.normalized, price.normalized, data.m)
    trained_cost = cost_function(
            mileage.normalized, price.normalized, data.m, data.theta)

    print('Training successful.\n'
          '\nAlgorithm precision (less is better, 0 is best):\n'
          '\n- with default thetas [0, 0]:'
          f'\n\t{default_cost}\n'
          f'\n- with trained thetas {data.theta}:'
          f'\n\t{trained_cost}\n')
    plot(mileage, price, data.theta)
