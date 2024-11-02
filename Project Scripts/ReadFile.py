import os
from tkinter import filedialog, messagebox

class CodeFileReader:
    def __init__(self, file_path: str = ""):
        self.file_path = file_path
        self.code_string = ""

    def add_file(self, file_path: str = ""):
        self.file_path = file_path
        self.code_string = ""

    def read_code(self):
        try:
            if not os.path.isfile(self.file_path):
                raise FileNotFoundError(f"The file {self.file_path} does not exist.")

            if not self.is_supported_file():
                raise ValueError("Unsupported file type. Please provide a valid Python (.py) or C++ (.cpp) file.")

            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.code_string = file.read()

        except FileNotFoundError as fnf_error:
            messagebox.showerror("File Not Found", str(fnf_error))
        except ValueError as ve:
            messagebox.showerror("Unsupported File Type", str(ve))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

    def is_supported_file(self):
        """Check if the file is a Python or C++ file."""
        try:
            _, file_extension = os.path.splitext(self.file_path)
            return file_extension in ['.py', '.cpp']
        except Exception as e:
            messagebox.showerror("Error", f"Error checking file type: {str(e)}")
            return False

    def navigate_file(self):
        try:
            self.file_path = filedialog.askopenfilename(title="Select a file")
            if self.file_path:
                print("File loaded successfully.")
            else:
                messagebox.showinfo("No File Selected", "No file was selected.")
        except Exception as e:
            messagebox.showerror("File Selection Error", f"An error occurred while selecting a file: {str(e)}")

    def get_code_string(self):
        return self.code_string
