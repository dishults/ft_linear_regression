'''
linear regression with a single feature - the mileage of the car.
'''
import csv

def estimate_price(mileage, theta):
    "predict the price of a car for a given mileage"
    return theta[0] + (theta[1] * mileage)

#def cost_function(x, y, m, t):
#    est = [0] * m
#    for i in range(m):
#        est[i] = (estimate_price(x[i], t) - y[i])**2
#    cost = sum(est)/(2 * m)
#    return cost

def normalize_data(data, m):
    "to help gradient descent converge faster"
    d = [0] * m
    #average = sum(data) / m
    max_data = max(data)
    for i in range(m):
        d[i] = data[i] / max_data
    #print("av:", average, "max - min:", (max(data) - min(data)))
    return d, max_data

def get_data(data):
    '''sort data'''
    mileage = []
    price = []
    for row in data:
        mileage.append(int(row[0]))
        price.append(int(row[1]))
    m = data.line_num - 1
    return mileage, price, m

def train_model(data):
    '''using gradient descent algorithm
    Read dataset file and perform a linear regression on the data.'''

    theta = [0, 0]
    tmp = [0, 0]
    learning_rate = 0.1
    mileage, price, m = get_data(data)
    mileage, max_mileage = normalize_data(mileage, m)
    price, max_price = normalize_data(price, m)
    est0 = [0] * m
    est1 = [0] * m
    change = 0
    previous_change = 1

    while previous_change != change:
        previous_change = change
        for i in range(m):
            est0[i] = estimate_price(mileage[i], theta) - price[i]
            est1[i] = est0[i] * mileage[i]
        tmp[0] = learning_rate * (sum(est0)/m)
        tmp[1] = learning_rate * (sum(est1)/m)
        change = (abs(tmp[0] - theta[0]) + abs(tmp[1] + theta[1])) / 2
        theta[0] -= tmp[0]
        theta[1] -= tmp[1]
    #print("cost: ", cost_function(mileage, price, m, theta))
    return theta, max_mileage, max_price

if __name__ == "__main__":
    #print("What mileage to check?")
    #MILEAGE_TO_CHECK = int(input())
    MILEAGE_TO_CHECK = 73000
    
    FILE = open("data.csv", "r")
    DATA = csv.reader(FILE)
    next(DATA) # to cut the table's header
    THETA, MAX_MILEAGE, MAX_PRICE = train_model(DATA)
    MILEAGE_TO_CHECK /= MAX_MILEAGE
    RES = estimate_price((MILEAGE_TO_CHECK), THETA)
    print("\nHere is your price estimate: ", int(RES * MAX_PRICE), '\n')
    FILE.close()
