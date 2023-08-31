import os
import pdfplumber
from docx import Document
from PIL import Image
import io
from pdf2image import convert_from_path


def sanitize_filename(filename):
    return ''.join(c if c.isalnum() else '_' for c in filename)

def pdf_to_markdown(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    img_subdir = os.path.join(output_dir, "images")
    os.makedirs(img_subdir, exist_ok=True)
    markdown_content = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            img = page.to_image()
            img_path = os.path.join(img_subdir, f"image_{page_number+1}.png")
            img.save(img_path)
            markdown_content += f"![Image {page_number+1}]({img_path})\n"

    return markdown_content

def docx_to_markdown(docx_path, output_dir):
    doc = Document(docx_path)
    markdown_content = ''
    for para in doc.paragraphs:
        markdown_content += para.text + '\n\n'

    for rel in doc.part.rels:
        if "image" in doc.part.rels[rel].target_ref:
            img_part = doc.part.related_parts[doc.part.rels[rel].target_ref]
            img_data = img_part.blob
            img = Image.open(io.BytesIO(img_data))
            img_filename = os.path.join(output_dir, os.path.basename(img_part.target_ref))
            img.save(img_filename, format="PNG")
            markdown_content += f"![Image]({img_filename})\n\n"

    return markdown_content

def convert_to_markdown(file_path):
    if os.path.isfile(file_path):
        markdown_content = pdf_to_markdown(file_path, "markdowns")
        output_file_path = os.path.join("markdowns", os.path.basename(file_path) + ".md")
        with open(output_file_path, "w", encoding="utf-8") as markdown_file:
            markdown_file.write(markdown_content)
    elif os.path.isdir(file_path):
        for root, _, files in os.walk(file_path):
            for file in files:
                if file.lower().endswith(('.pdf', '.docx')):
                    file_path = os.path.join(root, file)
                    convert_to_markdown(file_path)
    else:
        print("Invalid file or directory path.")



if __name__ == "__main__":
    print(r"""


             ('-. .-.            .-')    .-') _                              .-') _      (`-.      ('-.  _  .-')   .-') _     ('-.  _  .-')   
            ( OO )  /           ( OO ). (  OO) )                            ( OO ) )   _(OO  )_  _(  OO)( \( -O ) (  OO) )  _(  OO)( \( -O )  
  ,----.    ,--. ,--.  .----.  (_)---\_)/     '._  .-----.  .-'),-----. ,--./ ,--,',--(_/   ,. \(,------.,------. /     '._(,------.,------.  
 '  .-./-') |  | |  | /  ..  \ /    _ | |'--...__)'  .--./ ( OO'  .-.  '|   \ |  |\\   \   /(__/ |  .---'|   /`. '|'--...__)|  .---'|   /`. ' 
 |  |_( O- )|   .|  |.  /  \  .\  :` `. '--.  .--'|  |('-. /   |  | |  ||    \|  | )\   \ /   /  |  |    |  /  | |'--.  .--'|  |    |  /  | | 
 |  | .--, \|       ||  |  '  | '..`''.)   |  |  /_) |OO  )\_) |  |\|  ||  .     |/  \   '   /, (|  '--. |  |_.' |   |  |  (|  '--. |  |_.' | 
(|  | '. (_/|  .-.  |'  \  /  '.-._)   \   |  |  ||  |`-'|   \ |  | |  ||  |\    |    \     /__) |  .--' |  .  '.'   |  |   |  .--' |  .  '.' 
 |  '--'  | |  | |  | \  `'  / \       /   |  | (_'  '--'\    `'  '-'  '|  | \   |     \   /     |  `---.|  |\  \    |  |   |  `---.|  |\  \  
  `------'  `--' `--'  `---''   `-----'    `--'    `-----'      `-----' `--'  `--'      `-'      `------'`--' '--'   `--'   `------'`--' '--' 


    """)
    input_path = input("Enter the path of the file or directory to convert: ")
    result = convert_to_markdown(input_path)
    print(result)
