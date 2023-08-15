import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Use the credentials file you downloaded when setting up gspread
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('DataBase/salla-watermarkapp-5a84f25edd1f.json', scope)
client = gspread.authorize(creds)

# Open the Google Spreadsheet by its name (make sure you have access to it)
sheet = client.open('Salla_Customer').sheet1


def add_NewCustomer_details(*args):

    # The new row you want to add
    new_row = list(args)
    # Get all values from the sheet
    existing_data = sheet.get_all_values()

    # Check if first argument (usually 'id') already exists in the data
    for i, row in enumerate(existing_data, start=1):
        if args[1] in row:
            col_letter_end = chr(64 + len(new_row))  # Convert column number to letter
            sheet.update('A' + str(i) + ':' + col_letter_end + str(i), [new_row])  # Update the row
            break
    else:
        # If 'id' is not found in any row, append the new row
        sheet.append_row(new_row)
