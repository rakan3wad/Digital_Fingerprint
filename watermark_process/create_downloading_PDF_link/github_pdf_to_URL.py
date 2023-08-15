# from github import Github #pip install PyGithub
# import base64

# GitHub credentials
TOKEN = "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"
repo_path = "rakan3wad/digital_fingerprint"

import requests
import base64

# Replace these with your values
REPO_OWNER = 'rakan3wad'
REPO_NAME = 'digital_fingerprint'
FILE_PATH = 'example.pdf'
# FILE_NAME = 'yourfil5.pdf' # Name you want to give the file in the repository
COMMIT_MESSAGE = 'Adding a PDF file'

def create_downloading_PDF_link(FILE_NAME): #EXAMPLE: FILE_NAME = "yourfile4.pdf"
    # Read the file and encode it in base64
    with open(FILE_PATH, 'rb') as file:
        content = base64.b64encode(file.read()).decode('utf-8')

    # Prepare the request
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}'
    headers = {
        'Authorization': f'token {TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'message': COMMIT_MESSAGE,
        'content': content
    }

    # Send the request
    response = requests.put(url, json=data, headers=headers)

    # Check the response
    if response.status_code == 201:
        print(f'{FILE_PATH} has been uploaded to {REPO_OWNER}/{REPO_NAME}')
        return f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{FILE_NAME}"
    else:
        print(f'Error uploading {FILE_PATH}: {response.text}')
        # Error uploading create_downloading_PDF_link/example.pdf: {"message":"Invalid request.\n\n\"sha\" wasn't supplied.","documentation_url":"https://docs.github.com/rest/repos/contents#create-or-update-file-contents"}


print(create_downloading_PDF_link("STAMPED.pdf")) # حط اسم الكتيب ثم اسم العميل ثم 3 ارقام عشوائية