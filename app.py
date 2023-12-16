from flask import Flask, render_template, request, send_file, send_from_directory
from PyPDF2 import PdfWriter, PdfReader
from docx import Document
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename
import pytesseract
import os
import zipfile
from PIL import Image
import io


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    action = request.form.get('action')
    if uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

        if action == 'convert_to_pdf':
            pdf_file_path = convert_jpeg_to_pdf(file_path)
            return send_file(pdf_file_path, as_attachment=True)
        elif action == 'compress':
            return compress_pdf(file_path)
        elif action == 'convert':
            return convert_to_docx_with_ocr(file_path)
        elif action == 'convert_to_jpeg':
            return convert_pdf_to_jpeg(file_path)

    return 'Error'

def compress_pdf(file_path):
    output = PdfWriter()
    reader = PdfReader(file_path)

    for page in reader.pages:
        output.add_page(page)

    compressed_file_path = 'compressed_' + os.path.basename(file_path)
    compressed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], compressed_file_path)
    with open(compressed_file_path, 'wb') as f:
        output.write(f)

    return send_file(compressed_file_path, as_attachment=True)

def convert_jpeg_to_pdf(file_path):
    image = Image.open(file_path)
    pdf_path = os.path.splitext(file_path)[0] + '.pdf'

    # Если изображение не в формате RGB, конвертируем его
    if image.mode != 'RGB':
        image = image.convert('RGB')

    image.save(pdf_path)

    return pdf_path


def convert_to_docx_with_ocr(file_path):
    text = convert_pdf_to_text(file_path)
    doc = Document()
    doc.add_paragraph(text)
    docx_file_path = os.path.splitext(file_path)[0] + '.docx'
    doc.save(docx_file_path)

    return send_file(docx_file_path, as_attachment=True)

def convert_pdf_to_text(file_path):
    images = convert_from_path(file_path)
    text = ""

    for image in images:
        text += pytesseract.image_to_string(image, lang='rus+eng')

    return text

def convert_pdf_to_jpeg(file_path):
    images = convert_from_path(file_path)
    image_folder = os.path.splitext(file_path)[0]
    os.makedirs(image_folder, exist_ok=True)

    for i, image in enumerate(images):
        image_filename = f'page_{i+1}.jpeg'
        image_path = os.path.join(image_folder, image_filename)
        image.save(image_path, 'JPEG')

    zip_filename = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(image_folder) + '.zip')
    with zipfile.ZipFile(zip_filename, 'w') as img_zip:
        for image_file in os.listdir(image_folder):
            img_zip.write(os.path.join(image_folder, image_file), arcname=image_file)

    for image_file in os.listdir(image_folder):
        os.remove(os.path.join(image_folder, image_file))
    os.rmdir(image_folder)

    return send_file(zip_filename, as_attachment=True, download_name=os.path.basename(zip_filename))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
