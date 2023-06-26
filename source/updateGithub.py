import requests
import os
import json
import tempfile


gh_token = os.environ.get("gh_token")
gh_org = os.environ.get("gh_org")
gh_branch = os.environ.get("gh_branch")
gh_repo = os.environ.get("gh_repo")

repo_url=f"https://api.github.com/repos/{gh_org}/{gh_repo}/git"

headers = {
        'Authorization': f'Bearer {gh_token}',
        'Content-Type': 'application/json'
    }

# Find the temporary storage path
path = tempfile.gettempdir()


def create_blob(contents):
    
    payload = {
        "content": contents,
        "encoding": "utf-8"
    }

    response = requests.post(f"{repo_url}/blobs",
                            headers=headers,
                            json=payload)
    
    print(response)
    
    response_json=json.loads(response.text)

    print(response_json)
    
    file_sha = response_json["sha"]

    return file_sha


def get_sha_from_branch():
    response = requests.get(f"{repo_url}/trees/{gh_branch}", \
                             headers=headers)
    response_json=json.loads(response.text)

    root_sha = response_json["sha"]    
    
    return root_sha


def update_file(root_sha, file_sha):
    payload = {
        "tree":[
                    {
                        "path":"alert_configuration",
                        "mode":"100644",
                        "type":"blob",
                        "sha": file_sha
                    }
               ],
        "base_tree": root_sha
    }
    
    response = requests.post(f"{repo_url}/trees",
                            headers=headers,
                            json=payload)
    
    response_json=json.loads(response.text)
    computed_sha = response_json["sha"]

    return computed_sha


def make_commit(root_sha, computed_sha):
    payload = {
        "tree": computed_sha,
        "message":"Alert mechanism from Cloudrun autormaiton.",
        "parents": [root_sha]
    }

    response = requests.post(f"{repo_url}/commits",
                            headers=headers,
                            json=payload)
    
    response_json=json.loads(response.text)
    ref_sha = response_json["sha"]
    return ref_sha


def update_ref(ref_sha):
    payload = {
        "sha": ref_sha
    }

    response = requests.patch(f"{repo_url}/refs/heads/{gh_branch}",
                            headers=headers,
                            json=payload)
    print(response)


def process_github_commit(contents):
    file_sha = create_blob(contents)
    root_sha = get_sha_from_branch()
    computed_sha = update_file(root_sha, file_sha)
    ref_sha = make_commit(root_sha, computed_sha)
    update_ref(ref_sha)
