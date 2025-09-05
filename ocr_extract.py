import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from docx import Document
from io import BytesIO

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("PDF to Word OCR (Tamil + English) - No Poppler needed")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    st.write("🔄 Converting PDF to images using PyMuPDF...")
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    images = []
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    
    st.write("🔍 Running OCR...")
    text_output = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img, lang="tam+eng")
        text_output += f"\n\n--- Page {i+1} ---\n\n{text}"
    
    # Save to Word in memory
    doc = Document()
    for line in text_output.split('\n'):
        doc.add_paragraph(line)
    doc_bytes = BytesIO()
    doc.save(doc_bytes)
    doc_bytes.seek(0)
    
    st.write("💾 OCR Completed!")
    st.download_button(
        label="Download Word Document",
        data=doc_bytes,
        file_name="output.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    
    st.text_area("OCR Output Preview", text_output, height=400)
