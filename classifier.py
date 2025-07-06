import re
import hashlib
from datetime import datetime

def get_invoice_type(text):
    if "Amount Payable" in text or "Payable To" in text or "Due" in text:
        return "Payable"
    elif "Amount Received" in text or "Received From" in text:
        return "Receivable"
    else:
        return "Unknown"

def check_missing_vat(text):
    if "VAT" not in text and "Tax" not in text:
        return "Missing VAT"

def check_due_date(text):
    match = re.search(r"(Due Date|Due On)[:\s]*(\w+\s\d{1,2},?\s*\d{4})", text)
    if match:
        try:
            due_date = datetime.strptime(match.group(2), "%b %d %Y")
            if due_date > datetime.now():
                return "Future Due Date"
        except:
            pass

def get_invoice_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def get_confidence(text):
    hits = 0
    if re.search(r"Invoice\s*#?:?\s*\d+", text): hits += 1
    if re.search(r"Total\s*Amount[:₹\s]*\d+", text): hits += 1
    if re.search(r"(Date|Dated)[:\s]*\w+", text): hits += 1
    if "VAT" in text or "Tax" in text: hits += 1

    if hits >= 3:
        return "High"
    elif hits == 2:
        return "Medium"
    else:
        return "Low"

def classify_invoice(text, known_hashes=None):
    invoice_type = get_invoice_type(text)

    flags = []
    vat_flag = check_missing_vat(text)
    if vat_flag:
        flags.append(vat_flag)

    due_flag = check_due_date(text)
    if due_flag:
        flags.append(due_flag)

    hash_val = get_invoice_hash(text)
    if known_hashes and hash_val in known_hashes:
        flags.append("Duplicate Invoice")

    confidence = get_confidence(text)

    return {
        "invoice_type": invoice_type,
        "flags": flags,
        "confidence": confidence
    }