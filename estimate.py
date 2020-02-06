#!/usr/bin/env python3
'''
Estimate price of the car for the given mileage
'''
import os
import csv
import sys

MILEAGE = 0
PRICE = 1

def estimate_price(mileage, theta):
    'estimate the price of a car for a given mileage'
    return theta[0] + (theta[1] * mileage)

def process(mileage_to_check):
    'estimate the price with trained or default thetas'
    try:
        with open("results.csv") as file:
            data = csv.reader(file)
            line = next(data)
            theta = float(line[0]), float(line[1])
            line = next(data)
            average = float(line[0]), float(line[1])
            line = next(data)
            max_minus_min = int(line[0]), int(line[1])
            normalized_mileage = (mileage_to_check - average[MILEAGE]) / max_minus_min[MILEAGE]
            normalized_price = estimate_price((normalized_mileage), theta)
            price_estimate = max_minus_min[PRICE] * normalized_price + average[PRICE]
    except IOError:
        theta = [0, 0]
        price_estimate = estimate_price(mileage_to_check, theta)
    if price_estimate < 0:
        price_estimate = 0
    return price_estimate

def get_mileage_to_check():
    'Get a positive mileage from user to estimate the price'
    print("What mileage to check?")
    while True:
        try:
            mileage = int(input())
            assert mileage >= 0
            break
        except ValueError:
            print("Enter a valid number or hit Ctrl+C to exit")
        except AssertionError:
            print("Value is negative, try again with a positive number")
        except KeyboardInterrupt:
            sys.exit("\nStopped by the user")
    return mileage

def dir_check():
    '''Checks that you're trying to launch your program from
    ft_linear_regression directory'''
    cwd = os.getcwd()
    dirr = os.path.basename(cwd)
    if dirr != 'ft_linear_regression':
        sys.exit('Error: make sure you are in "ft_linear_regression" directory')

if __name__ == "__main__":
    dir_check()
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if not arg.isdigit():
                continue
            MILEAGE_TO_CHECK = int(arg)
            RESULT = int(process(MILEAGE_TO_CHECK))
            print(f"\nFor mileage {MILEAGE_TO_CHECK} price estimate is: {RESULT}")
    else:
        MILEAGE_TO_CHECK = get_mileage_to_check()
        RESULT = int(process(MILEAGE_TO_CHECK))
        print("\nHere is your price estimate: ", RESULT)
