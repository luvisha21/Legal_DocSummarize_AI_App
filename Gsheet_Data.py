import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Google Sheets Configuration
SERVICE_ACCOUNT_FILE = "/content/groovy-footing-449211-r2-068e664a1b06.json"  # Replace with your service account file for G-sheet
SPREADSHEET_ID = "1VsWczYC3s9fGlFx6cLgxBE7cLxcijipjsBYWaRLcF0g"  # Replace with your Google Sheet ID

RANGE_NAME = 'Sheet1!A1'

def authenticate_gsheet():
    """Authenticate with the Google Sheets API."""
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build('sheets', 'v4', credentials=credentials)

def write_to_gsheet(data):
    """Write data to Google Sheets."""
    service = authenticate_gsheet()
    sheet = service.spreadsheets()

    # Prepare data for writing
    values = [["Context", "Recommendations", "Risk Detection"]]
    for entry in data:
        values.append([entry["context"], entry["recommendations"], entry["risk detection"]])

    # Body for the API request
    body = {"values": values}

    # Write data to the sheet
    response = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"{response.get('updatedCells')} cells updated in Google Sheet.")

if __name__ == "__main__":
    # Load data from JSON
    with open("risk_analysis.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Write to Google Sheets
    write_to_gsheet(data)
