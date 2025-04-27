import requests
import urllib3
import uuid
import csv

APPGATE_API_URL = "appgate-api-url"
USERNAME = "username"
PASSWORD = "password"
PROVIDER_NAME = "idp-provider-name"

default_headers = {
    "Accept": "application/vnd.appgate.peer-v20+json",
    "Content-Type": "application/json"
}

def auth_token(username, password, provider_name):
    auth_url = f"{APPGATE_API_URL}/login"
    headers = default_headers
    login_payload = {
        "username": username,
        "password": password,
        "providerName": provider_name,
        "deviceId": str(uuid.uuid4())
    }
    
    response = requests.post(auth_url, json=login_payload, headers=headers, verify=False)
    token = response.json().get("token")
    return token

def get_entitlement(token, id):
    url = f"{APPGATE_API_URL}/entitlements/{id}"
    headers = {
        "Authorization": f"Bearer {token}",
        **default_headers
    }
    response = requests.get(url, headers=headers, verify=False)
    return response.json()

def get_all_policies(token):
    url = f"{APPGATE_API_URL}/policies"
    headers = {
        "Authorization": f"Bearer {token}",
        **default_headers
    }
    response = requests.get(url, headers=headers, verify=False)
    return response.json()['data']

def get_entitlements_by_tag(token, tag):
    url = f"{APPGATE_API_URL}/entitlements"
    headers = {
        "Authorization": f"Bearer {token}",
        **default_headers
    }
    response = requests.get(url, headers=headers, verify=False)
    all_entitlements = response.json()['data'] 

    entitlements = [
        ent for ent in all_entitlements if "tags" in ent and tag in ent["tags"]
    ]
    return entitlements

# Disable Insecure Request Warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ----- Starting script -----

token = auth_token(USERNAME, PASSWORD, PROVIDER_NAME)
policies = get_all_policies(token)

# File to store the CSV output
OUTPUT_CSV = "policies_report.csv"

# Open CSV file for writing
with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write header row
    writer.writerow([
        "Policy", "Expression", "Entitlement", "Site", "Entitlement Tags", "Notes", "Action", "protocol", "hosts", "ports"
    ])

    # Iterate over policies
    for id, policy in enumerate(policies):
        policy_name = f"Policy {id+1}: " + policy["name"]
        policy_expression = policy["expression"].strip()

        if "containsText" in policy_expression:
            part = policy_expression.split("containsText(\"")[1]
            expression = part.split("\")")[0]
        elif "CN=" in policy_expression:
            part = policy_expression.split("CN=")[1]
            expression = part.split(",OU")[0]
        elif "CN=" not in policy_expression and "indexOf" in policy_expression:
            part = policy_expression.split("indexOf(\"")[1]
            expression = part.split("\")")[0]
        else:
            expression = policy_expression

        # Entitlements linked by ID
        for entitlement_id in policy["entitlements"]:
            entitlement = get_entitlement(token, entitlement_id)
            if not entitlement['disabled']:
                actions = []
                for action in entitlement['actions']:
                    writer.writerow([
                        policy_name,
                        expression,
                        entitlement["name"],
                        entitlement["siteName"],
                        ", ".join(entitlement["tags"]) if entitlement["tags"] else "",
                        entitlement["notes"].strip() if entitlement["notes"] else "",
                        action['action'],
                        action['subtype'],
                        action['hosts'],
                        action['ports'] if 'ports' in action else ''
                    ])

        # Entitlements linked by tag
        if len(policy["entitlementLinks"]) > 0:
            for tag in policy["entitlementLinks"]:
                entitlements = get_entitlements_by_tag(token, tag)
                for entitlement in entitlements:
                    if not entitlement["disabled"]:
                        actions = []
                        for action in entitlement['actions']:
                            writer.writerow([
                                policy_name,
                                expression,
                                entitlement["name"],
                                entitlement["siteName"],
                                ", ".join(entitlement["tags"]) if entitlement["tags"] else "",
                                entitlement["notes"].strip() if entitlement["notes"] else "",
                                action['action'],
                                action['subtype'],
                                action['hosts'],
                                action['ports'] if 'ports' in action else ''
                            ])
