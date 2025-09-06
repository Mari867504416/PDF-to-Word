import streamlit as st
import requests

st.set_page_config(page_title="PDF OCR Extractor", layout="wide")

st.title("📄 PDF/Image OCR Extractor (Tamil + English)")

# Upload file
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

# OCR.space API Key (replace with your key)
API_KEY = "YOUR_OCR_SPACE_API_KEY"  # 🔑 Get from https://ocr.space/OCRAPI

if uploaded_file is not None:
    st.info(f"✅ File uploaded: {uploaded_file.name}")

    if st.button("Run OCR"):
        with st.spinner("🔍 Processing OCR..."):
            try:
                # Send file to OCR.space API
                files = {"file": uploaded_file}
                payload = {
                    "apikey": API_KEY,
                    "language": "tam+eng",  # Tamil + English
                    "isOverlayRequired": False
                }

                response = requests.post(
                    "https://api.ocr.space/parse/image",
                    files=files,
                    data=payload
                )

                # Convert response to JSON
                result = response.json()

                # Check for errors
                if result.get("IsErroredOnProcessing"):
                    error_msg = result.get("ErrorMessage")
                    st.error(f"❌ OCR API Error: {error_msg}")
                    st.stop()

                # Extract text
                parsed_text = result["ParsedResults"][0]["ParsedText"]

                st.success("✅ OCR Extraction Completed!")
                st.text_area("📄 Extracted Text:", parsed_text, height=400)

                # Option to download text as .docx
                from docx import Document
                doc = Document()
                doc.add_paragraph(parsed_text)
                output_path = "output.docx"
                doc.save(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇ Download as Word Document",
                        data=f,
                        file_name="extracted_text.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
