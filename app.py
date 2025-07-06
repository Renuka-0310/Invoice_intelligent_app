# Imports
import streamlit as st
import easyocr
from PIL import Image
import pandas as pd
from extractor import extract_invoice_fields
from classifier import classify_invoice

# Setup
st.set_page_config(page_title="Invoice Insight", layout="wide")
st.title("📄 Intelligent Invoice Insights System")

# File upload
uploaded_files = st.file_uploader("Upload Invoice Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
reader = easyocr.Reader(['en', 'ar'])

results = []

if uploaded_files:
    for file in uploaded_files:
        image = Image.open(file)
        ocr_result = reader.readtext(image, detail=0)
        text = " ".join(ocr_result)

        fields = extract_invoice_fields(text)
        classification = classify_invoice(text)

        with st.expander(f"🧾 {file.name} Summary"):
            st.image(image, caption="Invoice Preview", width=400)
            st.text_area("📄 Raw OCR Text", text, height=200)
            for k, v in fields.items():
                st.write(f"**{k}:** {v}")
            st.write(f"📌 Type: {classification['invoice_type']}")
            st.write(f"⚠️ Flags: {', '.join(classification['flags']) or 'None'}")
            st.write(f"🎯 Confidence: {classification['confidence']}")

        results.append({
            "Filename": file.name,
            **fields,
            "Type": classification["invoice_type"],
            "Flags": ", ".join(classification["flags"]),
            "Confidence": classification["confidence"]
        })

    df = pd.DataFrame(results)
    st.subheader("📊 Summary Table")
    st.dataframe(df)
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="invoice_summary.csv", mime="text/csv")

    # Chart 1: Monthly Count
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.strftime('%b %Y')
    st.subheader("📈 Monthly Invoice Count")
    st.bar_chart(df.groupby('Month').size())

    # Chart 2: Top Vendors
    df['Amount'] = pd.to_numeric(df['Total Amount'].str.replace(',', ''), errors='coerce')
    st.subheader("🏆 Top 5 Vendors by Amount")
    st.bar_chart(df.groupby('Vendor Name')['Amount'].sum().sort_values(ascending=False).head(5))

    # Chart 3: Payable vs Receivable
    st.subheader("📌 Invoice Type Distribution")
    st.bar_chart(df['Type'].value_counts())