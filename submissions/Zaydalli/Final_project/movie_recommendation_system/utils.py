import os
import sys

# ANSI Escape codes for basic colored output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a styled header."""
    clear_screen()
    print(f"{Colors.OKCYAN}{Colors.BOLD}{'=' * 50}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{title.center(50)}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{'=' * 50}{Colors.ENDC}")

def print_success(message):
    """Prints a success message in green."""
    print(f"{Colors.OKGREEN}✔ {message}{Colors.ENDC}")

def print_error(message):
    """Prints an error message in red."""
    print(f"{Colors.FAIL}✖ {message}{Colors.ENDC}")

def print_warning(message):
    """Prints a warning message in yellow."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def input_string(prompt, required=True):
    """Prompts the user for a string, with optional validation for empty input."""
    while True:
        value = input(prompt).strip()
        if required and not value:
            print_error("Input cannot be empty. Please try again.")
        else:
            return value

def input_int(prompt, min_val=None, max_val=None):
    """Prompts the user for an integer, with optional min/max validation."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                print_error("Input cannot be empty. Please try again.")
                continue
            
            value = int(value)
            if min_val is not None and value < min_val:
                print_error(f"Value must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print_error(f"Value cannot exceed {max_val}.")
                continue
            
            return value
        except ValueError:
            print_error("Invalid input. Please enter a valid number.")

def pause():
    """Pauses execution until the user presses Enter."""
    input(f"\n{Colors.OKBLUE}Press Enter to continue...{Colors.ENDC}")
