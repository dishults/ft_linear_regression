#!/usr/bin/env python3
"""
Estimate price of the car for the given mileage.
"""

import os
import csv
import sys

class Mileage:
    """Mileage of a car in km."""

    to_check = 0
    normalized = 0
    average = 0
    range_ = 0

    @classmethod
    def get_mileage_to_check(cls):
        """Get mileage for which to estimate price."""

        print("What mileage to check?")
        while True:
            try:
                cls.to_check = int(input())
                assert cls.to_check >= 0
                break
            except ValueError:
                print("Enter a valid number or hit Ctrl+C to exit")
            except AssertionError:
                print("Value is negative, try again with a positive number")
            except KeyboardInterrupt:
                sys.exit("\nStopped by the user")

    @classmethod
    def normalize(cls):
        """Normalize through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average).
        """

        cls.normalized = (cls.to_check - cls.average) / cls.range_

class Price:
    """Price for a given mileage."""

    normalized = 0
    average = 0
    range_ = 0
    estimated = 0

    @classmethod
    def normalize(cls):
        """Normalize through Feature Scaling (dividing by "max-min")
        and Mean Normalization (substracting average).
        """

        cls.normalized = cls.estimate((Mileage.normalized), Data.theta)

    @classmethod
    def denormalize(cls):
        """Return a real value."""

        return cls.range_ * cls.normalized + cls.average

    @staticmethod
    def estimate(mileage, theta):
        """Return price estimate of a car for a given mileage."""

        return theta[0] + (theta[1] * mileage)

class Data:
    """All data."""

    theta = [0, 0]

    @staticmethod
    def __str__():
        return f"\nFor mileage {Mileage.to_check} price estimate is: {Price.estimated}"

    @classmethod
    def process(cls):
        """Estimate price with trained or default thetas."""

        try:
            with open("results.csv") as file:
                data = csv.reader(file)
                cls.theta = [float(d) for d in next(data)]
                Mileage.average, Price.average = [float(d) for d in next(data)]
                Mileage.range_, Price.range_ = [int(d) for d in next(data)]
                Mileage.normalize(), Price.normalize()
                Price.estimated = int(Price.denormalize())
        except IOError:
            Price.estimated = int(Price.estimate(Mileage.to_check, cls.theta))
        Price.estimated = max(0, Price.estimated)  # if estimated is < 0 set it to 0

def dir_check():
    """Checks that you're trying to launch your program from
    ft_linear_regression directory.
    """

    cwd = os.getcwd()
    dirr = os.path.basename(cwd)
    if dirr != 'ft_linear_regression':
        sys.exit('Error: make sure you are in "ft_linear_regression" directory')

def main():
    dir_check()
    if len(sys.argv) > 1:
        for arg in sys.argv:
            try:
                Mileage.to_check = int(arg)
                assert Mileage.to_check >= 0
                Data.process()
                print(Data())
            except (ValueError, AssertionError):
                pass
    else:
        Mileage.get_mileage_to_check()
        Data.process()
        print(Data())

if __name__ == "__main__":
    main()
