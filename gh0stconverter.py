import os
import pdfplumber
from docx import Document
from PIL import Image
import io

def pdf_to_markdown(pdf_path, output_dir):
    markdown_content = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            markdown_content += text + '\n\n'
            
            images = page.images
            for img_num, image in enumerate(images, start=1):
                img = pdf.pages[page_num - 1].to_image(resolution=150)
                img_data = img.original
                img_filename = f"{output_dir}/image_{page_num}_{img_num}.png"
                img.save(img_filename)
                markdown_content += f"![Image]({img_filename})\n\n"
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
            img_filename = f"{output_dir}/{os.path.basename(img_part.target_ref)}"
            img.save(img_filename, format="PNG")
            markdown_content += f"![Image]({img_filename})\n\n"
    
    return markdown_content

def convert_to_markdown(input_path):
    _, filename = os.path.split(input_path)
    filename_without_extension, _ = os.path.splitext(filename)
    output_dir = filename_without_extension
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist
    
    markdown_content = ''
    
    _, extension = os.path.splitext(input_path)
    
    if extension == '.pdf':
        markdown_content = pdf_to_markdown(input_path, output_dir)
    elif extension == '.docx':
        markdown_content = docx_to_markdown(input_path, output_dir)
    else:
        return "Unsupported file format."
    
    markdown_file_path = f"{output_dir}/{filename_without_extension}.md"
    with open(markdown_file_path, 'w') as markdown_file:
        markdown_file.write(markdown_content)
        
    return markdown_file_path

if __name__ == "__main__":
    input_path = input("Enter the path of the file to convert: ").strip("'\"")
    
    if not os.path.exists(input_path):
        print("File not found.")
    else:
        input_path = os.path.abspath(input_path)
        markdown_file_path = convert_to_markdown(input_path)
        
        print(f"Conversion complete. Markdown file saved at: {markdown_file_path}")
