import tkinter as tk
from functools import partial
from tkinter import ttk
import CodeExecuter as CE
import ReadFile as CR
from tkinter import messagebox
import AiBot as MG

class App:
    def __init__(self):
        self.compare_frame = None
        self.window = tk.Tk()
        self.window.title("Testing Tool")
        self.window.geometry("1000x1000")
        self.window.configure(bg="#2E2E2E")  # Dark background for the main window

        self.model = MG.OllamaChat()

        # Create Tabs
        self.tab_control = ttk.Notebook(self.window)

        # Create the "Stress" tab
        self.stress_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.stress_tab, text="Stress Testing")

        # Create the "Compare" tab
        self.compare_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.compare_tab, text="Compare Outputs")

        # Create the "about" tab
        self.about_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.about_tab, text="About")

        self.tab_control.pack(expand=1, fill="both")

        # Layout for the "Stress" tab
        self.create_stress_tab()

        # Layout for the "Compare" tab
        self.create_compare_tab()
        self.create_about_tab()  # Add About tab
        self.change_theme_mode('#FFFAFA','#D3D3D3','#000000')

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
    def create_about_tab(self):
        about_text = """

    # Code Stress Testing and Comparison Tool


    
    ## Overview
    This tool is designed for stress testing and comparing code snippets. It enables users to upload code, 
    generate test cases, and compare outputs. Additionally, you can leverage AI to generate test cases efficiently.
    
    
    **Developer**: Mustafa Bahnasy  
    **Version**: 1.0  
    
    
    
    ## Using the AI Tool Effectively
    The AI generation feature allows you to create prompts in the designated "Generator" block.
    This project utilizes the lightweight phi3.5 model. Here are some examples of effective prompt structures:
    
    
    
    ### Prompt Examples
    
    1. **Task**: "Enter an integer N, followed by N space-separated integers."
       - **Effective Prompt**:
         ```
         N (1 < N < 100)
         A[i] (1 < A[i] < 100), where A is an array of size N.
         ```
    
    
    2. **Task**: "Enter a grid of size N x M."
       - **Effective Prompt**:
         ```
         N, M (1 < N < 100, 1 < M < 1000), two space-separated integers
         A[i][j] (1 < A[i][j] < 10), where A is a grid of size N x M.
         ```
    
    You can modify the code generated by the AI to suit your specific requirements. 
    Additionally, multiple prompts can be submitted, as the tool runs locally on your device.
    
    
    
    ## Important Notes
    - **Performance Considerations**: The performance of the AI model may vary based on the device used,
        as it relies on your local resources.
        
    - **Stress Testing**: In the stress test section, you can provide a single test generator code and adjust
        the number of test cases directly in the GUI.
        
    - **Feedback**: If you encounter any issues or have suggestions, please feel free to reach out via email
        at mustafaabdallah2003@gmail.com.
    

            """

        # Frame for About text and scrollbar
        frame = tk.Frame(self.about_tab)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Scrollable Text widget
        text_widget = tk.Text(frame, wrap=tk.WORD)
        text_widget.insert(tk.END, about_text)
        text_widget.config(state=tk.DISABLED)  # Make text read-only
        text_widget.pack(side=tk.LEFT, expand=True, fill="both")

        text_widget.tag_configure("red", foreground="red")
        text_widget.tag_configure("blue", foreground="blue")
        text_widget.tag_configure("green", foreground="green")
        text_widget.tag_configure("purple", foreground="purple")
        # Scrollbar
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        text_widget.config(bg="#E6E6F0",fg="#000080")
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

    def change_theme_mode(self, back: str,back2:str, txt: str):

        self.input_code_1.config(bg=back, fg=txt)
        self.upload_code_1_butt.config(bg=back2, fg=txt)
        self.input_code_2.config(bg=back, fg=txt)
        self.upload_code_2_butt.config(bg=back2, fg=txt)
        self.generator_box.config(bg=back, fg=txt)
        self.upload_gen_butt.config(bg=back2, fg=txt)
        self.stress_test_num_entry.config(bg=back, fg=txt)
        self.test_stress_butt.config(bg=back2, fg=txt)
        self.test_case_input_box.config(bg=back, fg=txt)
        self.output_code_1.config(bg=back, fg=txt)
        self.output_code_2.config(bg=back, fg=txt)
        self.next_test_but.config(bg=back2, fg=txt)
        # Change color for widgets in create_compare_tab
        self.compare_code_box.config(bg=back, fg=txt)
        self.load_code_button.config(bg=back2, fg=txt)
        self.run_code_button.config(bg=back2, fg=txt)
        self.test_case_box.config(bg=back, fg=txt)
        self.correct_output_box.config(bg=back, fg=txt)
        self.output_box.config(bg=back, fg=txt)
        # Set colors for text widgets
        self.input_code_1.config(bg=back, fg=txt)
        self.input_code_2.config(bg=back, fg=txt)
        self.generator_box.config(bg=back, fg=txt)
        self.test_case_input_box.config(bg=back, fg=txt, state="normal")
        self.output_code_1.config(bg=back, fg=txt, state="normal")
        self.output_code_2.config(bg=back, fg=txt, state="normal")

        # Set colors for buttons
        for button in [self.upload_code_1_butt, self.upload_code_2_butt, self.upload_gen_butt, self.test_stress_butt, self.next_test_but]:
            button.config(bg=back2, fg=txt)

        # Set colors for entries
        self.stress_test_num_entry.config(bg=back, fg=txt)


        # Re-disable text widgets if needed
        self.test_case_input_box.config(state=tk.DISABLED)
        self.output_code_1.config(state=tk.DISABLED)
        self.output_code_2.config(state=tk.DISABLED)



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
