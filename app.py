import streamlit as st
import pandas as pd
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
import os
from dotenv import load_dotenv

# Google Sheets Configuration
SERVICE_ACCOUNT_FILE = "/content/groovy-footing-449211-r2-068e664a1b06.json"  # Replace with your service account file for G-sheet
SPREADSHEET_ID = "1VsWczYC3s9fGlFx6cLgxBE7cLxcijipjsBYWaRLcF0g"  # Replace with your Google Sheet ID

# LLM Configuration
import google.generativeai as genai
# Configure and initialize GenAI
api_key = "AIzaSyBQiT1bfsMLONlsyYygJYq7-gBA6HMkPQA" #enter your own gemini api_key (which is free)
genai.configure(api_key=api_key)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# Streamlit App
st.set_page_config(page_title="Legal Document Risk Analysis", layout="wide")

# Enhanced CSS for Custom Styling
st.markdown(
    """
    <style>
    .main-container {
        padding: 2rem;
        background-color: #f9f9f9;
        font-family: 'Arial', sans-serif;
        color: #333333;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .upload-box {
        background-color: #ffffff;
        border: 2px dashed #dcdcdc;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 20px;
        color: #888;
    }
    .dataframe-container {
        margin-top: 20px;
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .button-row button {
        margin-right: 10px;
        background-color: #2ecc71;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .button-row button:hover {
        background-color: #27ae60;
    }
    .chat-container {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        border-radius: 10px;
        padding: 20px;
        margin-top: 30px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .sidebar {
        background-color: #f3f3f3;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("\U0001F4D6 Legal Document Risk Analysis Dashboard")

# Sidebar for Email Configuration
st.sidebar.header("Email Configuration 📧")
sender_email = st.sidebar.text_input("Sender Email", placeholder="Enter sender email...")
sender_password = st.sidebar.text_input("Sender Password", placeholder="Enter sender password...")
recipient_email = st.sidebar.text_input("Recipient Email", placeholder="Enter recipient email...")
subject = "Legal Document Risks and Recommendations"
send_email = st.sidebar.button("Send Email")

# File Upload Section
st.subheader("\U0001F4C4 Upload a Legal Document")
st.markdown(
    "<div class='upload-box'>Drag and drop your file here or use the button below to upload your document (TXT, DOCX, PDF).</div>",
    unsafe_allow_html=True
)
uploaded_file = st.file_uploader("Upload your document", type=["txt", "docx", "pdf"])

# Layout for Analysis Results
if uploaded_file:
    st.success("File uploaded successfully!")
    file_content = uploaded_file.read().decode("utf-8")

    # Analyze the document
    st.subheader("\U0001F50D Analyzing the document...")
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=20)
    texts = text_splitter.split_text(file_content)
    embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(texts, embed)

    def detect_risks_and_recommendations(text_chunks):
        results = []
        for chunk in text_chunks:
            prompt = (
                f"Analyze the following text and provide a structured response:\n\n"
                f"Text: {chunk}\n\n"
                f"Provide the following details:\n"
                f"- Risks: Summarize potential risks, issues, or hidden dependencies clearly.\n"
                f"- Recommendations: Suggest practical, clear, and actionable recommendations to mitigate the risks.\n\n"
                f"Output format:\n"
                f"Risks: <List the risks in simple bullet points>\n"
                f"Recommendations: <List the recommendations in simple bullet points>"
            )
            response = model.start_chat().send_message(prompt)
            response_text = response.text
            risks, recommendations = "No risks identified.", "No recommendations provided."

            if "Risks:" in response_text and "Recommendations:" in response_text:
                try:
                    risks_start = response_text.index("Risks:") + len("Risks:")
                    recommendations_start = response_text.index("Recommendations:")
                    risks = response_text[risks_start:recommendations_start].strip()
                    recommendations = response_text[recommendations_start + len("Recommendations:"):].strip()
                except ValueError:
                    pass

            results.append({
                "context": chunk,
                "risks": risks,
                "recommendations": recommendations
            })
        return results

    results = detect_risks_and_recommendations(texts)
    df = pd.DataFrame(results)

    # Display Results in a Styled Table
    st.subheader("\U0001F4CA Results")
    st.markdown(
        "<div class='dataframe-container'>", unsafe_allow_html=True
    )
    st.dataframe(df, height=500)
    st.markdown("</div>", unsafe_allow_html=True)

    # Download Results Button
    st.download_button(
        label="\U0001F4E5 Download Results",
        data=df.to_csv(index=False),
        file_name="risk_analysis.csv",
        mime="text/csv",
    )

    # Save to Google Sheets
    if st.button("Save to Google Sheets"):
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()

        values = [["Context", "Risks", "Recommendations"]]
        for result in results:
            values.append([result["context"], result["risks"], result["recommendations"]])

        body = {"values": values}
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body=body,
        ).execute()
        st.success("Data saved to Google Sheets.")

    # Email Sending Section
    if send_email:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(
                MIMEText(
                    f"Please find the risk analysis report attached:\n\n"
                    f"https://docs.google.com/spreadsheets/d/1rvEwtYh7mpqcBZgv7D14giGZ_mhBM-aiNZ_dxjJJQf0/edit?usp=sharing",
                    "plain"
                )
            )
            server.send_message(message)
            server.quit()
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")

    # Chat Area
    st.subheader("\U0001F4AC Chat About the Document")
    query = st.text_input("Type your question here...", placeholder="Ask something about the document")
    if st.button("Get Response"):
        chat_session = model.start_chat()
        prompt = f"Based on the legal document:\n{texts}\nAnswer the following question:\n{query}"
        response = chat_session.send_message(prompt)
        st.write(response.text)
