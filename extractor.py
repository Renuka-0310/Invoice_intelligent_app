import re

def extract_invoice_fields(text):
    invoice_no = re.search(r"Invoice[\s#:]*(\w+)", text, re.IGNORECASE)
    
    # Multiple date formats
    date_match = re.search(
        r"(Date|Dated)[\s:]*([\d]{2}[/\-][\d]{2}[/\-][\d]{4}|[\w]+\s\d{1,2},?\s*\d{4}|[\d]{4}-[\d]{2}-[\d]{2})",
        text,
        re.IGNORECASE
    )
    
    # Flexible vendor name patterns
    vendor_match = re.search(r"(Vendor|From|Supplier|Bill From|Sold By)[\s:]*([\w\s,.&\-]+)", text, re.IGNORECASE)

    # Total Amount with ₹/$/Rs/etc
    amount_match = re.search(r"(Total\s*Amount|Amount\s*Due|Grand\s*Total)[\s:₹\$Rs]*([\d,\.]+)", text, re.IGNORECASE)

    # VAT / TAX
    vat_match = re.search(r"(VAT|GST|Tax)[\s:₹\$Rs]*([\d,\.]+)", text, re.IGNORECASE)

    return {
        "Invoice Number": invoice_no.group(1) if invoice_no else "Not Found",
        "Date": date_match.group(2) if date_match else "Not Found",
        "Vendor Name": vendor_match.group(2) if vendor_match else "Not Found",
        "Total Amount": amount_match.group(2) if amount_match else "Not Found",
        "VAT/Tax": vat_match.group(2) if vat_match else "Not Found"
    }