import re

def extract_invoice_fields(text):
    fields = {}

    # Invoice Number
    invoice_no = re.search(r"(?:Invoice\s*(?:#|Number)?[:\-]?\s*)(\w+)", text, re.IGNORECASE)
    fields["Invoice Number"] = invoice_no.group(1) if invoice_no else "Not Found"

    # Date
    date_match = re.search(
        r"(?:Date|Dated|Invoice\s*Date)[\s:]*([\d]{2}[/\-][\d]{2}[/\-][\d]{4}|[\w]+\s\d{1,2},?\s*\d{4}|[\d]{4}-[\d]{2}-[\d]{2})",
        text,
        re.IGNORECASE
    )
    fields["Date"] = date_match.group(1) if date_match else "Not Found"

    # Vendor Name
    vendor_match = re.search(r"(Vendor|From|Supplier|Bill From|Sold By)[\s:]*([\w\s,.&\-]+)", text, re.IGNORECASE)
    if vendor_match:
        fields["Vendor Name"] = vendor_match.group(2).strip()
    else:
        lines = text.split("\n")
        fallback = next((line for line in lines if "Ltd" in line or "Inc" in line or "Corp" in line or "Company" in line), "Not Found")
        fields["Vendor Name"] = fallback.strip()

    # Total Amount
    amount_match = re.search(r"(Total\s*Amount|Amount\s*Due|Grand\s*Total)[\s:₹\$Rs]*([\d,\.]+)", text, re.IGNORECASE)
    fields["Total Amount"] = amount_match.group(2) if amount_match else "Not Found"

    # VAT / Tax
    vat_match = re.search(r"(VAT|GST|Tax)[\s:₹\$Rs]*([\d,\.]+)", text, re.IGNORECASE)
    fields["VAT/Tax"] = vat_match.group(2) if vat_match else "Not Found"

    # Currency
    currency_match = re.search(r"(USD|EUR|INR|GBP|₹|\$|Rs\.?)", text)
    fields["Currency"] = currency_match.group(1) if currency_match else "Not Found"

<<<<<<< HEAD
    return fields
=======
    return fields
>>>>>>> 71091050ded3f19dfcda20015423e1af8865cb00
