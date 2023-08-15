import requests
import base64

def upload_pdf_to_github(token, repo_owner, repo_name, file_path, new_file_name, commit_message):
    # Open the PDF file and encode it in base64
    with open(file_path, 'rb') as file:
        content = base64.b64encode(file.read()).decode('utf-8')

    # Define the URL for the GitHub API request
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{new_file_name}"

    # Prepare the headers for the request
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }

    # Prepare the payload for the request
    payload = {
        "message": commit_message,
        "content": content
    }

    # Make the request to the GitHub API
    response = requests.put(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 201:
        # Extract the raw URL from the response
        raw_url = response.json()['content']['download_url']
        return raw_url
    else:
        return f"Error: {response.json()}"

# Example usage
token = "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"
repo_owner = "rakan3wad"
repo_name = "Digital_Fingerprint"
file_path = "STAMPED.pdf"
new_file_name = "watermark_process/create_downloading_PDF_link/all_PDF_files/new_name_for_file3.pdf" #✏️
commit_message = "Uploading PDF file with new name"

raw_url = upload_pdf_to_github(token, repo_owner, repo_name, file_path, new_file_name, commit_message)
print(raw_url)
