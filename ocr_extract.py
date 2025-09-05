import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from docx import Document
from io import BytesIO

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("PDF to Word OCR (Tamil + English)")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    st.write("🔄 Converting PDF to images...")
    
    # Convert PDF bytes to images
    pages = convert_from_bytes(uploaded_file.read(), dpi=300)
    
    st.write("🔍 Running OCR...")
    text_output = ""
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, lang="tam+eng")
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
