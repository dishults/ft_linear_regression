'''
linear regression with a single feature - the mileage of the car.
'''
import csv
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
            #print(theta[0], theta[1])
            #print(average[MILEAGE], average[PRICE])
            #print(max_minus_min[MILEAGE], max_minus_min[PRICE])
            normalized_mileage = (mileage_to_check - average[MILEAGE]) / max_minus_min[MILEAGE]
            normalized_price = estimate_price((normalized_mileage), theta)
            price_estimate = max_minus_min[PRICE] * normalized_price + average[PRICE]
    except IOError:
        theta = [0, 0]
        price_estimate = estimate_price(mileage_to_check, theta)
    return price_estimate

def get_mileage_to_check():
    "Get a positive mileage from user to estimate the price"
    mileage = -1
    while mileage < 0:
        print("What mileage to check?")
        mileage = int(input())
        if mileage < 0:
            print("Value is negative, try again with a positive number")
    return mileage

if __name__ == "__main__":
    MILEAGE_TO_CHECK = get_mileage_to_check()
    RESULT = int(process(MILEAGE_TO_CHECK))
    if RESULT <= 0:
        print("\nThe estimate is that your car isn't worth anything.")
        print("Keep using it or recycle and get a new one.")
    else:
        print("\nHere is your price estimate: ", RESULT)
