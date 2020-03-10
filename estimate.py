#!/usr/bin/env python3
'''
Estimate price of the car for the given mileage
'''
import os
import csv
import sys

class Mileage:
    'Mileage of a car in km'
    def __init__(self):
        self.to_check = 0
        self.normalized = 0
        self.average = 0
        self.max_minus_min = 0

    def __str__(self):
        return f"\nFor mileage {self.to_check}"

    def get_mileage_to_check(self):
        'For what mileage should the price be estimated'
        print("What mileage to check?")
        while True:
            try:
                self.to_check = int(input())
                assert self.to_check >= 0
                break
            except ValueError:
                print("Enter a valid number or hit Ctrl+C to exit")
            except AssertionError:
                print("Value is negative, try again with a positive number")
            except KeyboardInterrupt:
                sys.exit("\nStopped by the user")

    def normalize(self):
        '''through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average)'''
        self.normalized = (self.to_check - self.average) / self.max_minus_min

class Price:
    'Price for a given mileage'
    def __init__(self):
        self.normalized = 0
        self.average = 0
        self.max_minus_min = 0
        self.estimated = 0

    def __str__(self):
        return f"price estimate is: {self.estimated}"

    def normalize(self, mileage_normalized, theta):
        '''through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average)'''
        self.normalized = price_estimate((mileage_normalized), theta)

    def denormalize(self):
        'to a real value'
        return self.max_minus_min * self.normalized + self.average

def price_estimate(mileage, theta):
    'estimate the price of a car for a given mileage'
    return theta[0] + (theta[1] * mileage)

def process(mileage, price):
    'estimate the price with trained or default thetas'
    try:
        with open("results.csv") as file:
            data = csv.reader(file)
            line = next(data)
            theta = float(line[0]), float(line[1])
            line = next(data)
            mileage.average, price.average = float(line[0]), float(line[1])
            line = next(data)
            mileage.max_minus_min, price.max_minus_min = int(line[0]), int(line[1])
            mileage.normalize()
            price.normalize(mileage.normalized, theta)
            price.estimated = int(price.denormalize())
    except IOError:
        theta = [0, 0]
        price.estimated = int(price_estimate(mileage.to_check, theta))
    price.estimated = max(0, price.estimated) # if estimated is < 0 set it to 0

def dir_check():
    '''Checks that you're trying to launch your program from
    ft_linear_regression directory'''
    cwd = os.getcwd()
    dirr = os.path.basename(cwd)
    if dirr != 'ft_linear_regression':
        sys.exit('Error: make sure you are in "ft_linear_regression" directory')

if __name__ == "__main__":
    dir_check()
    MILEAGE = Mileage()
    PRICE = Price()
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if not arg.isdigit():
                continue
            MILEAGE.to_check = int(arg)
            process(MILEAGE, PRICE)
            print(MILEAGE, PRICE)
    else:
        MILEAGE.get_mileage_to_check()
        process(MILEAGE, PRICE)
        print(MILEAGE, PRICE)
