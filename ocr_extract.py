import streamlit as st
import requests
from docx import Document

# 🔑 Your OCR.space API key
API_KEY = "K89663616288957"

st.title("📄 PDF to Word (OCR.space API)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    st.info("⏳ Uploading file to OCR.space and extracting text...")

    url = "https://api.ocr.space/parse/image"

    payload = {
        "apikey": API_KEY,
        "language": "eng",   # Tamil OCR not stable → use "eng" first
        "isOverlayRequired": False,
        "filetype": "pdf"    # ✅ FIX → explicitly tell API it's a PDF
    }

    # pass correct file object with filename
    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue())
    }

    response = requests.post(url, data=payload, files=files)

    try:
        result = response.json()
    except Exception as e:
        st.error(f"❌ Response parse error: {e}")
        st.stop()

    # Error handling
    if isinstance(result, dict) and result.get("IsErroredOnProcessing"):
        st.error(f"❌ OCR API Error: {result.get('ErrorMessage')}")
        st.stop()

    # Extract text
    text = ""
    if "ParsedResults" in result:
        for item in result["ParsedResults"]:
            text += item.get("ParsedText", "") + "\n"

    if not text.strip():
        st.warning("⚠️ No text extracted. Try with English docs or use Tesseract locally.")
    else:
        st.success("✅ OCR extraction done!")

        # Save to Word
        doc = Document()
        doc.add_paragraph(text)
        output_path = "output.docx"
        doc.save(output_path)

        with open(output_path, "rb") as f:
            st.download_button("📥 Download Word File", f, file_name="output.docx")
