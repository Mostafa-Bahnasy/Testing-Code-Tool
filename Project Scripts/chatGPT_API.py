import subprocess
import re

#
# Write Python code to generate one test case for the following input format:
#
# Input Format:
# - The first line contains an integer `n` (1 ≤ n ≤ 100), representing the number of items.
# - The next line contains `n` integers, each between -1000 and 1000, representing item values.
#
# Constraints:
# - `n` ranges from 1 to 100.
# - Each integer is between -1000 and 1000.
#
# Generate edge cases as well, such as:
# - Minimum values (e.g., `n = 1` with the smallest possible integer).
# - Maximum values (e.g., `n = 100` with the largest integers).
# - Cases with all positive values, all negative values, and a mix of both.
#
# **Only provide the Python code without any additional explanation.**
#

# Write Python code to generate one test case with the following format:
#
# Input Format:
# - The first line contains two integers `n` and `m` (1 ≤ n, m ≤ 100), representing the number of rows and columns.
# - The next `n` lines each contain `m` integers, each between -1000 and 1000.
#
# Constraints:
# - `n` and `m` range from 1 to 100.
# - Each integer is between -1000 and 1000.
#
# Include edge cases like:
# - Minimum values (e.g., `n = 1` and `m = 1` with the smallest integer).
# - Maximum values (e.g., `n = 100` and `m = 100` with the largest integers).
# - Cases with all positive values, all negative values, and a mix of both.
#
# **Only provide the Python code without additional explanation.**
#


# Write Python code to generate one test case for the following input format:
#
# Input Format:
# - The first line contains an integer `n` (1 ≤ n ≤ 100), the length of the string.
# - The second line contains a string of length `n`, consisting of uppercase English letters (A-Z).
#
# Constraints:
# - `n` ranges from 1 to 100.
# - The string should include edge cases like:
#   - All identical characters (e.g., "AAAA").
#   - Alternating characters (e.g., "ABABAB...").
#   - Completely random characters.
#
# **Only provide the Python code without additional explanation.**
#


# Write Python code to generate one test case for the following input format:
#
# Input Format:
# - The first line contains two integers `n` and `m` (1 ≤ n ≤ 50, 0 ≤ m ≤ n*(n-1)/2), representing the number of nodes and edges.
# - The next `m` lines each contain two integers `u` and `v` (1 ≤ u, v ≤ n), representing an undirected edge between nodes `u` and `v`.
#
# Constraints:
# - `n` ranges from 1 to 50, and `m` is a valid number of edges for `n` nodes.
# - Include cases like:
#   - Minimum edge case (e.g., `n = 1`, `m = 0`).
#   - Maximum edge case (e.g., complete graph with `m = n*(n-1)/2` edges).
#   - Disconnected graph with `m = 0`.
#
# **Only provide the Python code without additional explanation.**
#


# Write Python code to generate one test case with the following format:
#
# Input Format:
# - The first line contains an integer `n` (1 ≤ n ≤ 200), the number of random values.
# - The next line contains `n` integers between 1 and 10,000.
#
# Constraints:
# - `n` ranges from 1 to 200.
# - Include cases such as:
#   - Minimum values (e.g., `n = 1` and value = 1).
#   - Maximum values (e.g., `n = 200` with all values at 10,000).
#   - Random distribution within the range.
#
# **Only provide the Python code without additional explanation.**


class Phi3_5Model:
    def __init__(self):
        # Command to run the phi3.5 model
        self.command = ["ollama", "run", "phi3.5"]

    def format_prompt(self,prompt):
        return "Write Python code to generate one test case for the following input format:\n"+prompt+"\nOnly provide the Python code without additional explanation or text."
    def extract_python_substring(self,text: str) -> str:

        pattern = r'\{```Python,(.*?)```}'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            # Return the captured group, stripping any leading/trailing whitespace
            return match.group(1).strip()
        else:
            return ""
    def send_prompt(self, prompt: str) -> str:
        prompt = self.format_prompt(prompt)
        print(prompt)
        process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Communicate with the process, sending the prompt and capturing output and errors
        output, error = process.communicate(input=prompt)

        # Check for errors and return the appropriate response
        if error:
            return f"Error: {error}"


        return self.extract_python_substring(output)
