import easyocr
from pdf2image import convert_from_bytes
import re

reader = easyocr.Reader(['en'])  # Add 'ar' for Arabic

def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        images = convert_from_bytes(file.read())
        for img in images:
            result = reader.readtext(np.array(img), detail=0, paragraph=True)
            text += " ".join(result) + "\n"
    else:
        result = reader.readtext(file.read(), detail=0, paragraph=True)
        text = " ".join(result)
    return text
import easyocr
from pdf2image import convert_from_bytes
import re

reader = easyocr.Reader(['en'])  # Add 'ar' for Arabic

def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        images = convert_from_bytes(file.read())
        for img in images:
            result = reader.readtext(np.array(img), detail=0, paragraph=True)
            text += " ".join(result) + "\n"
    else:
        result = reader.readtext(file.read(), detail=0, paragraph=True)
        text = " ".join(result)
    return text
def extract_fields(text):
    fields = {
        "Invoice Number": re.findall(r"Invoice\s*No\.?:?\s*(\w+)", text),
        "Date": re.findall(r"Date:?\s*(\d{1,2}/\d{1,2}/\d{2,4})", text),
        "Vendor": re.findall(r"From:? (.+)", text),
        "Total Amount": re.findall(r"Total:? \$?(\d+[\.,]?\d*)", text),
        "VAT/Tax": re.findall(r"(?:VAT|Tax):?\s*[\$€]?\s*(\d+[\.,]?\d*)", text),
        "Due Date": re.findall(r"Due\s*Date:?\s*(\d{1,2}/\d{1,2}/\d{2,4})", text),
        "Currency": re.findall(r"([$€£])", text)
    }
    return {k: v[0] if v else "" for k, v in fields.items()}

def process_invoice(file):
    text = extract_text(file)
    fields = extract_fields(text)
    return {"raw_text": text, "fields": fields}
