#!/usr/bin/env python3
"""
Train model
"""

import csv

from estimate import dir_check
from estimate import Price as p
import bonus

class Mileage:
    """Mileage of a car in km."""

    mileage = []
    normalized = []
    average = 0
    range_ = 0

    @classmethod
    def normalize(cls):
        """Normalize through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average).
        """

        cls.average = sum(cls.mileage) / Data.m
        cls.range_ = max(cls.mileage) - min(cls.mileage)
        cls.normalized = [(km - cls.average) / cls.range_ for km in cls.mileage]

class Price:
    """Price for a given mileage."""

    price = []
    normalized = []
    average = 0
    range_ = 0

    @classmethod
    def normalize(cls):
        """Normalize through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average).
        """

        cls.average = sum(cls.price) / Data.m
        cls.range_ = max(cls.price) - min(cls.price)
        cls.normalized = [(price - cls.average) / cls.range_ for price in cls.price]

class Data:
    """All necessary data for model training."""

    m = 0  # Number of lines
    theta = [0, 0]

    @classmethod
    def get_data(cls, data_csv):
        """Sort csv data into Mileage and Price and normalize them."""

        for mileage, price in data_csv:
            Mileage.mileage.append(int(mileage))
            Price.price.append(int(price))            
        cls.m = data_csv.line_num - 1
        Mileage.normalize(), Price.normalize()

    @classmethod
    def train_model(cls, learning_rate=0.1):
        """Train model using linear function with gradient descent algorithm."""

        tmp = [0, 0]
        est = [[0] * cls.m, [0] * cls.m]
        change = [0, 1]

        while change[0] != change[1]:
            change[0] = change[1]
            for i in range(cls.m):
                est[0][i] = p.estimate(Mileage.normalized[i], cls.theta) - Price.normalized[i]
                est[1][i] = est[0][i] * Mileage.normalized[i]
            tmp[0] = learning_rate * (sum(est[0])/cls.m)
            tmp[1] = learning_rate * (sum(est[1])/cls.m)
            change[1] = (abs(tmp[0] - cls.theta[0]) + abs(tmp[1] + cls.theta[1])) / 2
            cls.theta[0] -= tmp[0]
            cls.theta[1] -= tmp[1]

    @classmethod
    def process(cls):
        """Read data file -> train model on it -> store the results."""

        with open("data.csv") as file:
            data_csv = csv.reader(file)
            header = next(data_csv)
            assert len(header) == 2
            assert not any(cell.isdigit() for cell in header)
            cls.get_data(data_csv)
        cls.train_model()
        with open("results.csv", 'w') as res:
            writer = csv.writer(res)
            writer.writerow(cls.theta)
            writer.writerow([Mileage.average, Price.average])
            writer.writerow([Mileage.range_, Price.range_])

def main():
    dir_check()
    try:
        Data.process()
        bonus.show(Mileage, Price, Data)
    except IOError as ex:
        print((type(ex).__name__))
        print('Couldn\'t find \"data.csv\" file to train the model.'
              '\nMake sure "data.csv" is in the same folder with your'
              'training program and you launch it from that folder')
    except (IndexError, ValueError) as ex:
        print(f'Exception {type(ex).__name__} has occured with msg:\n{ex}\n'
              '\nDouble check that your \"data.csv\" file is correct.'
              '\n- first line is a header: km,price'
              '\n- all other lines are positive integers (two per line)'
              '\n- no empty new lines at the end or just one'
              '\n- no other funky stuff. Just data, pure data')
    except (ZeroDivisionError, StopIteration) as ex:
        print('''File "data.csv" must have at least three lines''')
    except AssertionError as ex:
        print('Incorrect header for \"data.csv\" file.\n'
              'Your file should have a header with two values, ex:\n\tkm,price')

if __name__ == "__main__":
    main()