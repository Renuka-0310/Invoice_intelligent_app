import re
from datetime import datetime

def classify_invoice(text):
    classification = {
        "invoice_type": "Unknown",
        "flags": [],
        "confidence": 0
    }

    # Basic rule-based detection
    text_lower = text.lower()
    if "payable" in text_lower or "you owe" in text_lower:
        classification["invoice_type"] = "Payable"
        classification["confidence"] += 50
    elif "receivable" in text_lower or "amount to receive" in text_lower:
        classification["invoice_type"] = "Receivable"
        classification["confidence"] += 50

    # VAT existence
    if not re.search(r"(VAT|Tax|GST)", text, re.IGNORECASE):
        classification["flags"].append("Missing VAT")

    # Date check for future due date
    due_date_match = re.search(
        r"(?:Due\s*Date)[:\-]?\s*(\d{2}[/\-]\d{2}[/\-]\d{4}|\d{4}-\d{2}-\d{2})",
        text,
        re.IGNORECASE
    )
    if due_date_match:
        try:
            due_date_str = due_date_match.group(1)
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d" if "-" in due_date_str else "%d/%m/%Y")
            if due_date > datetime.now():
                classification["flags"].append("Future Due Date")
                classification["confidence"] += 15
        except Exception:
            classification["flags"].append("Unrecognized Due Date")

    # Duplicate invoice guess (mock logic)
    if text_lower.count("invoice number") > 1:
        classification["flags"].append("Duplicate Invoice Mention")

    # Final confidence normalization
    classification["confidence"] = min(classification["confidence"] + 35, 100)

<<<<<<< HEAD
    return classification
=======
    return classification
>>>>>>> 71091050ded3f19dfcda20015423e1af8865cb00
