import io
import pdfplumber
import io
import pdfplumber

def extract_text_from_pdf_or_text(uploaded_file) -> str:
    """Accepts an uploaded file-like object from Streamlit and returns extracted text.

    Falls back to reading as plain text if PDF parsing fails.
    """
    # Try PDF first
    try:
        uploaded_file.seek(0)
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
        return "\n".join(pages)
    except Exception:
        # Try to read as text
        try:
            uploaded_file.seek(0)
            data = uploaded_file.read()
            if isinstance(data, bytes):
                return data.decode('utf-8', errors='replace')
            return data
        except Exception:
            return ""
