import requests
import json


headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer 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',
    'X-GitHub-Api-Version': '2022-11-28',
}

data = """{
            "assignee": "sarsatis",
            "assignees": [
            "sarsatis"
            ],
            "base": "main",
            "body": "Updated deployment specification with a new image version.",
            "head": "solar-system-13",
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
    'Authorization': 'Bearer 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',
    'Content-Type': 'application/json',
}

label_data = """{
     "labels": ["${NAME}"]
    }"""

print('https://api.github.com/repos/sarsatis/helm-charts/issues/{pr_number}/labels')
response = requests.post(f'https://api.github.com/repos/sarsatis/helm-charts/issues/{pr_number}/labels', headers=label_headers, data=label_data)
print(response)