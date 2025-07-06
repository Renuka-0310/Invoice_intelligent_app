from datetime import datetime

def classify_invoice(fields):
    today = datetime.today()
    issues = []
    
    payable = "pay" in fields.get("Vendor", "").lower()
    
    if not fields["VAT/Tax"]:
        issues.append("Missing VAT")
    
    try:
        due_date = datetime.strptime(fields["Due Date"], "%d/%m/%Y")
        if due_date > today:
            issues.append("Future due date")
        elif due_date < today:
            issues.append("Overdue")
    except:
        issues.append("Invalid due date")

    return {
        "type": "Payable" if payable else "Receivable",
        "issues": issues,
        "urgency": "Overdue" if "Overdue" in issues else "Normal"
    }
