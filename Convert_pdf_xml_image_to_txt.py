

import tkinter as tk
from tkinter import filedialog
import magic
from email import message_from_file
import string
import docx2txt
from bs4 import BeautifulSoup


def extract_text(file_path):
    file_type = magic.from_file(file_path, mime=True)

    if file_type == 'text/plain':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    if file_type == 'application/msword' or file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return docx2txt.process(file_path)

    if file_type == 'message/rfc822':
        with open(file_path, 'r', encoding='utf-8') as file:
            msg = message_from_file(file)
            return msg.get_payload()

    if file_type == 'application/pdf':
        return textract.process(file_path, method='pdfminer').decode('utf-8')

    if file_type == 'text/html' or file_type == 'application/xhtml+xml' or file_type == 'text/xml':
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            return soup.get_text()

    return ''


def select_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf"), ("Word Documents", "*.doc *.docx"), ("Text Files", "*.txt"), ("EML Files", "*.eml"), ("HTML Files", "*.html"), ("XML Files", "*.xml"), ("Image Files", "*.jpg *.jpeg *.png *.bmp")])
    extracted_text = ""  # Variable to store the combined extracted text

    for file in files:
        extracted_text += extract_text(file)

    write_to_file(extracted_text)  # Write the combined text to a file


def format_text_file(text):
    formatted_text = text.replace(' ', '\n')  # Replace spaces with line breaks
    formatted_text = '\n'.join(line.strip() for line in formatted_text.split('\n') if line.strip() and len(line.strip()) >= 2 and any(char.isalpha() for char in line))

    # Remove punctuation characters
    translator = str.maketrans('', '', string.punctuation)
    formatted_text = formatted_text.translate(translator)

    return formatted_text


def write_to_file(text):
    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if output_file_path:
        formatted_text = format_text_file(text)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_text)
        print("Text written to file:", output_file_path)


root = tk.Tk()
root.title("Document Text Extractor")  # Set the title of the main window

files_button = tk.Button(root, text="Select Files", command=select_files)
files_button.pack()

root.mainloop()
