import streamlit as st
import requests
import tempfile
import os
from PyPDF2 import PdfReader, PdfWriter

# -------------------------
# Function: Split PDF (max 3 pages each)
# -------------------------
def split_pdf(uploaded_file, pages_per_file=3):
    temp_dir = tempfile.mkdtemp()
    reader = PdfReader(uploaded_file)
    total_pages = len(reader.pages)
    parts = []

    for i in range(0, total_pages, pages_per_file):
        writer = PdfWriter()
        for j in range(i, min(i + pages_per_file, total_pages)):
            writer.add_page(reader.pages[j])

        part_path = os.path.join(temp_dir, f"part_{i//pages_per_file+1}.pdf")
        with open(part_path, "wb") as f:
            writer.write(f)
        parts.append(part_path)

    return parts

# -------------------------
# Function: OCR with OCR.space API
# -------------------------
def ocr_space_file(filename, api_key, language="eng"):
    payload = {
        "apikey": api_key,
        "language": language,
        "isOverlayRequired": False,
        "OCREngine": 2,
        "filetype": "PDF"
    }
    with open(filename, "rb") as f:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": f},
            data=payload
        )
    try:
        return response.json()
    except:
        return {"IsErroredOnProcessing": True, "ErrorMessage": ["Invalid JSON response"]}

# -------------------------
# Streamlit UI
# -------------------------
st.title("📄 PDF to Text (OCR.space API - 3 page limit per file)")

api_key = st.text_input("🔑 Enter your OCR.space API Key:", type="password")
uploaded_file = st.file_uploader("📤 Upload PDF", type=["pdf"])

if uploaded_file and api_key:
    st.info("📑 Splitting PDF into 3-page chunks...")
    pdf_parts = split_pdf(uploaded_file)

    all_text = ""
    for idx, part in enumerate(pdf_parts, start=1):
        st.write(f"⏳ Processing Part {idx}...")
        result = ocr_space_file(part, api_key, language="eng")

        if result.get("IsErroredOnProcessing"):
            st.error(f"❌ OCR API Error (Part {idx}): {result.get('ErrorMessage')}")
        else:
            parsed_results = result.get("ParsedResults", [])
            for res in parsed_results:
                all_text += res.get("ParsedText", "") + "\n"

    if all_text.strip():
        st.success("✅ OCR Completed Successfully!")
        st.text_area("📜 Extracted Text:", all_text, height=400)

        # Download as .txt
        st.download_button(
            label="💾 Download as TXT",
            data=all_text,
            file_name="ocr_output.txt",
            mime="text/plain"
        )
