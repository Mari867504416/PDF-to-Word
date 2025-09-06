import streamlit as st
import requests

# 🔑 உங்கள் OCR.space API Key இங்கே இடுங்கள்
API_KEY = "K89663616288957"

st.title("📄 PDF/Image to Text (Tamil + English OCR)")
st.write("Upload a PDF or Image file and extract text using OCR.space API.")

uploaded_file = st.file_uploader("Upload File", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info(f"✅ File uploaded: {uploaded_file.name}")

    # OCR API call
    files = {
        "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
    }
    payload = {
        "apikey": API_KEY,
        "language": "tam",  # Tamil OCR (works for Tamil + English also)
        "isOverlayRequired": False
    }

    st.write("⏳ Running OCR... Please wait...")
    response = requests.post("https://api.ocr.space/parse/image", files=files, data=payload)

    try:
        result = response.json()  # JSON parse

        # 🔍 Error Handling
        if result.get("IsErroredOnProcessing"):
            error_msg = result.get("ErrorMessage")
            st.error(f"❌ OCR API Error: {error_msg}")
            st.stop()

        # ✅ Extract text
        extracted_text = result["ParsedResults"][0]["ParsedText"]

        st.subheader("📑 Extracted Text:")
        st.text_area("OCR Output", extracted_text, height=300)

        # 💾 Save to TXT
        st.download_button("⬇ Download as TXT", extracted_text, file_name="output.txt")

    except Exception as e:
        st.error(f"Unexpected Error: {e}")
