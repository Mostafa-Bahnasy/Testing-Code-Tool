import ollama
import re
from tkinter import messagebox

class OllamaChat:
    def __init__(self, model_name="phi3.5"):
        self.model_name = model_name

    def send_prompt(self, prompt: str):
        try:
            prompt = """provide me with only block of python code, with no text before or after it, this code
                        prints the following values in order I give you, and within the given constraints, The
                        values you print must be random within the constraints given, do not print further values.
            """ + prompt + """
            Do not make your code print extra text with the given input, just print numbers 
            without extra "Enter the number" or something like that.
            """

            result = self.get_response(prompt)

            if result.startswith("An error occurred:"):
                messagebox.showerror("Model Error", result)
                return result

            # Regular expression to find text within ```python ... ```
            match = re.search(r"```python(.*?)```", result, re.DOTALL)

            if match:
                return match.group(1).strip()  # Extracts and removes any surrounding whitespace
            else:
                messagebox.showinfo("No Code Found", "No Python code block found.")
                return "No Python code block found."

        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
            return f"An unexpected error occurred: {e}"

    def get_response(self, prompt):
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            return response.get('response', "No response text found")
        except Exception as e:
            messagebox.showerror("Ollama Model Error", f"Error generating response from model: {str(e)}")
            return f"An error occurred: {e}"
