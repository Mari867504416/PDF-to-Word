import streamlit as st
import requests
from docx import Document
from io import BytesIO

st.title("PDF to Word OCR - No Tesseract needed (Cloud)")

api_key = "YOUR_OCR_SPACE_API_KEY"  # Replace with your key

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    st.write("🔄 Uploading PDF to OCR API...")
    
    # Send PDF to OCR.space
    response = requests.post(
        'https://api.ocr.space/parse/image',
        files={"filename": uploaded_file.getvalue()},
        data={"apikey": api_key, "language": "tam+eng", "isOverlayRequired": False},
    )
    
    result = response.json()
    
    if result.get("IsErroredOnProcessing"):
        st.error("OCR API Error: " + result.get("ErrorMessage")[0])
    else:
        parsed_text = ""
        for page in result.get("ParsedResults", []):
            parsed_text += page.get("ParsedText", "") + "\n\n"
        
        st.write("💾 OCR Completed!")
        
        # Save to Word
        doc = Document()
        for line in parsed_text.split("\n"):
            doc.add_paragraph(line)
        
        doc_bytes = BytesIO()
        doc.save(doc_bytes)
        doc_bytes.seek(0)
        
        st.download_button(
            label="Download Word Document",
            data=doc_bytes,
            file_name="output.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        st.text_area("OCR Output Preview", parsed_text, height=400)
