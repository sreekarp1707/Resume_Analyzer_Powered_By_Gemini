import pdfplumber
from docx import Document


def extract_text(file):
    filename = file.name.lower()

    if filename.endswith('.pdf'):
        text = ""

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text.strip()

    elif filename.endswith('.docx'):
        document = Document(file)

        text = []

        for paragraph in document.paragraphs:
            text.append(paragraph.text)

        return "\n".join(text).strip()

    return ""