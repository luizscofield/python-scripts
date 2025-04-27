import requests

# Configuration
TARGET_OPENSEARCH_DASHBOARDS_URL = "http://your-target-opensearch-dashboards-url"
IMPORT_FILE = "dashboard.ndjson"

# API Request
url = f"{TARGET_OPENSEARCH_DASHBOARDS_URL}/api/saved_objects/_import"
headers = {"kbn-xsrf": "true"}

with open(IMPORT_FILE, "rb") as file:
    response = requests.post(url, headers=headers, files={"file": file})

# Check response
if response.status_code == 200:
    print("Dashboard imported successfully!")
else:
    print(f"Failed to import dashboard: {response.text}")
