import os
import json
import subprocess
import sys
from dotenv import load_dotenv
from grok4fast_api import generate_release_notes, generate_failure_synopsis

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GROK4FAST_API_KEY")

LOG_DIR = 'logs'
RUNS_FILE = os.path.join(LOG_DIR, 'runs.json')
RELEASE_NOTES_FILE = os.path.join(LOG_DIR, 'release_notes.json')
FAILURE_SYNOPSIS_FILE = os.path.join(LOG_DIR, 'failure_synopsis.json')

# Get commit messages from git log matching Conventional Commit prefixes
def get_commit_messages():
    try:
        # Run git log to get recent commits matching pattern
        result = subprocess.run(['git', 'log', '--oneline', '--since=1 week ago', '--grep=^\\(feat\\|fix\\|chore\\):'], capture_output=True, text=True)
        if result.returncode == 0:
            messages = result.stdout.strip().split('\n')
            return [msg for msg in messages if msg]
        else:
            print("Git command failed, using default messages", file=sys.stderr)
            return ["feat: initial pipeline setup", "fix: general fixes"]
    except Exception as e:
        print(f"Error fetching commits: {e}, using defaults", file=sys.stderr)
        return ["feat: initial pipeline setup", "fix: general fixes"]

# Get last run
with open(RUNS_FILE) as f:
    runs = json.load(f)
last_run = runs[-1] if runs else None

if last_run:
    # Release notes
    commit_messages = get_commit_messages()
    if API_KEY:
        notes = generate_release_notes(commit_messages, api_key=API_KEY)
        with open(RELEASE_NOTES_FILE, 'w') as f:
            json.dump(notes, f, indent=2)
    else:
        print("API key not found, skipping release notes.", file=sys.stderr)

    # Failure synopsis if failed
    if not last_run['success']:
        if API_KEY:
            logs = '\n'.join([last_run['results'][s]['log'] for s in last_run['results']])
            synopsis = generate_failure_synopsis(logs, api_key=API_KEY)
            with open(FAILURE_SYNOPSIS_FILE, 'w') as f:
                json.dump(synopsis, f, indent=2)
        else:
            print("API key not found, skipping failure synopsis.", file=sys.stderr)
