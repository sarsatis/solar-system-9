echo "Opening a Pull Request"

# curl -X 'POST' \
#   'https://github.com/sarsatis/gitops-argocd/pulls' \
#   -H 'accept: application/json' \
#   -H "authorization: $GITHUB_TOKEN" \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "assignee": "sarsatis",
#   "assignees": [
#     "sarsatis"
#   ],
#   "base": "main",
#   "body": "Updated deployment specification with a new image version.",
#   "head": "feature-test",
#   "title": "Updated Solar System Image"
# }'

echo "sa ${GITHUB_TOKEN}"
githupass = URLEncoder.encode("$GITHUB_TOKEN",'UTF-8')
echo "sa ${githupass}"

curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $githupass"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  'https://api.github.com/repos/sarsatis/gitops-argocd/pulls' \
  -d '{
  "assignee": "sarsatis",
  "assignees": [
    "sarsatis"
  ],
  "base": "main",
  "body": "Updated deployment specification with a new image version.",
  "head": "feature-test",
  "title": "Updated Solar System Image"
}'

echo "Success"

