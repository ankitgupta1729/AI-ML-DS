from calculator import add_numbers, divide_numbers
import random

def main(value_param):
    a = 10
    b = random.randint(0, 2)  # Random integer between 0 and 2
    if value_param == 'sum':
        value = add_numbers(a, b)
        print(f"The sum of {a} and {b} is {value}")

    if value_param == 'divide':
        value = divide_numbers(a, b)
        print(f"The division of {a} by {b} is {value}")

if __name__ == "__main__":
    #main('sum')
    main('divide')