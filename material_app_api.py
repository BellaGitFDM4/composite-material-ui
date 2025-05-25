import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/predict"  # Update to deployed URL later

st.title("🔍 Composite Material Classifier (via API)")

st.markdown("Enter material properties:")

density = st.number_input("Density", min_value=0.0, max_value=20.0, step=0.1)
strength = st.number_input("Tensile Strength", min_value=0.0, max_value=5000.0, step=1.0)
category = st.selectbox("Category", ["Polymer", "Metal", "Composite", "Ceramic", "Natural"])
process = st.selectbox("Process", ["Extrusion", "Casting", "Weaving", "Molding", "Forging", "Lamination", "Injection Molding"])
description = st.text_area("Description", "This material includes fiber and resin.")

if st.button("Predict"):
    payload = {
        "density": density,
        "tensile_strength": strength,
        "category": category,
        "process": process,
        "description": description,
    }
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()["is_composite"]
        st.success("✅ Composite" if result else "❌ Not a Composite")
    else:
        st.error(f"API error: {response.status_code}")

st.markdown("---")
st.subheader("📂 Batch Prediction from CSV")

uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if st.button("Run Batch Prediction"):
        files = {"file": uploaded_file.getvalue()}
        res = requests.post("http://127.0.0.1:8000/predict-batch", files=files)
        if res.status_code == 200:
            result_df = pd.DataFrame(res.json())
            st.success("✅ Predictions completed.")
            st.dataframe(result_df)
            st.download_button("Download Results", result_df.to_csv(index=False), "predictions.csv")
        else:
            st.error("❌ Failed to get predictions from API.")
