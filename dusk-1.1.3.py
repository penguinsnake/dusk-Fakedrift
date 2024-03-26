import subprocess as sub
import sys
import ast
import tkinter as tk
import time
import os
import math
import json

class Dusk:
    def __init__(self):
        self.variables = {}
        isModdedDusk = False
        global error_check
        error_check = f"isModdedDusk?: {str(isModdedDusk)} reason:"
        self.functions = {}
        self.included = {}
        self.command_tags = {  # Define command_tags attribute for multi-line content
            'writefil': True,
            'dfunction': True,
        }
        self.commands = {
            'print': self._print_command,
            'assign': self._assign_command,
            'add': self._add_command,
            'subtract': self._subtract_command,
            'multiply': self._multiply_command,
            'divide': self._divide_command,
            'window': self._window_command,
            'interact': self._run_interactive_mode,
            'time': self._time_command,
            'dassign': self._de_assign_command,
            'cdir': self._cdir_command,
            'deldir': self._deldir_command,
            'cfil': self._cfil_command,
            'delfil': self._delfil_command,
            'writefil': self._writefil_command,
            'scriptint': self._scriptint_command,
            'dfunction': self._function_command,
            'sroot': self._sroot_command,
            'input': self._input_command,
            'errorthrow': self._error_throw,
        }

        self.imported_modules = []

    def _input_command(self, args):
        if len(args) != 2:
            return "Error: Invalid input command. Usage: <variable_name> <message>"
        var_name = args[0]
        message = args[1]
        message = message.replace("'", "")
        self.variables[var_name] = input(message)

    def _error_throw(self, args):
        if len(args) != 2:
            return "Error: Wow an error from the error_throw command, smart. Usage: <message> <error or warning>"
        message = args[0]
        message = message.replace("'", "")
        ew = args[1]
        if ew == "error":
            print(f"Error: {message}")
            sys.exit()
        elif ew == "warning":
            print(f"Warning: {message}")
        else:
            print(f"dusk-1.1.3.py says: kys mr. {message}")

    def _sroot_command(self, args):
        if len(args) != 2:
            return "Error: Invalid sroot command. Usage: <variable_name> <input>"
        var_name = args[0]
        input_value = args[1]
        if input_value in self.variables:
            input_value = self.variables[input_value]
        if input_value.isdigit():
            input_value = int(input_value)
        elif not str(input_value).isdigit():
            self.variables[var_name] = "Error: sroot command failed, cannot print"
            return "Error: Invalid input type. Input must be a positive integer"
        output = math.sqrt(input_value)
        self.variables[var_name] = output

    def _scriptint_command(self, args):
        if len(args) < 3:
            return "Error: Invalid scriptint command. Usage: <output_var> <script_name> <arg1> <arg2> <arg3> ..."
        var_name = args[0]
        script_name = args[1] + '.py'
        full_path = os.path.join('scripts', script_name)
        full_path = full_path.replace("\\", "/")
        if args[2] != '.n':
            script_args = args[2:]
            for i, arg in enumerate(script_args):
                if arg in self.variables:
                    script_args[i] = self.variables[arg]
        else:
            script_args = ["none given, running error check",  f"{error_check} .n used in scriptint command"]
            print(script_args)
        
        try:
            # Run the script and capture its stdout
            result = sub.run(['python', full_path, *script_args], capture_output=True, text=True, check=True)
            # Evaluate the output to Python data structure
            ovars = ast.literal_eval(result.stdout.strip())
            # Assign the output to the variables dictionary
            if var_name != '.n':
                self.variables[var_name] = ovars
        except sub.CalledProcessError as e:
            print(f"Error executing script: {e}")
        except ValueError:
            print("Error: Script did not return a valid Python data structure")

    def _cdir_command(self, args):
        if len(args) != 1:
            return "Error: Invalid cdir command. Usage: <directory_name>"
        directory_name = args[0]
        try:
            os.mkdir(directory_name)
        except FileExistsError:
            return f"Error: Directory '{directory_name}' already exists."
        except Exception as e:
            return f"Error: {str(e)}"

    def _deldir_command(self, args):
        if len(args) != 1:
            return "Error: Invalid deldir command. Usage: <directory_name>"
        directory_name = args[0]
        try:
            os.rmdir(directory_name)
        except FileNotFoundError:
            return f"Error: Directory '{directory_name}' not found."
        except OSError as e:
           return f"Error: {str(e)}"

    def _function_command(self, args):
        # Check if the command has at least 2 arguments
        if len(args) < 2:
            return "Error: Invalid function command. Usage: <function_name> {<function_body>}"

        # Extract function name and function body
        function_name = args[0]
        function_body = ' '.join(args[2:]).strip()  # Combine all arguments except the first one and remove leading/trailing spaces
        function_body = function_body.replace('{', '').replace('}', '')  # Remove '{' and '}'
        
        # Split function body into individual commands based on newline character
        commands = function_body.split('\n')

        # Initialize lists to store commands and newlines separately
        command_list = []
        newline_list = []

        # Iterate through commands and separate commands and newlines
        for command in commands:
            if command.startswith('>'):
                command_list.append(command.lstrip('>'))  # Remove '>' and leading/trailing spaces
            elif command.strip():  # Check if command is not an empty line
                newline_list.append(command)

        try:
            # Add the function to the functions dictionary along with newline commands
            if newline_list:
                self.functions[function_name] = (command_list, newline_list)
            else:
                self.functions[function_name] = command_list
            return None
        except Exception as e:
            return f"Error: {str(e)}"

    def _writefil_command(self, args):
        # Check if the command has at least 4 arguments
        if len(args) < 4:
            return "Error: Invalid writefil command. Usage: <directory>|<file_name>|<file_extension>{<file_content>}"

        # Extract arguments
        directory_name, file_name, file_extension = args[:3]
        
        if directory_name == ".p":
            directory_name = os.getcwd()
        # Extract file content by joining all remaining arguments and removing curly braces
        file_content = ' '.join(args[3:])
        file_content = file_content.replace('{', '').replace('}', '')

        # Remove '>' from the file content
        file_content = file_content.replace('>', '')

        # Remove '{' from the file name and extension
        file_name = file_name.replace('{', '')
        file_extension = file_extension.replace('{', '')

        try:
            # Concatenate directory path and file name
            file_path = os.path.join(directory_name, f"{file_name}.{file_extension}")

            # Write file content to the file with each line on a separate line
            with open(file_path, 'w') as f:
                # Split content by newline '\n' and write each line separately
                for line in file_content.split('\n'):
                    f.write(line.strip() + '\n')
        except Exception as e:
            return f"Error: {str(e)}"

    def _cfil_command(self, args):
        if len(args) != 3:
            return "Error: Invalid cfil command. Usage: <directory_name>|<file_name>|<file_extension>"
        directory_name, file_name, file_extension = args
        try:
            # Concatenate directory path and file name
            file_path = os.path.join(directory_name, file_name)
            # Add file extension to the file name
            file_path_with_extension = f"{file_path}.{file_extension}"
            # Create the file
            with open(file_path_with_extension, 'w'):
                pass
        except Exception as e:
            return f"Error: {str(e)}"


    def _delfil_command(self, args):
        if len(args) != 2:
            return "Error: Invalid delfil command. Usage: <directory_name> <file_name>"
        directory_name, file_name = args
        try:
            os.remove(os.path.join(directory_name, file_name))
            return f"File '{file_name}' deleted successfully from directory '{directory_name}'."
        except FileNotFoundError:
            return f"Error: File '{file_name}' not found in directory '{directory_name}'."
        except Exception as e:
            return f"Error: {str(e)}"

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

    def _run_interactive_mode(self, args):
        if len(args) != 0:
            return "Error: interact command takes no arguments"
        print("Welcome to Dusk's REPL")
        print("Enter 'exit' to quit.")
        
        while True:
            command = input("SANS@ ").strip()

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

    def _time_command(self, args):
        if len(args) != 1:
            return "Error: Invalid time command. Usage: <variable_name>"
        variable_name = args[0]
        current_time = time.strftime("%H:%M:%S", time.localtime())
        self.variables[variable_name] = current_time

    def _de_assign_command(self, args):
        if len(args) != 1:
            return "Error: Invalid de-assign command. Usage: <variable_name>"
        variable_name = args[0]
        if variable_name in self.variables:
            del self.variables[variable_name]
        else:
            return f"Error: Variable '{variable_name}' not found for de-assignment."

    def parse_file(self, filename):
        print("Hello from DUSK-python based")
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
                    result = self.parse_command(command, file)  # Pass the file object to parse_command
                    if result is not None and result != '':
                        output += str(result) + "\n"
        print(output.strip())

    def parse_command(self, command, file=None):
        # Check if the command is a comment (starts with "@")
        if command.startswith("@"):
            return None  # Skip comments

        # Parse the command name and arguments
        tokens = command.split('|')
        command_name = tokens[0]

        # Check if it's a standard command
        if command_name in self.commands:
            # Check if the command is a multi-line command
            is_multi_line = self.command_tags.get(command_name, False)

            if is_multi_line:
                # Gather multi-line content until the end tag is encountered
                multi_line_content = []
                if file is not None:
                    for line in file:  # Use the provided file object to read multi-line content
                        if line.strip() == '}':
                            break
                        multi_line_content.append(line.strip())

                # Pass multi-line content as a single argument to the command execution method
                return self.commands[command_name](tokens[1:] + ['\n'.join(multi_line_content)])
            else:
                # For single-line commands, pass arguments as usual
                return self.commands[command_name](tokens[1:])

        # If the command is not a recognized function or standard command, return an error
                    # Check if it's a function
        elif command_name in self.functions:
            # Execute each command in the function body
            for func_command in self.functions[command_name]:
                # Parse and execute the command
                result = self.parse_command(func_command)
                if result is not None and result != '':
                    print(result)  # Print command output for debugging
            
            # No need to return anything here since the function commands have already been executed
            return None
        else:
            return f"Error: Unknown command '{command_name}'"

# Create an instance of the Dusk class
dusk_lang = Dusk()

# Parse file of which is askedd
parsed_files = []
inp = input("which file would you want to run (exclude the .dusk extension)?  ")
file_name = f"{inp}.dusk"
if inp:
    if file_name not in parsed_files:
        print(f"Parsing {file_name}...")
        dusk_lang.parse_file(file_name)
        parsed_files.append(file_name)
    else:
        sys.exit(f"Error: File '{file_name}' has already been parsed")

time.sleep(2)
sys.exit()