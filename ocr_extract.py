import streamlit as st
import requests
from docx import Document
from io import BytesIO

st.set_page_config(page_title="PDF to Word OCR", layout="wide")
st.title("PDF to Word OCR (Tamil + English) - Cloud Friendly")

# Replace with your OCR.space API Key
api_key = "YOUR_OCR_SPACE_API_KEY"

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    st.write("🔄 Uploading PDF to OCR API...")

    try:
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={"filename": uploaded_file.getvalue()},
            data={"apikey": api_key, "language": "tam+eng", "isOverlayRequired": False},
            timeout=120  # increase if PDF is large
        )
    except requests.exceptions.RequestException as e:
        st.error(f"Network/API error: {e}")
        st.stop()

    # Parse response
    try:
        result = response.json()
    except ValueError:
        st.error("OCR API did not return valid JSON.")
        st.stop()

    # Check for API errors
    if result.get("IsErroredOnProcessing"):
        error_msg = result.get("ErrorMessage")
        st.error(f"OCR API Error: {error_msg}")
        st.stop()

    # Extract text
    parsed_text = ""
    for page in result.get("ParsedResults", []):
        parsed_text += page.get("ParsedText", "") + "\n\n"

    if not parsed_text.strip():
        st.warning("No text detected in the PDF.")
        st.stop()

    st.write("💾 OCR Completed!")

    # Save to Word document in memory
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
