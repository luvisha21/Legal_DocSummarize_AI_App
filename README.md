# Legal Document Risk Analysis Dashboard
<h4><a href=''>By Lavisha Saroha</a></h4>

A Streamlit-powered web application designed to analyze legal documents, identify potential risks, and provide actionable recommendations. It integrates with Google Sheets for saving results and offers email notifications to stakeholders.

## Features

- **File Upload**: Upload legal documents in `.txt`, `.docx`, or `.pdf` formats for analysis.
- **Risk Analysis**: Analyze documents for potential risks and generate recommendations using the LLaMA 3.2 model.
- **Interactive Dashboard**:
  - Displays analysis results in a structured table.
  - Allows downloading results as a CSV file.
- **Google Sheets Integration**: Save analysis results directly to a Google Sheet for record-keeping and further analysis.
- **Email Notifications**: Send a summary of the analysis results to stakeholders via email.
- **Chat Functionality**: Query the document for additional insights or clarifications.
- **User-Friendly Interface**: Organized layout with intuitive navigation and modern design elements.

---

## Technology Stack

### Backend
- **Python**: Core programming language for backend development.
- **LangChain**: Framework for handling Large Language Models (LLMs) and document-based analysis.
- **LLaMA 3.2**: Advanced language model used for risk and recommendation generation.
- **Chroma**: Vector database for document chunking and efficient retrieval.
- **HuggingFace**: Embedding models for semantic similarity between document chunks.

### Frontend
- **Streamlit**: Web framework for building the user interface with custom layouts and real-time interactions.

### Additional Tools
- **Google Sheets API**: For exporting results to Google Sheets.
- **SMTP**: For sending email notifications with the analysis summary.
- **Custom CSS**: For styling the dashboard and improving the user experience.

---

## How It Works

1. **Upload a Document**:
   - Users can upload documents in `.txt`, `.docx`, or `.pdf` format.
   - ![Image](https://github.com/user-attachments/assets/3abae01c-67ea-4d40-8aab-e312ee3d613e)
   
2. **Document Analysis**:
   - The uploaded document is split into smaller chunks for efficient analysis.
   - The LLaMA 3.2 model evaluates each chunk to identify potential risks and provide recommendations.
   - ![Image](https://github.com/user-attachments/assets/4426d1ce-16f3-400b-968e-6edf7c530644)

3. **View Results**:
   - The analysis results are displayed in a table, with columns detailing the document's context, identified risks, and corresponding recommendations.
   - ![Image](https://github.com/user-attachments/assets/862a4834-5294-48ad-b6d7-5d9a89c95148)

4. **Save and Share**:
   - Users can save the results directly to a Google Sheet for further use.
   - Email notifications containing the analysis summary are sent to relevant stakeholders.
   - ![Image](https://github.com/user-attachments/assets/03a7f9c3-6717-45dd-8a01-8a3b032c8a0a)

5. **Query the Document**:
   - Use the chat interface to ask specific questions about the document, enabling deeper insights.
   - ![Image](https://github.com/user-attachments/assets/a0be65ff-bf57-4494-8f7c-6570784d0990)

---

## Prerequisites

Ensure you have the following installed:
- **Python 3.8 or above**

Install the required Python libraries by running the following command:
```bash
pip install -r requirements.txt
