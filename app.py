# Imports
import os
import streamlit as st
import easyocr
from PIL import Image
from pdf2image import convert_from_bytes
import numpy as np
import pandas as pd
from extractor import extract_invoice_fields
from classifier import classify_invoice

# Streamlit setup
st.set_page_config(page_title="Invoice Insight", layout="wide")
st.title("📄 Intelligent Invoice Insights System")

# OCR setup
reader = easyocr.Reader(['en'], gpu=False)

# File upload
uploaded_files = st.file_uploader("Upload Invoice Files (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

results = []

if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"🧾 {file.name}")

        # Convert PDF to image(s)
        if file.name.endswith(".pdf"):
            images = convert_from_bytes(file.read())
        else:
            image = Image.open(file)
            images = [image]

        for image in images:
            np_img = np.array(image)
            extracted = reader.readtext(np_img)
            text = " ".join([res[1] for res in extracted])

            # Extraction + classification
            fields = extract_invoice_fields(text)
            classification = classify_invoice(text)

            # Display section
            with st.expander(f"📄 {file.name} Summary"):
                st.image(image, caption="Invoice Preview", width=400)
                st.text_area("🧾 OCR Text", text, height=200)
                for k, v in fields.items():
                    st.markdown(f"**{k}:** {v}")
                st.markdown(f"📌 Type: **{classification['invoice_type']}**")
                st.markdown(f"⚠️ Flags: **{', '.join(classification['flags']) or 'None'}**")
                st.markdown(f"🎯 Confidence: **{classification['confidence']}%**")

            # Store results
            results.append({
                "Filename": file.name,
                **fields,
                "Type": classification["invoice_type"],
                "Flags": ", ".join(classification["flags"]),
                "Confidence": classification["confidence"]
            })

    # Summary table
    df = pd.DataFrame(results)
    st.subheader("📊 Summary Table")
    st.dataframe(df)

    # Download button
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="invoice_summary.csv", mime="text/csv")

    # Monthly trends
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.strftime('%b %Y')
    st.subheader("📈 Monthly Invoice Count")
    st.bar_chart(df.groupby("Month").size())

    # Top vendors
    df["Amount"] = pd.to_numeric(df["Total Amount"].str.replace(',', ''), errors="coerce")
    st.subheader("🏆 Top 5 Vendors by Amount")
    top_vendors = df.groupby("Vendor Name")["Amount"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_vendors)

    # Type distribution
    st.subheader("📌 Invoice Type Distribution")
    st.bar_chart(df["Type"].value_counts())
    st.bar_chart(df["Type"].value_counts())

