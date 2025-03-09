import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# Flask API Endpoint (Replace with actual deployed URL if hosted)
FLASK_API_URL = "http://127.0.0.1:5000"

st.title("📅 Goodwing Timetabler")

# File Upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
max_time = st.slider("Select max solver time (seconds)", min_value=30, max_value=600, value=160)
st.write(f"Solver will run for {max_time} seconds.")

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    if st.button("Generate Schedule"):
        with st.spinner("⏳ Processing... Please wait!"):
            # Send file to API
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{FLASK_API_URL}/solve", files=files)

            if response.status_code == 200:
                st.success("✅ Schedule generated successfully!")

                # Fetch download link
                download_url = f"{FLASK_API_URL}/download"
                st.markdown(f"[⬇️ Download Schedule](http://127.0.0.1:5000/download)", unsafe_allow_html=True)

                # Display the schedule
                download_response = requests.get(download_url)
                if download_response.status_code == 200:
                    schedule_data = BytesIO(download_response.content)
                    df = pd.read_excel(schedule_data)
                    st.write("### 📊 Generated Schedule")
                    st.dataframe(df)
                else:
                    st.error("⚠️ Failed to load schedule.")
            else:
                st.error(f"⚠️ Error: {response.json().get('error', 'Unknown error')}")