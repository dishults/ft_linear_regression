'''
linear regression with a single feature - the mileage of the car.
'''
import csv
import estimate as e

#def cost_function(x, y, m, t):
#    est = [0] * m
#    for i in range(m):
#        est[i] = (estimate_price(x[i], t) - y[i])**2
#    cost = sum(est)/(2 * m)
#    return cost

def normalize_data(data, m):
    '''through Feature Scaling (dividing by "max-min")
    and Mean Normalization (substracting average)'''
    normalized = [0] * m
    average = sum(data) / m
    max_minus_min = max(data) - min(data)
    for i in range(m):
        normalized[i] = (data[i] - average) / max_minus_min
    return normalized

def get_data(data):
    'sort data'
    mileage = []
    price = []
    for row in data:
        mileage.append(int(row[0]))
        price.append(int(row[1]))
    m = data.line_num - 1
    return mileage, price, m

def train_model(mileage, price, m, learning_rate):
    '''using gradient descent algorithm
    Read dataset file and perform a linear regression on the data.'''
    theta = [0, 0]
    tmp = [0, 0]
    n_mileage = normalize_data(mileage, m)
    n_price = normalize_data(price, m)
    est = [[0] * m, [0] * m]
    change = [0, 1]
    while change[0] != change[1]:
        change[0] = change[1]
        for i in range(m):
            est[0][i] = e.estimate_price(n_mileage[i], theta) - n_price[i]
            est[1][i] = est[0][i] * n_mileage[i]
        tmp[0] = learning_rate * (sum(est[0])/m)
        tmp[1] = learning_rate * (sum(est[1])/m)
        change[1] = (abs(tmp[0] - theta[0]) + abs(tmp[1] + theta[1])) / 2
        theta[0] -= tmp[0]
        theta[1] -= tmp[1]
    #print("cost: ", cost_function(mileage, price, m, theta))
    return theta, sum(mileage)/m, sum(price)/m

def process():
    try:
        with open("data.csv") as file:
            data = csv.reader(file)
            next(data) # to cut the table's header
            mileage, price, lines_nb = get_data(data)
        theta, average_m, average_p = train_model(mileage, price, lines_nb, 0.1)
        with open("results.csv", 'w+') as res:
            writer = csv.writer(res)
            writer.writerow(theta)
            writer.writerow([average_m, average_p])
            writer.writerow([(max(mileage) - min(mileage)), (max(price) - min(price))])
        return 1
    except IOError:
        print('''Couldn't find "data.csv" file to train the model''')
        return 0

if __name__ == "__main__":
    if process() == 1:
        print("Training successful")
