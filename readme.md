# 📄 Extract Text from PDFs using LLaMA 🦙

This README provides detailed instructions on how to use the program that extracts text from PDF files and retrieves information using the LLaMA 3.1 model.

## 🚀 Usage

To use this program, follow the steps below:

1. **Run the Program:**
   - Open your terminal or command prompt.
   - Navigate to the directory where you have the program files.
   - Run the program by executing the following command:
     ```bash
     python main.py --directory <directory>
     ```
   - Replace `<directory>` with the path to the directory containing the PDF files you want to process.

2. **Customize Output:**
   - You can customize the program's output by modifying the configuration file (`config.json` or similar). This file allows you to specify parameters such as the output format, the level of detail, and any other settings related to how the extracted information is presented.

### ✨ Features

- **📄 PDF Text Extraction:** This program extracts text from PDF files, making it easier to process large volumes of documents.
- **🔍 LLaMA Model Integration:** The extracted text is processed using the LLaMA 3.1 model, which enables advanced information retrieval and analysis.
- **🛠 Customizable Output:** The program's output can be tailored to meet specific needs by adjusting settings in the configuration file.

### 📋 Requirements

Ensure that you have the following software and dependencies installed before running the program:

- **🐍 Python 3.x:** Make sure you have Python 3.x installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
- **📦 OLLaMA and LLaMA 3.1 Model:** The program relies on the OLLaMA platform and the LLaMA 3.1 model for text processing. Ensure these are installed and properly configured.

### 📥 Installation

Follow these steps to install the program and its dependencies:

1. **Clone the Repository:**
   - Use the following command to clone the repository to your local machine:
     ```bash
     git clone <repository_url>
     ```
   - Replace `<repository_url>` with the URL of the repository where the program's code is hosted.

2. **Install Dependencies:**
   - Navigate to the cloned repository's directory:
     ```bash
     cd <repository_directory>
     ```
   - Replace `<repository_directory>` with the path to the directory where the repository was cloned.
   - Install the required Python packages by running:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run OLLaMA:**
   - Ensure that the OLLaMA platform is running with the LLaMA 3.1 model installed. Follow the platform's documentation to start the service if it's not already running.

4. **Run the Program:**
   - Execute the program by running the following command:
     ```bash
     python main.py --directory <directory>
     ```
   - Replace `<directory>` with the path to the directory containing the PDF files you want to process.

### 🛠 Configuration

You can modify the program's behavior by editing the configuration file (e.g., `config.json`). The configuration file allows you to set various parameters, such as:

- **Output Format:** Choose between different output formats like JSON, plain text, or CSV.
- **Detail Level:** Adjust the level of detail in the output (e.g., summary vs. full text).
- **Model Settings:** Customize settings related to the LLaMA model, such as temperature, max tokens, etc.

### 💻 Example

Here’s an example of how to run the program:

```bash
python main.py --directory ./pdfs
```

In this example, the program will process all PDF files located in the `./pdfs` directory and output the results based on the configured settings.

### ❓ Troubleshooting

- **Missing Dependencies:** If you encounter errors related to missing packages, ensure all dependencies are installed correctly using `pip install -r requirements.txt`.
- **Model Not Found:** If the program fails to locate the LLaMA model, verify that OLLaMA is running and properly configured.

