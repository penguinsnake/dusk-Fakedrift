import sys
import tkinter as tk
import time
import os

class Dusk:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.commands = {
            'print': self._print_command,
            'assign': self._assign_command,
            'add': self._add_command,
            'subtract': self._subtract_command,
            'multiply': self._multiply_command,
            'divide': self._divide_command,
            'window': self._window_command,
            'interact': self._run_interactive_mode,
            'mkdir': self._mkdir_command,
            'time': self._time_command,
            'dassign': self._de_assign_command
        }

    def _print_command(self, args):
        if len(args) != 1:
            return "Error: Invalid print command"
        value = args[0]

        # Check if value is a variable
        if value in self.variables:
            return self.variables[value]

        # Check if value is a string literal
        if value.startswith("'") and value.endswith("'"):
            # If the value is a string literal, print the string without the surrounding quotes
            return value[1:-1]

        # If the value is neither a variable nor a string literal, it's an error
        return f"Error: Invalid value '{value}' to print"

    def _assign_command(self, args):
        if len(args) != 2:
            return "Error: Invalid assign command"
        variable_name, value = args
        self.variables[variable_name] = value
        return None

    def _run_interactive_mode(self, args):
        if len(args) != 0:
            return "Error: interact command takes no arguments"
        print("Welcome to Dusk's REPL")
        print("Enter 'exit' to quit.")
        
        while True:
            command = input(">>> ").strip()

            if command.lower() == 'exit':
                print("Exiting Dusk's REPL")
                break

            result = self.parse_command(command)
            if result is not None and result != '':
                print(result)

    def _add_command(self, args):
        if len(args) != 3:
            return "Error: Invalid add command"
        variable_name, value1, value2 = args

        # Check if value1 is a variable
        if value1 in self.variables:
            value1 = self.variables[value1]

        # Check if value2 is a variable
        if value2 in self.variables:
            value2 = self.variables[value2]

        try:
            result = int(value1) + int(value2)
            self.variables[variable_name] = result
        except ValueError:
            return f"Error: Invalid values '{value1}' or '{value2}' for addition"
        
    def _window_command(self, args):
        if len(args) != 3:
            return "Error: Invalid window command"
        title, width, height = args
        root = tk.Tk()
        root.geometry(f"{width}x{height}")
        root.title(title)
        root.mainloop()

    def _subtract_command(self, args):
        if len(args) != 3:
            return "Error: Invalid subtract command"
        variable_name, value1, value2 = args
        try:
            value1 = int(value1) if value1.isdigit() else int(self.variables.get(value1, 0))
            value2 = int(value2) if value2.isdigit() else int(self.variables.get(value2, 0))
            result = value1 - value2
            self.variables[variable_name] = result
        except ValueError:
            return f"Error: Invalid values '{value1}' or '{value2}' for subtraction"

    def _multiply_command(self, args):
        if len(args) != 3:
            return "Error: Invalid multiply command"
        variable_name, value1, value2 = args
        try:
            value1 = int(value1) if value1.isdigit() else int(self.variables.get(value1, 0))
            value2 = int(value2) if value2.isdigit() else int(self.variables.get(value2, 0))
            result = value1 * value2
            self.variables[variable_name] = result
        except ValueError:
            return f"Error: Invalid values '{value1}' or '{value2}' for multiplication"

    def _divide_command(self, args):
        if len(args) != 3:
            return "Error: Invalid divide command"
        variable_name, value1, value2 = args
        try:
            value1 = int(value1) if value1.isdigit() else int(self.variables.get(value1, 0))
            value2 = int(value2) if value2.isdigit() else int(self.variables.get(value2, 0))
            if value2 == 0:
                return "Error: Division by zero"
            result = value1 / value2
            self.variables[variable_name] = result
        except ValueError:
            return f"Error: Invalid values '{value1}' or '{value2}' for division"

    def _mkdir_command(self, args):
        if len(args) != 1:
            return "Error: Invalid mkdir command"
        directory_name = args[0]
        try:
            os.mkdir(directory_name)
            return f"Directory '{directory_name}' created successfully."
        except OSError:
            return f"Error: Failed to create directory '{directory_name}'."

    def _time_command(self, args):
        if len(args) != 1:
            return "Error: Invalid time command. Usage: time <variable_name>"
        variable_name = args[0]
        current_time = time.strftime("%H:%M:%S", time.localtime())
        self.variables[variable_name] = current_time
        return f"Time saved to variable '{variable_name}': {current_time}"

    def _de_assign_command(self, args):
        if len(args) != 1:
            return "Error: Invalid de-assign command. Usage: dassign <variable_name>"
        variable_name = args[0]
        if variable_name in self.variables:
            del self.variables[variable_name]
            return f"Variable '{variable_name}' de-assigned."
        else:
            return f"Error: Variable '{variable_name}' not found for de-assignment."

    def parse_file(self, filename):
        """Parse and execute commands from a file."""
        output = ""
        with open(filename, 'r') as file:
            first_line = file.readline().strip()
            if first_line != "start|dusk":
                print(f"Warning: dusk (language) hasn't been started in {filename}, it won't work, the first line should be start|dusk")
                sys.exit()
            
            for line in file:
                command = line.strip()
                if command:
                    result = self.parse_command(command)
                    if result is not None and result != '':
                        output += str(result) + "\n"
        print(output.strip())

    def parse_command(self, command):
        """Parse and execute a command."""
        tokens = command.split('|')
        command_name = tokens[0].strip()

        # Check if the command is a comment and ignore it
        if command_name.startswith('@'):
            return ''

        if command_name in self.commands:
            result = self.commands[command_name](tokens[1:])
            return result if result is not None else ''
        elif command_name in self.functions:
            # Execute the function
            function_body = self.functions[command_name]
            function_args = tokens[1:]
            return self._execute_function(function_body, function_args)
        else:
            return "Error: Invalid command"

# Create an instance of the Dusk class
dusk_lang = Dusk()

# Parse commands from .dusk files
import glob
for file_name in glob.glob("*.dusk"):
    dusk_lang.parse_file(file_name)

time.sleep(2)  # Optional delay to allow messages to be seen before program exits
