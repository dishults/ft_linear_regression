#!/usr/bin/env python3
'''
Train model
'''
import csv

import estimate as e
import bonus as b

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
        if len(row) != 2:
            raise IndexError('Too many columns')
    m = data.line_num - 1
    return mileage, price, m

def train_model(mileage, price, m, learning_rate):
    '''using a linear function with a gradient descent algorithm'''
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
    print('Training successful.\n',\
        '\nAlgorithm precision (less is better, 0 is best):\n',\
        '\n- with default thetas [0, 0]:',\
        f'\n\t{b.cost_function(n_mileage, n_price, m, [0, 0])}\n',\
        f'\n- with trained thetas {theta}:',\
        f'\n\t{b.cost_function(n_mileage, n_price, m, theta)}\n')
    return theta, sum(mileage)/m, sum(price)/m

def process():
    'Read data file -> train model on it -> store the results'
    with open("data.csv") as file:
        data = csv.reader(file)
        header = next(data)
        assert len(header) == 2
        assert not any(cell.isdigit() for cell in header)
        mileage, price, lines_nb = get_data(data)
    theta, average_m, average_p = train_model(mileage, price, lines_nb, 0.1)
    with open("results.csv", 'w+') as res:
        writer = csv.writer(res)
        writer.writerow(theta)
        writer.writerow([average_m, average_p])
        writer.writerow([(max(mileage) - min(mileage)), (max(price) - min(price))])
    b.plot(mileage, price, lines_nb)

if __name__ == "__main__":
    e.dir_check()
    try:
        process()
    except IOError as ex:
        print((type(ex).__name__))
        print('Couldn\'t find \"data.csv\" file to train the model.',\
            '\nMake sure "data.csv" is in the same folder with your',\
            'training program and you launch it from that folder')
    except (IndexError, ValueError) as ex:
        print(f'Exception {type(ex).__name__} has occured with msg:\n{ex}\n',\
            '\nDouble check that your \"data.csv\" file is correct.',\
            '\n- first line is a header: km,price',\
            '\n- all other lines are positive integers (two per line)',\
            '\n- no empty new lines at the end or just one',\
            '\n- no other funky stuff. Just data, pure data')
    except (ZeroDivisionError, StopIteration) as ex:
        print('''File "data.csv" must have at least three lines''')
    except AssertionError as ex:
        print('Incorrect header for \"data.csv\" file.',\
            'Your file should have a header with two values, ex:\nkm,price')
