import json

FILE = "groups"
DESTINATION_FILE = "groups_hcl"

with open(FILE, 'r') as file:

    json_groups = []
    for group in file:
        json_groups.append({"group_name": group.strip()})

final_json = json.dumps(json_groups, indent=4).replace("\"group_name\":", "group_name =")

with open(DESTINATION_FILE, 'w') as file:
    file.write(final_json)
