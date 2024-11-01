import tkinter as tk
from functools import partial
from tkinter import ttk
import CodeExecuter as CE
import ReadFile as CR
from tkinter import messagebox

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Testing Tool")
        self.window.geometry("1000x1000")

        # Create Tabs
        self.tab_control = ttk.Notebook(self.window)

        # Create the "Stress" tab
        self.stress_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.stress_tab, text="Stress")
        self.tab_control.add(ttk.Frame(self.tab_control), text="Compare")
        self.tab_control.add(ttk.Frame(self.tab_control), text="Auto")

        self.tab_control.pack(expand=1, fill="both")
        # Layout for the "Stress" tab
        self.create_stress_tab()

        self.code_execute = CE.CodeExecutor()
        self.code_reader = CR.CodeFileReader()

        self.code_1_string = ""
        self.code_2_string = ""
        self.gen_code_string = ""
        self.test_loop = 0

    def init_test_stress(self):
        self.test_loop = int(self.stress_test_num_entry.get())
        # print("init",self.test_loop)

        if self.code_1_string != self.input_code_1.get("1.0", "end-1c"):
            self.code_1_string = self.input_code_1.get("1.0", "end-1c")

        if self.code_2_string != self.input_code_2.get("1.0", "end-1c"):
            self.code_2_string = self.input_code_2.get("1.0", "end-1c")

        if self.gen_code_string != self.generator_box.get("1.0", "end-1c"):
            self.gen_code_string = self.generator_box.get("1.0", "end-1c")

        self.stress_test_method()

    def stress_test_method(self):
        # print("go",self.test_loop)
        self.test_loop = self.test_loop - 1
        if self.test_loop<0:
            self.test_loop = 0
            messagebox.showinfo("Tests","Test Cases Ended!")
            return

        input_test = self.execute_runner(self.gen_code_string,"")
        output_1 = self.execute_runner(self.code_1_string,input_test)
        output_2 = self.execute_runner(self.code_2_string,input_test)

        self.test_case_input_box.delete(1.0,tk.END)
        self.test_case_input_box.insert(tk.END,input_test)

        if self.test_show_radio_var.get() == "A": # all
            self.output_code_1.delete(1.0,tk.END)
            self.output_code_1.insert(tk.END,output_1)
            self.output_code_2.delete(1.0,tk.END)
            self.output_code_2.insert(tk.END,output_2)

        elif self.test_show_radio_var.get() == "B": #wrong
            if self.compare_strings(output_2,output_1):
                self.output_code_1.delete(1.0,tk.END)
                self.output_code_2.delete(1.0,tk.END)
                self.output_code_1.insert(tk.END,"Passed!")
                self.output_code_2.insert(tk.END,"Passed!")
            else:
                self.output_code_1.delete(1.0,tk.END)
                self.output_code_1.insert(tk.END,output_1)
                self.output_code_2.delete(1.0,tk.END)
                self.output_code_2.insert(tk.END,output_2)

        else:
            print("radio button show test err")

    def compare_strings(self, str1, str2):
        # Remove whitespace and trailing newlines, then compare
        cleaned_str1 = ''.join(str1.split())
        cleaned_str2 = ''.join(str2.split())
        return cleaned_str1 == cleaned_str2

    def execute_runner(self,code:str,inp:str):
        self.code_execute.add_code(code,inp)
        self.code_execute.run()
        return self.code_execute.get_output()

    def on_click_upload_code(self, flag):
        self.code_reader.navigate_file()
        self.code_reader.read_code()
        if flag == 1:
            self.code_1_string = self.code_reader.get_code_string()
            self.input_code_1.delete(1.0,tk.END)
            self.input_code_1.insert(tk.END,self.code_1_string)
        elif flag == 2:
            self.code_2_string = self.code_reader.get_code_string()
            self.input_code_2.delete(1.0,tk.END)
            self.input_code_2.insert(tk.END,self.code_2_string)
        elif flag == 3:
            self.gen_code_string = self.code_reader.get_code_string()
            self.generator_box.delete(1.0,tk.END)
            self.generator_box.insert(tk.END,self.gen_code_string)

    def generator_rad_selected(self):
        #print(self.generate_radio_var.get())
        if self.generate_radio_var.get()=="B":
            self.generated_ai_code_butt.destroy()
        elif self.generate_radio_var.get() =="A":
            self.generated_ai_code_butt = tk.Button(self.bottom_frame, text="See generated code")
            self.generated_ai_code_butt.grid(row=0, column=0, padx=5)
        else:
            print("ERRor")

    def on_click_set_gen(self):
        if self.generate_radio_var.get()=="B":
            self.on_click_upload_code(3)
        elif self.generate_radio_var.get()=="A":
            self.validate_prompt()

    def create_stress_tab(self):
        # Left section (for menu, radio buttons, text boxes, and buttons)
        self.left_frame = tk.Frame(self.stress_tab)
        self.left_frame.grid(row=0, column=0, sticky="n")

        # Label and larger Text box with copy/paste capability
        tk.Label(self.left_frame, text="Input Code_1:").grid(row=1, column=0, sticky="w")
        self.input_code_1 = tk.Text(self.left_frame, width=60, height=10)
        self.input_code_1.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.upload_code_1_butt = tk.Button(self.left_frame, text="Upload code_1",command=partial(self.on_click_upload_code,1))
        self.upload_code_1_butt.grid(row=2, column=10, padx=5, pady=5)

        tk.Label(self.left_frame, text="Input Code_2:").grid(row=3, column=0, sticky="w")
        self.input_code_2 = tk.Text(self.left_frame, width=60, height=10)
        self.input_code_2.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.upload_code_2_butt = tk.Button(self.left_frame, text="Upload code_2",command=partial(self.on_click_upload_code,2))
        self.upload_code_2_butt.grid(row=4, column=10, padx=5, pady=5)

        # Label and three radio buttons below the first text box
        tk.Label(self.left_frame, text="Options:").grid(row=5, column=0, sticky="w")
        self.radio_frame2 = tk.Frame(self.left_frame)
        self.radio_frame2.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.generate_radio_var = tk.StringVar(value="A")
        self.ai_rad_butt = tk.Radiobutton(self.radio_frame2, text="Generate With AI", variable=self.generate_radio_var, value="A",command=self.generator_rad_selected).pack(anchor="w")
        self.gen_rad_butt= tk.Radiobutton(self.radio_frame2, text="Write your Generator", variable=self.generate_radio_var, value="B",command=self.generator_rad_selected).pack(anchor="w")

        # Label and second larger text box
        tk.Label(self.left_frame, text="Generator/Prompt:").grid(row=8, column=0, sticky="w")
        self.generator_box = tk.Text(self.left_frame, width=60, height=10)
        self.generator_box.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.upload_gen_butt = tk.Button(self.left_frame, text="Set Generator",command=self.on_click_set_gen)
        self.upload_gen_butt.grid(row=9, column=10, padx=5, pady=5)

        # Label and three objects [Button, Menu, Button]
        tk.Label(self.left_frame, text="Actions:").grid(row=10, column=0, sticky="w")
        self.bottom_frame = tk.Frame(self.left_frame)
        self.bottom_frame.grid(row=11, column=0, padx=5, pady=5, sticky="w")

        self.generated_ai_code_butt = tk.Button(self.bottom_frame, text="See generated code")
        self.generated_ai_code_butt.grid(row=0, column=0, padx=5)

        self.test_stress_butt = tk.Button(self.bottom_frame, text="Test",command=self.init_test_stress)
        self.test_stress_butt.grid(row=0, column=1, padx=5)

        # Numeric entry for integers in range(1, 10000)
        validate_integer = self.window.register(self.validate_integer)
        self.stress_test_num_entry = tk.Entry(self.bottom_frame, validate="key", validatecommand=(validate_integer, '%P'))
        self.stress_test_num_entry.grid(row=0, column=2, padx=5)  # Add the numeric entry next to the test_stress_butt

        # Right section (for three larger text boxes and buttons beside them)
        self.right_frame = tk.Frame(self.stress_tab)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # First right text box and button
        tk.Label(self.right_frame, text="Test Case:").grid(row=0, column=0, sticky="w")
        self.test_case_input_box = tk.Text(self.right_frame, width=40, height=10)
        self.test_case_input_box.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Second right text box and button
        tk.Label(self.right_frame, text="Output of Code_1").grid(row=2, column=0, sticky="w")
        self.output_code_1 = tk.Text(self.right_frame, width=40, height=10)
        self.output_code_1.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Third right text box and button
        tk.Label(self.right_frame, text="Output of Code_2:").grid(row=4, column=0, sticky="w")
        self.output_code_2 = tk.Text(self.right_frame, width=40, height=10)
        self.output_code_2.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.next_test_butt = tk.Button(self.right_frame, text="Next Test",command=self.stress_test_method)
        self.next_test_butt.grid(row=6, column=0, padx=5, pady=5)

        # Label and two radio buttons below the first text box
        self.radio_frame3 = tk.Frame(self.right_frame)
        self.radio_frame3.grid(row=11, column=0, padx=5, pady=5, sticky="w")
        self.test_show_radio_var = tk.StringVar(value="A")
        tk.Radiobutton(self.radio_frame3, text="Show All", variable=self.test_show_radio_var, value="A").pack(anchor="w")
        tk.Radiobutton(self.radio_frame3, text="Show WA", variable=self.test_show_radio_var, value="B").pack(anchor="w")

    def validate_integer(self, new_value):
        """Validation function to check if the new value is an integer in range(1, 10000)."""
        if new_value == "":  # Allow empty input
            return True
        try:
            value = int(new_value)  # Try converting to integer
            return 1 <= value <= 5000  # Check if value is in range
        except ValueError:
            return False  # Not a valid integer

    def run(self):
        self.window.mainloop()

    def validate_prompt(self):
        print("in validate")


# Create and run the application
if __name__ == "__main__":
    app = App()
    app.run()
