# AI Document Intelligence & Workflow Platform
Live at: https://zyroo-internship-aiml-task2-gcbwznvkbfk2xmwwwchgnr.streamlit.app

**Zyroo Internship Program — AI/ML Internship — Week 1, Task 01**
Level: Beginner

A simple Streamlit app that lets a user upload a PDF or image, reads the text
(with OCR fallback for scanned documents), identifies whether the document is
an **Invoice** or **Resume**, extracts a few simple fields, and displays the
result.

## Flow

```
Upload → Read Text (PyMuPDF / OCR) → Identify Type → Extract Fields → Show Result
```

## Features

- Accepts **PDF, JPG/JPEG, PNG**
- Text extraction from normal PDFs via **PyMuPDF**
- OCR fallback via **Tesseract (pytesseract)** for scanned pages/images
- Simple rule-based classification: **Invoice**, **Resume**, or **Other**
- Regex/keyword-based field extraction:
  - **Invoice:** Invoice Number, Date, Company Name, Total Amount
  - **Resume:** Name, Email, Phone, Skills
- Clean Streamlit UI showing filename, type, extracted fields, and raw text

## Project Structure

```
ai-document-intelligence/
├── app.py
├── requirements.txt
├── packages.txt        # system deps (tesseract-ocr) for Streamlit Cloud
├── README.md
└── samples/             # put sample invoice/resume files here for testing
```

## Setup (Local)

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/ai-document-intelligence.git
   cd ai-document-intelligence
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR** (needed only for scanned images/PDFs)
   - **Windows:** download the installer from the
     [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) page.
   - **macOS:** `brew install tesseract`
   - **Linux (Debian/Ubuntu):** `sudo apt-get install tesseract-ocr`

5. **Run the app**
   ```bash
   streamlit run app.py
   ```
   The app opens at `http://localhost:8501`.

## Testing

Test with at least 3 sample documents (2 invoices, 1 resume) — drop them in
`samples/` and upload them through the UI. Confirm:
- Text is extracted correctly
- Document type is identified correctly
- Note down any fields that aren't found (regex rules are intentionally simple)

## Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub (see below).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select this repository, branch `main`, and set the main
   file path to `app.py`.
4. Click **Deploy**. Streamlit Cloud will read `requirements.txt` and
   `packages.txt` (for the `tesseract-ocr` system package) automatically.

## Tech Stack

- Python
- Streamlit
- PyMuPDF
- Tesseract OCR (pytesseract)
- Regular Expressions
- Git + GitHub

## Notes

- This is a beginner MVP focused on a simple, working end-to-end flow rather
  than perfect accuracy — see the assignment brief for scope.
- An optional next step (per the assignment) is replacing the rule-based
  classifier with a small TF-IDF + Logistic Regression model.
