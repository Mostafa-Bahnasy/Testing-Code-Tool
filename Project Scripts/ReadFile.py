import os
from tkinter import filedialog


class CodeFileReader:
    def __init__(self, file_path: str = ""):
        self.file_path = file_path
        self.code_string = ""

    def add_file(self, file_path:str = ""):
        self.file_path = file_path
        self.code_string = ""

    def read_code(self):
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")

        if not self.is_supported_file():
            raise ValueError("Unsupported file type. Please provide a valid Python (.py) or C++ (.cpp) file.")

        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.code_string = file.read()

    def is_supported_file(self):
        """Check if the file is a Python or C++ file."""
        _, file_extension = os.path.splitext(self.file_path)
        return file_extension in ['.py', '.cpp']

    def navigate_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a file")
        if self.file_path:
            print("Signal loaded successfully.")
        else:
            print("NO file uploaded.")


    def get_code_string(self):
        return self.code_string


