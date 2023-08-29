# gh0stconverter
# Document to Markdown Converter

This script allows you to convert text and images from PDF and DOCX files into Markdown format. The extracted text is converted to Markdown paragraphs, while images are saved separately and linked in the Markdown content.

## Features

- Converts text content from PDF and DOCX files into Markdown format.
- Extracts images from PDF and DOCX files and saves them separately.
- Creates a separate Markdown file containing the converted content and image links.

## Prerequisites

- Python 3.7 or later
- Required Python packages: `pdfplumber`, `python-docx`, `Pillow`

## Usage

1. Install the required Python packages:

   ```bash
   pip install pdfplumber python-docx Pillow

Clone this repository or download the converter.py file.

Open a terminal and navigate to the directory containing the converter.py file.

Run the script:

Copy code
python converter.py
Follow the prompts to provide the path of the file you want to convert.

The script will create a directory with the same name as the input file (without extension) and save the extracted content and images inside it.

The converted Markdown file will be saved in the same directory.

Copy the Markdown content from the generated file and paste it into your preferred Markdown-based note-taking application (e.g., Joplin).

Notes
Make sure the input file is in PDF or DOCX format.
The script is provided as-is and may not handle all edge cases.
It's recommended to create a virtual environment to isolate dependencies if needed.
License
This project is licensed under the MIT License.

vbnet
Copy code

Remember to replace the `LICENSE` link with the actual link to your license file (if you're using one) and add any additional sections or information you think would be helpful for users.
