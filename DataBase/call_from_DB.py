import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up the API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('DataBase/salla-watermarkapp-5a84f25edd1f.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet using its name or URL
sheet = client.open("Salla_Customer").sheet1

# Get the value of cell A1
value = sheet.cell(1, 1).value
print(value)