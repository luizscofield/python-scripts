import requests
import urllib3
import uuid
import json

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

for id, policy in enumerate(policies):
    print(f"\n-------------------------- Policy {id+1}: {policy['name']} --------------------------\n")
    print(f"Tags: {policy['tags']}")
    print(f"Expression: \n\n{policy['expression']}\n")
    entitlement_sequence = 0
    for index, entitlement_id in enumerate(policy['entitlements']):
        entitlement = get_entitlement(token, entitlement_id)
        print(f"---- Policy {id+1} - Entitlement {index+1}: {entitlement['name']} --------\n")
        print(f"---- Site: {entitlement['siteName']}")
        print(f"---- Tags: {entitlement['tags']}")
        print(f"---- Notes: \n{entitlement['notes']}\n")
        print(f"---- Actions: \n{json.dumps(entitlement['actions'], indent=4)}\n")
        entitlement_sequence = index
    if len(policy['entitlementLinks']) > 0:
        for tag in policy['entitlementLinks']:
            entitlements = get_entitlements_by_tag(token, tag)
            for entitlement in entitlements:
                if entitlement['disabled'] is not True:
                    print(f"---- Policy {id+1} - Entitlement {entitlement_sequence+1}: {entitlement['name']} --------\n")
                    print(f"---- Site: {entitlement['siteName']}")
                    print(f"---- Tags: {entitlement['tags']}")
                    print(f"---- Notes: \n{entitlement['notes']}\n")
                    print(f"---- Actions: \n{json.dumps(entitlement['actions'], indent=4)}\n")
                    entitlement_sequence +=1