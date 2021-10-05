from prompt_toolkit.shortcuts import button_dialog, input_dialog

def main():

    starting_number = input_dialog(
        title="Collatz Equation", text="Please enter any positive whole number:"
    ).run()

    starting_number = int(starting_number)

    counter = 0
    while starting_number > 1:
        counter += 1
        if  starting_number % 2 == 0:
            starting_number = starting_number / 2
        else:
            starting_number = (3 * starting_number + 1)/2
        print(starting_number)

    print(f'The total number of iterations it took to get back to one is: {counter}') 

    result = button_dialog(
        title="Button dialog example",
        text="Are you sure?",
        buttons=[("Yes", True), ("No", False), ("Maybe...", None)],
    ).run()

    print("Result = {}".format(result))


if __name__ == "__main__":
    main()
