import os
import pandas as pd
import json
from datetime import datetime

LOG_DIR = 'logs'
RUNS_FILE = os.path.join(LOG_DIR, 'runs.json')
CSV_FILE = os.path.join(LOG_DIR, 'runs.csv')

# Helper to read exit code and log

def read_stage(stage):
    with open(os.path.join(LOG_DIR, f'{stage}.exit')) as f:
        exit_code = int(f.read().strip())
    with open(os.path.join(LOG_DIR, f'{stage}.log')) as f:
        log = f.read()
    return exit_code, log

def save_run(run):
    # Save to JSON
    runs = []
    if os.path.exists(RUNS_FILE):
        with open(RUNS_FILE) as f:
            runs = json.load(f)
    runs.append(run)
    with open(RUNS_FILE, 'w') as f:
        json.dump(runs[-10:], f, indent=2)
    # Save to CSV
    df = pd.DataFrame(runs[-10:])
    df.to_csv(CSV_FILE, index=False)

if __name__ == '__main__':
    stages = ['test', 'build_docker', 'smoke']
    results = {}
    for stage in stages:
        exit_code, log = read_stage(stage)
        results[stage] = {'exit_code': exit_code, 'log': log}
    run = {
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'success': all(results[s]['exit_code'] == 0 for s in stages)
    }
    save_run(run)
    print(json.dumps(run, indent=2))
