import subprocess
import tempfile
import os
from tkinter import messagebox

class CodeExecutor:
    def __init__(self, code: str = "", input_string: str = ""):
        self.code = code
        self.input_string = input_string
        self.output = ""

    def add_code(self, code: str, inp: str):
        self.code = code
        self.input_string = inp
        self.output = ""

    def run(self):
        try:
            if self.is_python_code():
                self.run_python_code()
            elif self.is_cpp_code():
                self.run_cpp_code()
            else:
                raise ValueError("Unsupported code type. Please provide valid Python or C++ code.")
        except ValueError as ve:
            messagebox.showerror("Error", f"{str(ve)}")

    def is_python_code(self):
        return "print" in self.code or "def " in self.code

    def is_cpp_code(self):
        return "#include" in self.code or "int main" in self.code

    def run_python_code(self):
        try:
            # Create a temporary Python file
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                temp_file.write(self.code.encode('utf-8'))
                temp_file_path = temp_file.name

            # Run the Python code with input redirection
            process = subprocess.run(
                ["python", temp_file_path],
                input=self.input_string,
                capture_output=True,
                text=True
            )

            # Store the output and errors
            self.output = process.stdout + process.stderr

        except subprocess.SubprocessError as e:
            messagebox.showerror("Execution Error", f"Error running Python code: {str(e)}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def run_cpp_code(self):
        global executable_path
        try:
            # Create a temporary C++ file
            with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as temp_file:
                temp_file.write(self.code.encode('utf-8'))
                temp_file_path = temp_file.name

            # Compile the C++ code
            executable_path = temp_file_path[:-4]  # Remove the .cpp extension
            compile_command = ["g++", temp_file_path, "-o", executable_path]

            try:
                subprocess.run(compile_command, check=True, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                self.output = f"Compilation Error:\n{e.stderr.decode()}"
                messagebox.showerror("Compilation Error", self.output)
                return

            # Run the compiled executable with input redirection
            process = subprocess.run(
                [executable_path],
                input=self.input_string,
                capture_output=True,
                text=True
            )

            # Store the output and errors
            self.output = process.stdout + process.stderr

        except subprocess.SubprocessError as e:
            messagebox.showerror("Execution Error", f"Error running C++ code: {str(e)}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
        finally:
            # Clean up the temporary files
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if os.path.exists(executable_path):
                os.remove(executable_path)

    def get_output(self):
        return self.output
