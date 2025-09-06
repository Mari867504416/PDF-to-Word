import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# -------------------------------------
# OCR function (Tesseract)
# -------------------------------------
def ocr_pdf(uploaded_file, lang="tam+eng"):
    text = ""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page_num in range(len(doc)):
        # Convert page to image
        pix = doc[page_num].get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # OCR extract
        page_text = pytesseract.image_to_string(img, lang=lang)
        text += f"\n--- Page {page_num+1} ---\n"
        text += page_text

    return text

# -------------------------------------
# Streamlit UI
# -------------------------------------
st.title("📄 Unlimited PDF to Text (Tesseract OCR)")

uploaded_file = st.file_uploader("📤 Upload PDF", type=["pdf"])

if uploaded_file:
    st.info("⏳ Running OCR... Please wait...")
    extracted_text = ocr_pdf(uploaded_file, lang="tam+eng")

    if extracted_text.strip():
        st.success("✅ OCR Completed Successfully!")
        st.text_area("📜 Extracted Text:", extracted_text, height=400)

        # Download button
        st.download_button(
            label="💾 Download as TXT",
            data=extracted_text,
            file_name="ocr_output.txt",
            mime="text/plain"
        )
    else:
        st.error("❌ No text extracted. Try with a clearer PDF.")
