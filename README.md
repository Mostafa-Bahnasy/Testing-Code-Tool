# Code Comparison and Test Generation Tool

## Overview

The **Code Comparison and Test Generation Tool** is an innovative application designed to facilitate the comparison of code snippets and their outputs. This tool enables users to effortlessly input multiple code snippets, execute them, and visually compare the results. Additionally, the application leverages artificial intelligence to assist users in generating tests based on the provided snippets, enhancing productivity and code reliability.

## Key Features

- **Code Snippet Comparison**: Input and compare the outputs of multiple code snippets seamlessly.
- **Automated Test Generation**: Utilize an integrated AI model to generate comprehensive tests based on your code.
- **Intuitive Graphical User Interface**: A user-friendly GUI that simplifies interactions and enhances usability.
- **Standalone Executable**: Easily run the application on your local machine without needing to set up a development environment.

## Demonstration Videos

Explore the functionality of the application through the following demonstration videos:

- **Part 1: Code Input and Comparison**  
  [![Part 1](Project%20Files/AI%20generator%20image.png)](Project%20Files/code%20compare%20tests.mp4)

- **Part 2: Test Generation Process**  
  [![Part 2](Project%20Files/code%20compare%20tests.png)](Project%20Files/manual%20stress%20test.mp4)

- **Part 3: AI-Assisted Test Generation**  
  [![Part 3](Project%20Files/manual%20stress%20test.png)](Project%20Files/AI%20generator%20video.mp4)


## Installation Instructions

To set up the application on your local machine, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mostafa-Bahnasy/Testing-Code-Tool.git
   cd Testing-Code-Tool
   ```

2. **Install Required Dependencies**: Ensure Python is installed on your system, then execute the following command to install the necessary packages:

```bash
pip install -r requirements.txt
```

3. **Run the Application:**: 
- You can launch the application directly using the provided .exe file.


## AI Requirements

To use the AI model in this project, you need to download the Ollama CLI. Follow these steps:

1. Download the Ollama CLI from the following link: [Ollama Download](https://ollama.com/download).

2. Once you have installed the CLI, run the following bash script to start the AI model:
```bash
ollama run phi3.5
```

Make sure you have the necessary permissions to execute the script and that the Ollama CLI is correctly installed on your system.


## Technologies Used
- Python
- Tkinter (for GUI)
- AI Model phi3.5


## Contributing
Contributions to enhance the functionality of this project are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request detailing your changes.
For any issues or feature requests, please open an issue in the repository.

## Troubleshooting
If you encounter issues during installation or usage, please check the following:

- Ensure you have Python and pip installed correctly.
- Check the console for any error messages for guidance.

## Future Improvements
- **Adding automated tests**, allowing users to compare code snippets online by their links on popular platforms such as Codeforces, Atcoder, and others.
- Improving GUI responsiveness.


For further information, feel free to contact me at [mustafaabdallah2003@gmail.com].



