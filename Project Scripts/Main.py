import tkinter as tk
from functools import partial
from tkinter import ttk
import CodeExecuter as CE
import ReadFile as CR
from tkinter import messagebox
import openai
import chatGPT_API as MG

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Testing Tool")
        self.window.geometry("1000x1000")

        self.model = MG.Phi3_5Model()

        # Create Tabs
        self.tab_control = ttk.Notebook(self.window)

        # Create the "Stress" tab
        self.stress_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.stress_tab, text="Stress")

        # Create the "Compare" tab
        self.compare_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.compare_tab, text="Compare")

        # Create the "Auto" tab
        self.auto_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.auto_tab, text="Auto")

        self.tab_control.pack(expand=1, fill="both")

        # Layout for the "Stress" tab
        self.create_stress_tab()

        # Layout for the "Compare" tab
        self.create_compare_tab()

        self.code_execute = CE.CodeExecutor()
        self.code_reader = CR.CodeFileReader()

        self.code_1_string = ""
        self.code_2_string = ""
        self.gen_code_string = ""
        self.ai_gen_code_string = ""
        self.compare_code_string = ""
        self.test_loop = 0

    def init_test_stress(self):
        self.test_loop = int(self.stress_test_num_entry.get())

        if self.code_1_string != self.input_code_1.get("1.0", "end-1c"):
            self.code_1_string = self.input_code_1.get("1.0", "end-1c")

        if self.code_2_string != self.input_code_2.get("1.0", "end-1c"):
            self.code_2_string = self.input_code_2.get("1.0", "end-1c")

        if self.gen_code_string != self.generator_box.get("1.0", "end-1c"):
            self.gen_code_string = self.generator_box.get("1.0", "end-1c")

        self.stress_test_method()

    def stress_test_method(self):
        self.test_loop -= 1
        if self.test_loop < 0:
            self.test_loop = 0
            messagebox.showinfo("Tests", "Test Cases Ended!")
            return

        input_test = self.execute_runner(self.gen_code_string, "")
        output_1 = self.execute_runner(self.code_1_string, input_test)
        output_2 = self.execute_runner(self.code_2_string, input_test)

        self.test_case_input_box.config(state=tk.NORMAL)
        self.test_case_input_box.delete(1.0, tk.END)
        self.test_case_input_box.insert(tk.END, input_test)
        self.test_case_input_box.config(state=tk.DISABLED)

        self.output_code_1.config(state=tk.NORMAL)
        self.output_code_2.config(state=tk.NORMAL)

        if self.test_show_radio_var.get() == "A":  # Show all outputs
            self.output_code_1.delete(1.0, tk.END)
            self.output_code_1.insert(tk.END, output_1)
            self.output_code_2.delete(1.0, tk.END)
            self.output_code_2.insert(tk.END, output_2)
        elif self.test_show_radio_var.get() == "B":  # Show wrong answers
            if self.compare_strings(output_2, output_1):
                self.output_code_1.delete(1.0, tk.END)
                self.output_code_2.delete(1.0, tk.END)
                self.output_code_1.insert(tk.END, "Passed!")
                self.output_code_2.insert(tk.END, "Passed!")
            else:

                self.output_code_1.delete(1.0, tk.END)
                self.output_code_1.insert(tk.END, output_1)
                self.output_code_2.delete(1.0, tk.END)
                self.output_code_2.insert(tk.END, output_2)
        self.output_code_1.config(state=tk.DISABLED)
        self.output_code_2.config(state=tk.DISABLED)

    def compare_strings(self, str1, str2):
        cleaned_str1 = ''.join(str1.split())
        cleaned_str2 = ''.join(str2.split())
        return cleaned_str1 == cleaned_str2

    def execute_runner(self, code: str, inp: str):
        self.code_execute.add_code(code, inp)
        self.code_execute.run()
        return self.code_execute.get_output()

    def on_click_upload_code(self, flag):
        self.code_reader.navigate_file()
        self.code_reader.read_code()
        if flag == 1:
            self.code_1_string = self.code_reader.get_code_string()
            self.input_code_1.delete(1.0, tk.END)
            self.input_code_1.insert(tk.END, self.code_1_string)
        elif flag == 2:
            self.code_2_string = self.code_reader.get_code_string()
            self.input_code_2.delete(1.0, tk.END)
            self.input_code_2.insert(tk.END, self.code_2_string)
        elif flag == 3:
            self.gen_code_string = self.code_reader.get_code_string()
            self.generator_box.delete(1.0, tk.END)
            self.generator_box.insert(tk.END, self.gen_code_string)
        elif flag == 4: #compare tab
            self.compare_code_string = self.code_reader.get_code_string()
            self.compare_code_box.delete(1.0,tk.END)
            self.compare_code_box.insert(tk.END,self.compare_code_string)

    def on_click_set_gen(self):
        if self.generate_radio_var.get() == "B":
            self.on_click_upload_code(3)
        elif self.generate_radio_var.get() == "A":
            self.validate_prompt()

    def show_ai_generator(self):
        self.gen_code_string = self.ai_gen_code_string

    def create_stress_tab(self):
        self.left_frame = tk.Frame(self.stress_tab)
        self.left_frame.grid(row=0, column=0, sticky="n")

        tk.Label(self.left_frame, text="Input Code_1:").grid(row=1, column=0, sticky="w")
        self.input_code_1 = tk.Text(self.left_frame, width=60, height=10)
        self.input_code_1.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.upload_code_1_butt = tk.Button(self.left_frame, text="Upload code_1", command=partial(self.on_click_upload_code, 1))
        self.upload_code_1_butt.grid(row=2, column=10, padx=5, pady=5)

        tk.Label(self.left_frame, text="Input Code_2:").grid(row=3, column=0, sticky="w")
        self.input_code_2 = tk.Text(self.left_frame, width=60, height=10)
        self.input_code_2.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.upload_code_2_butt = tk.Button(self.left_frame, text="Upload code_2", command=partial(self.on_click_upload_code, 2))
        self.upload_code_2_butt.grid(row=4, column=10, padx=5, pady=5)

        tk.Label(self.left_frame, text="Options:").grid(row=5, column=0, sticky="w")
        self.radio_frame2 = tk.Frame(self.left_frame)
        self.radio_frame2.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.generate_radio_var = tk.StringVar(value="A")
        self.ai_rad_butt = tk.Radiobutton(self.radio_frame2, text="Generate With AI", variable=self.generate_radio_var, value="A").pack(anchor="w")
        self.gen_rad_butt = tk.Radiobutton(self.radio_frame2, text="Write your Generator", variable=self.generate_radio_var, value="B").pack(anchor="w")

        tk.Label(self.left_frame, text="Generator/Prompt:").grid(row=8, column=0, sticky="w")
        self.generator_box = tk.Text(self.left_frame, width=60, height=10)
        self.generator_box.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.upload_gen_butt = tk.Button(self.left_frame, text="Set Generator", command=self.on_click_set_gen)
        self.upload_gen_butt.grid(row=9, column=10, padx=5, pady=5)

        tk.Label(self.left_frame, text="Number of Tests:").grid(row=10, column=0, sticky="w")
        self.bottom_frame = tk.Frame(self.left_frame)
        self.bottom_frame.grid(row=11, column=0, padx=5, pady=5, sticky="w")

        self.test_stress_butt = tk.Button(self.bottom_frame, text="Test", command=self.init_test_stress)
        self.test_stress_butt.grid(row=0, column=1, padx=5)

        validate_integer = self.window.register(self.validate_integer)
        self.stress_test_num_entry = tk.Entry(self.bottom_frame, validate="key", validatecommand=(validate_integer, '%P'))
        self.stress_test_num_entry.grid(row=0, column=2, padx=5)

        self.right_frame = tk.Frame(self.stress_tab)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        tk.Label(self.right_frame, text="Test Case:").grid(row=0, column=0, sticky="w")
        self.test_case_input_box = tk.Text(self.right_frame, width=40, height=10)
        self.test_case_input_box.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.test_case_input_box.config(state=tk.DISABLED)

        tk.Label(self.right_frame, text="Output Code_1:").grid(row=2, column=0, sticky="w")
        self.output_code_1 = tk.Text(self.right_frame, width=40, height=10)
        self.output_code_1.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.output_code_1.config(state=tk.DISABLED)

        tk.Label(self.right_frame, text="Output Code_2:").grid(row=4, column=0, sticky="w")
        self.output_code_2 = tk.Text(self.right_frame, width=40, height=10)
        self.output_code_2.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.output_code_2.config(state=tk.DISABLED)

        self.test_show_radio_var = tk.StringVar(value="A")
        tk.Label(self.right_frame, text="Show Output:").grid(row=6, column=0, sticky="w")
        self.show_frame = tk.Frame(self.right_frame)
        self.show_frame.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.show_all_butt = tk.Radiobutton(self.show_frame, text="Show All", variable=self.test_show_radio_var, value="A")
        self.show_all_butt.pack(anchor="w")
        self.show_wrong_butt = tk.Radiobutton(self.show_frame, text="Show Wrong", variable=self.test_show_radio_var, value="B")
        self.show_wrong_butt.pack(anchor="w")
        self.next_test_but = tk.Button(self.right_frame, text="Next Test", command=self.stress_test_method)
        self.next_test_but.grid(row=9, column=0, padx=5)

    def create_compare_tab(self):
        self.compare_frame = tk.Frame(self.compare_tab)
        self.compare_frame.pack(padx=10, pady=10)

        # Left Frame for Code
        self.left_compare_frame = tk.Frame(self.compare_frame)
        self.left_compare_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        tk.Label(self.left_compare_frame, text="Code:").grid(row=0, column=0, sticky="w")
        self.compare_code_box = tk.Text(self.left_compare_frame, width=50, height=30)
        self.compare_code_box.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Buttons for loading and running code
        self.load_code_button = tk.Button(self.left_compare_frame, text="Load Code", command=partial(self.on_click_upload_code, 4))
        self.load_code_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.run_code_button = tk.Button(self.left_compare_frame, text="Run Code", command=self.run_code)
        self.run_code_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Right Frame for Outputs
        self.right_compare_frame = tk.Frame(self.compare_frame)
        self.right_compare_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

        tk.Label(self.right_compare_frame, text="Test Case:").grid(row=0, column=0, sticky="w")
        self.test_case_box = tk.Text(self.right_compare_frame, width=40, height=10)
        self.test_case_box.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        tk.Label(self.right_compare_frame, text="Correct Output:").grid(row=2, column=0, sticky="w")
        self.correct_output_box = tk.Text(self.right_compare_frame, width=40, height=10)
        self.correct_output_box.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        tk.Label(self.right_compare_frame, text="Output:").grid(row=4, column=0, sticky="w")
        self.output_box = tk.Text(self.right_compare_frame, width=40, height=10)
        self.output_box.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.output_box.config(state=tk.DISABLED)

    def run_code(self):
        self.compare_code_string = self.compare_code_box.get("1.0", "end-1c")
        input_string = self.test_case_box.get("1.0", "end-1c")
        out_tmp = self.execute_runner(self.compare_code_string,input_string)
        self.output_box.config(state=tk.NORMAL)

        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, out_tmp)
        self.output_box.config(state=tk.DISABLED)


    def validate_integer(self, new_value):
        if new_value == "":
            return True
        try:
            int(new_value)
            return True
        except ValueError:
            return False

    def validate_prompt(self):
        prompt = self.generator_box.get("1.0", "end-1c")
        if not prompt.strip():
            messagebox.showwarning("Input Error", "Prompt cannot be empty.")
            return
        self.generate_with_ai(prompt)

    def generate_with_ai(self, prompt):
        try:
            self.ai_gen_code_string =  self.model.send_prompt(prompt)
            self.gen_code_string = self.ai_gen_code_string
            self.generator_box.delete(1.0, tk.END)
            self.generator_box.insert(tk.END, self.gen_code_string)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate code: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.window.mainloop()
