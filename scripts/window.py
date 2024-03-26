import tkinter as tk
#1.3-2 BETA
def window():
    try:
        root = tk.Tk()
        root.geometry(f"300x300")
        root.title("dusk window")
        root.mainloop()
        return None
    except ValueError:
        return "Error: Non-integer arguments provided"

if __name__ == "__main__":
    # Pass command-line arguments to the greater function
    result = window()
    # Print the result to standard output
    print(result)