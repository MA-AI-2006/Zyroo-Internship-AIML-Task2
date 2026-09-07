"""
AI Document Intelligence & Workflow Platform
Zyroo Internship Program - AI/ML Internship - Week 1, Task 01

A simple Streamlit MVP that lets a user upload a PDF or image, reads the
text (with OCR fallback), identifies whether it's an Invoice or Resume,
extracts a few simple fields, and displays the result.

Flow: Upload -> Read Text -> Identify Type -> Find Simple Information -> Show Result
"""

import io
import re

import fitz  # PyMuPDF
import streamlit as st
from PIL import Image

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


ALLOWED_TYPES = ["pdf", "jpg", "jpeg", "png"]


# ---------------------------------------------------------------------------
# Step 2: Read the text
# ---------------------------------------------------------------------------

def extract_text_from_pdf(file_bytes: bytes) -> tuple[str, bool]:
    """Extract text from a PDF using PyMuPDF. Falls back to OCR per-page
    if a page has no selectable text and OCR is available.

    Returns (text, used_ocr).
    """
    text_parts = []
    used_ocr = False

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in doc:
        page_text = page.get_text().strip()
        if page_text:
            text_parts.append(page_text)
        elif OCR_AVAILABLE:
            # No selectable text on this page -> rasterize and OCR it
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            text_parts.append(ocr_text)
            used_ocr = True
    doc.close()

    return "\n".join(text_parts).strip(), used_ocr


def extract_text_from_image(file_bytes: bytes) -> tuple[str, bool]:
    """Extract text from an image file using OCR."""
    if not OCR_AVAILABLE:
        return "", False
    img = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(img)
    return text.strip(), True


# ---------------------------------------------------------------------------
# Step 3: Simple document type classification (rule-based)
# ---------------------------------------------------------------------------

def classify_document(text: str) -> str:
    lower = text.lower()

    invoice_keywords = ["invoice", "invoice number", "total", "amount due", "bill to"]
    resume_keywords = ["resume", "curriculum vitae", "skills", "education", "experience"]

    invoice_score = sum(1 for kw in invoice_keywords if kw in lower)
    resume_score = sum(1 for kw in resume_keywords if kw in lower)

    if invoice_score == 0 and resume_score == 0:
        return "Other"
    if invoice_score >= resume_score:
        return "Invoice"
    return "Resume"


# ---------------------------------------------------------------------------
# Step 4: Extract simple information (regex / keyword based)
# ---------------------------------------------------------------------------

def extract_invoice_fields(text: str) -> dict:
    fields = {
        "Invoice Number": None,
        "Date": None,
        "Company Name": None,
        "Total Amount": None,
    }

    inv_num = re.search(r"invoice\s*(?:number|no\.?|#)\s*[:\-]?\s*([A-Za-z0-9\-]+)", text, re.IGNORECASE)
    if inv_num:
        fields["Invoice Number"] = inv_num.group(1).strip()

    date = re.search(r"\b(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}|\d{4}[/\-]\d{1,2}[/\-]\d{1,2})\b", text)
    if date:
        fields["Date"] = date.group(1).strip()

    total = re.search(r"(?:total|amount due|grand total)\s*[:\-]?\s*([A-Za-z]{0,3}\s?[\d,]+\.?\d*)", text, re.IGNORECASE)
    if total:
        fields["Total Amount"] = total.group(1).strip()

    # Naive company-name guess: first non-empty line that isn't "invoice"
    for line in text.splitlines():
        clean = line.strip()
        if clean and "invoice" not in clean.lower() and len(clean) < 60:
            fields["Company Name"] = clean
            break

    return fields


def extract_resume_fields(text: str) -> dict:
    fields = {
        "Name": None,
        "Email": None,
        "Phone": None,
        "Skills": None,
    }

    email = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    if email:
        fields["Email"] = email.group(0).strip()

    phone = re.search(r"(\+?\d[\d\-\s]{8,}\d)", text)
    if phone:
        fields["Phone"] = phone.group(1).strip()

    skills_match = re.search(r"skills\s*[:\-]?\s*(.+)", text, re.IGNORECASE)
    if skills_match:
        fields["Skills"] = skills_match.group(1).strip()[:200]

    # Naive name guess: first non-empty line of the document
    for line in text.splitlines():
        clean = line.strip()
        if clean:
            fields["Name"] = clean
            break

    return fields


def extract_fields(doc_type: str, text: str) -> dict:
    if doc_type == "Invoice":
        return extract_invoice_fields(text)
    if doc_type == "Resume":
        return extract_resume_fields(text)
    return {}


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="AI Document Intelligence", page_icon="📄", layout="centered")

    st.title("📄 AI Document Intelligence & Workflow Platform")
    st.caption("Zyroo Internship Program • AI/ML Internship • Week 1 • Task 01")

    st.write(
        "Upload a **PDF, JPG, or PNG**. The app will read the text, identify whether "
        "it's an **Invoice** or **Resume**, extract a few simple fields, and show the result."
    )

    if not OCR_AVAILABLE:
        st.info(
            "OCR (pytesseract) isn't installed in this environment, so scanned "
            "images/PDFs without selectable text won't be read. Text-based PDFs "
            "still work normally."
        )

    uploaded_file = st.file_uploader(
        "Upload a document", type=ALLOWED_TYPES, accept_multiple_files=False
    )

    if uploaded_file is None:
        st.stop()

    file_bytes = uploaded_file.read()
    file_ext = uploaded_file.name.split(".")[-1].lower()

    st.subheader("1. Uploaded Document")
    st.write(f"**Filename:** {uploaded_file.name}")
    st.write(f"**File type:** {file_ext.upper()}")

    with st.spinner("Reading text..."):
        if file_ext == "pdf":
            text, used_ocr = extract_text_from_pdf(file_bytes)
        else:
            text, used_ocr = extract_text_from_image(file_bytes)

    if not text:
        st.error(
            "No text could be extracted from this file. If it's a scanned "
            "document, make sure Tesseract OCR is installed."
        )
        st.stop()

    st.subheader("2. Document Type")
    doc_type = classify_document(text)
    st.write(f"**Identified type:** `{doc_type}`" + (" (via OCR)" if used_ocr else ""))

    st.subheader("3. Extracted Fields")
    fields = extract_fields(doc_type, text)
    if fields:
        for key, value in fields.items():
            st.write(f"**{key}:** {value if value else '_Not found_'}")
    else:
        st.write("No fields extracted (document type is `Other`).")

    st.subheader("4. Extracted Text")
    with st.expander("Show raw extracted text"):
        st.text(text)


if __name__ == "__main__":
    main()
