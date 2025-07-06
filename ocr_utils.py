import easyocr
import re

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_files(file_path):
    result = reader.readtext(file_path, detail=0, paragraph=True)
    return "\n".join(result)

def parse_invoice_fields(text):
    fields = {}
    fields["Invoice Number"] = re.findall(r'(?:Invoice|Inv)\s*#?:?\s*(\w+)', text, re.I)
    fields["Date"] = re.findall(r'Date[:\s]*([\d/\-\.]+)', text, re.I)
    fields["Vendor Name"] = re.findall(r'From[:\s]*(\w+)', text, re.I)
    fields["Total Amount"] = re.findall(r'Total\s*[:\s]*\$?([\d,\.]+)', text, re.I)
    fields["VAT/Tax"] = re.findall(r'(?:VAT|Tax)\s*[:\s]*\$?([\d,\.]+)', text, re.I)
    fields["Due Date"] = re.findall(r'Due\s*Date[:\s]*([\d/\-\.]+)', text, re.I)
    fields["Currency"] = re.findall(r'USD|EUR|GBP|AED|INR', text, re.I)

    # Clean up and get first match or default
    cleaned = {k: (v[0] if v else "Not found") for k, v in fields.items()}
    return cleaned
