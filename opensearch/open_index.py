import requests

# Opensearch Information
host = 'opensearch-url'

# user
username = "username"
password = "password"

# index
index= "index-name"

# Delete doc
path = f'/{index}/_open' # the OpenSearch API endpoint
url = host + path

headers = {"Content-Type": "application/json"}

response = requests.post(url, auth=(username, password), headers=headers)

print(response.status_code)
print(response.text)