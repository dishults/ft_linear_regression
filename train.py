#!/usr/bin/env python3
'''
Train model
'''
import csv

from estimate import dir_check, price_estimate
import bonus

THETA = [0, 0]

class Data:
    'All necessary data for model training'

    def __init__(self):
        self.m = 0  #number of lines
        self.learning_rate = 0.1
        self.mileage = Mileage()
        self.price = Price()

    def get_data(self, data_csv):
        'sort data'
        for row in data_csv:
            self.mileage.mileage.append(int(row[0]))
            self.price.price.append(int(row[1]))
            if len(row) != 2:
                raise IndexError('Too many columns')
        self.m = data_csv.line_num - 1

    def normalize(self):
        'normalize data for easier model training'
        self.mileage.normalize(self.m)
        self.price.normalize(self.m)

class Mileage:
    'Mileage of a car in km'
    def __init__(self):
        self.mileage = []
        self.normalized = []
        self.average = 0
        self.max_minus_min = 0

    def normalize(self, m):
        '''through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average)'''
        self.normalized = [0] * m
        self.average = sum(self.mileage) / m
        self.max_minus_min = max(self.mileage) - min(self.mileage)
        for i in range(m):
            self.normalized[i] = (self.mileage[i] - self.average) / self.max_minus_min

class Price:
    'Price for a given mileage'
    def __init__(self):
        self.price = []
        self.normalized = []
        self.average = 0
        self.max_minus_min = 0

    def normalize(self, m):
        '''through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average)'''
        self.normalized = [0] * m
        self.average = sum(self.price) / m
        self.max_minus_min = max(self.price) - min(self.price)
        for i in range(m):
            self.normalized[i] = (self.price[i] - self.average) / self.max_minus_min

def train_model(data):
    'using a linear function with a gradient descent algorithm'
    mileage, price, learning_rate, m = data.mileage, data.price, data.learning_rate, data.m
    tmp = [0, 0]
    est = [[0] * m, [0] * m]
    change = [0, 1]
    data.normalize()
    while change[0] != change[1]:
        change[0] = change[1]
        for i in range(m):
            est[0][i] = price_estimate(mileage.normalized[i], THETA) - price.normalized[i]
            est[1][i] = est[0][i] * mileage.normalized[i]
        tmp[0] = learning_rate * (sum(est[0])/m)
        tmp[1] = learning_rate * (sum(est[1])/m)
        change[1] = (abs(tmp[0] - THETA[0]) + abs(tmp[1] + THETA[1])) / 2
        THETA[0] -= tmp[0]
        THETA[1] -= tmp[1]

def process():
    'Read data file -> train model on it -> store the results'
    with open("data.csv") as file:
        data_csv = csv.reader(file)
        header = next(data_csv)
        assert len(header) == 2
        assert not any(cell.isdigit() for cell in header)
        data = Data()
        data.get_data(data_csv)
    train_model(data)
    with open("results.csv", 'w') as res:
        writer = csv.writer(res)
        writer.writerow(THETA)
        writer.writerow([data.mileage.average, data.price.average])
        writer.writerow([data.mileage.max_minus_min, data.price.max_minus_min])
    bonus.show(data, THETA)

if __name__ == "__main__":
    dir_check()
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
