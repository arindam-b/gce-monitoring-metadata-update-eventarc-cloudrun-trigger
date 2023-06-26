# Python libraries

```bash
pip install flask google-auth-httplib2 google-api-python-client
pip install google-cloud-storage
```

# Environment variable for the cloud run

```bash
Environment variables:
storage_bucket = "eviden-ai-poc"
storage_path = "alert-configs/linux"
gh_org = "arindam-b"
gh_repo = "alert-monitoring"
gh_branch = "main"
gh_token = Is the github token mounted from secret manager
```