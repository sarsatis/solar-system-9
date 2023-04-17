import requests
import json
import os

API_TOKEN = os.getenv('GITHUB_TOKEN_PSW')
authorization = f'token {API_TOKEN}'

name = os.getenv('NAME')
build_id = os.getenv('BUILD_ID')


headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': authorization,
    'X-GitHub-Api-Version': '2022-11-28',
}

data = f"""{
            "assignee": "sarsatis",
            "assignees": [
            "sarsatis"
            ],
            "base": "main",
            "body": "Updated deployment specification with a new image version.",
            "head": "{name}-{build_id}",
            "title": "Updated Solar System Image"
        }"""

response = requests.post('https://api.github.com/repos/sarsatis/helm-charts/pulls', headers=headers, data=data)

pretty_json = json.loads(response.content)
print (json.dumps(pretty_json, indent=2))
print(pretty_json.get("number"))
pr_number = pretty_json.get("number")
# pr_number = 16


label_headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': authorization,
    'Content-Type': 'application/json',
}

label_data = f"""{
     "labels": ["{name}"]
    }"""

print('https://api.github.com/repos/sarsatis/helm-charts/issues/{pr_number}/labels')
response = requests.post(f'https://api.github.com/repos/sarsatis/helm-charts/issues/{pr_number}/labels', headers=label_headers, data=label_data)
print(response)