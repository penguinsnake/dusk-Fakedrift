#1.3-2 BETA
def greater(args):
    if len(args) != 2:
        return "Error: Invalid number of arguments"
    try:
        # Convert arguments to integers
        # If an error occurs, return "Error: Non-integer arguments provided"
        num1 = int(args[0])
        num2 = int(args[1])
        # Return True if num1 is greater than num2, else False
        return num1 > num2
    except ValueError:
        return "Error: Non-integer arguments provided"

if __name__ == "__main__":
    import sys
    # Pass command-line arguments to the greater function
    result = greater(sys.argv[1:])
    # Print the result to standard output
    print(result)