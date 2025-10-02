import streamlit as st
import pandas as pd
import json
import os

LOG_DIR = 'logs'
RUNS_FILE = os.path.join(LOG_DIR, 'runs.json')
CSV_FILE = os.path.join(LOG_DIR, 'runs.csv')
RELEASE_NOTES_FILE = os.path.join(LOG_DIR, 'release_notes.json')
FAILURE_SYNOPSIS_FILE = os.path.join(LOG_DIR, 'failure_synopsis.json')

st.set_page_config(page_title="Pipeline Pilot Dashboard", layout="wide")
st.title("Pipeline Pilot Dashboard")

# Load run history
def load_runs():
    if os.path.exists(RUNS_FILE):
        with open(RUNS_FILE) as f:
            return json.load(f)
    return []

runs = load_runs()

success_count = sum(1 for r in runs if r.get('success'))
failure_count = len(runs) - success_count

st.metric("Success Count", success_count)
st.metric("Failure Count", failure_count)

st.subheader("Last 10 Pipeline Runs")
if runs:
    df = pd.DataFrame([
        {
            'Timestamp': r['timestamp'],
            'Success': r['success'],
            'Test Exit': r['results']['test']['exit_code'],
            'Build Exit': r['results']['build_docker']['exit_code'],
            'Smoke Exit': r['results']['smoke']['exit_code'],
        } for r in runs
    ])
    st.dataframe(df)
else:
    st.info("No runs found.")

# Release Notes
st.subheader("Latest Release Notes")
if os.path.exists(RELEASE_NOTES_FILE):
    with open(RELEASE_NOTES_FILE) as f:
        notes = json.load(f)
    st.json(notes)
else:
    st.info("No release notes found.")

# Failure Synopsis
st.subheader("Latest Failure Synopsis")
if os.path.exists(FAILURE_SYNOPSIS_FILE):
    with open(FAILURE_SYNOPSIS_FILE) as f:
        synopsis = json.load(f)
    st.json(synopsis)
else:
    st.info("No failure synopsis found.")

st.subheader("Run Details")
for i, r in enumerate(reversed(runs)):
    with st.expander(f"Run {len(runs)-i}: {r['timestamp']}"):
        st.write(r)
