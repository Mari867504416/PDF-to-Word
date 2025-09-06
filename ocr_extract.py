import streamlit as st
import requests
from docx import Document
from io import BytesIO

st.title("📄 PDF to Word (API4AI OCR - Unlimited Pages)")

# Your RapidAPI credentials
api_host = "ocr43.p.rapidapi.com"
api_url = "https://ocr43.p.rapidapi.com/v1/results"
api_key = st.text_input("Enter RapidAPI Key:", type="password")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded and api_key:
    with st.spinner("Running OCR via API4AI..."):
        files = {"url": uploaded.getvalue()}
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host
        }
        response = requests.post(api_url, headers=headers, files=files)
        try:
            data = response.json()
        except Exception as e:
            st.error(f"Invalid response: {e}")
            st.stop()

        # Extract text
        if not (data.get("results")):
            st.error("No OCR results returned.")
            st.stop()

        extracted = ""
        for res in data["results"]:
            extracted += res.get("entities", [{}])[0].get("objects", [{}])[0].get("entities", [{}])[0].get("text", "") + "\n"

        st.success("OCR Complete!")

        st.text_area("Extracted Text", extracted, height=400)

        # Download as Word
        doc = Document()
        for line in extracted.split("\n"):
            doc.add_paragraph(line)
        buf = BytesIO()
        doc.save(buf)
        buf.seek(0)
        st.download_button("Download .docx", buffer=buf, file_name="output.docx")
