import os
import json
import subprocess
from dotenv import load_dotenv

def generate_release_notes(commit_messages, api_key):
    url = "https://api.grok4fast.com/v1/release-notes"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"commits": commit_messages}
    
    curl_command = [
        'curl', '-s', '-X', 'POST', url,
        '-H', f"Authorization: Bearer {api_key}",
        '-H', "Content-Type: application/json",
        '-d', json.dumps(data)
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        return {"error": str(e)}

load_dotenv()
API_KEY = os.getenv("GROK4FAST_API_KEY")

def generate_failure_synopsis(logs, api_key):
    url = "https://api.grok4fast.com/v1/failure-synopsis"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"logs": logs}

    curl_command = [
        'curl', '-s', '-X', 'POST', url,
        '-H', f"Authorization: Bearer {api_key}",
        '-H', "Content-Type: application/json",
        '-d', json.dumps(data)
    ]

    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        return {"error": str(e)}

def generate_failure_synopsis(logs, api_key=None):
    key = api_key or API_KEY

if __name__ == "__main__":
    # Example usage:
    # 1. Get commit messages (simulate)
    commit_messages = ["feat: add pipeline dashboard", "fix: handle log capture errors"]
    notes = generate_release_notes(commit_messages, API_KEY)
    print("Release Notes:", notes)
    # 2. Get logs for failed run (simulate)
    logs = "Error: Docker build failed due to missing Dockerfile."
    synopsis = generate_failure_synopsis(logs, API_KEY)
    print("Failure Synopsis:", synopsis)
    notes = generate_release_notes(commit_messages)
    print("Release Notes:", notes)
    synopsis = generate_failure_synopsis(logs)
    print("Failure Synopsis:", synopsis)
