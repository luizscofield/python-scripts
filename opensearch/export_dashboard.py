"""
Author:      Luiz Scofield
Date:        02/20/2025
Description: Use this script to export an Opensearch dashboard to a file
"""
import requests

# user information
username = "username"
password = "password"

# Opensearch Information
HOST = 'opensearch-url'
DASHBOARD_ID = "dashboard-id"
EXPORT_FILE = "dashboard.ndjson"

# API Request
url = f"{HOST}/api/saved_objects/_export"
headers = {
    "Content-Type": "application/json",
}

data = {"objects": [{"type": "dashboard","id": DASHBOARD_ID}]}

response = requests.post(url, auth=(username, password), json=data, headers=headers)

# Save the response to a file
if response.status_code == 200:
    with open(EXPORT_FILE, "wb") as file:
        file.write(response.content)
    print(f"Dashboard exported successfully to {EXPORT_FILE}")
else:
    print(f"Failed to export dashboard: {response.text}")
