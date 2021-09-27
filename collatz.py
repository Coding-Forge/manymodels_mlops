def main():
    starting_number = int(input("Please enter any positive whole number: "))

    counter = 0
    while starting_number > 1:
        counter += 1
        if  starting_number % 2 == 0:
            starting_number = starting_number / 2
        else:
            starting_number = (3 * starting_number + 1)/2
        print(starting_number)

    print(f'The total number of iterations it took to get back to one is: {counter}') 

if __name__ == "__main__":
    main()