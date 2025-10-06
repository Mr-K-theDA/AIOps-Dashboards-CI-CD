# AIOps Dashboards & CI-CD IRMAI

This repository contains a small AIOps dashboard project with a simple PowerShell-driven pipeline that runs unit tests, builds a Docker image, executes a smoke test, captures logs, and generates release notes. The pipeline is intended for use on Windows (PowerShell) and was developed to be lightweight and easy to run locally.

---

## Quick status

- Pipeline: `./pipeline.ps1` — runs tests, builds Docker image, runs smoke tests, captures logs, and runs post-pipeline actions.
- Logs: stored in the `logs/` directory. Each pipeline run writes exit code files (`*.exit`) and log files (`*.log`). Recent runs show successful exit codes (0) for tests, Docker build, and smoke tests.

---

## Repository layout

- `pipeline.ps1` - Main pipeline script for Windows PowerShell. Orchestrates installs, tests, Docker build, smoke tests, and post steps.
- `Dockerfile` - Project Dockerfile used by the pipeline to build the container image.
- `requirements.txt` - Python dependencies used by the pipeline and the app.
- `smoke_test.py`, `test_app.py` - Smoke and unit test scripts.
- `capture_logs.py`, `post_pipeline.py` - Helpers used by the pipeline to collect logs and perform post-run actions (release notes etc.).
- `logs/` - Directory containing logs from runs (exit codes and verbose logs).

---

## Prerequisites

Ensure the following are installed and available on PATH:

- Python 3.8+ (python)
- pip
- Docker Desktop (or Docker Engine accessible from this machine)
- Git
- PowerShell (Windows PowerShell v5.1 or PowerShell 7+)

Notes for Windows/WSL users:
- Docker Desktop is recommended. If Docker uses the WSL2 backend ensure the `docker-desktop` WSL distribution is running.
- If Docker client reports a named-pipe/connect error, start Docker Desktop and wait until it initializes.

---

## Setup

1. Clone the repository and cd into the repo root.
2. (Optional) Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
``` 

3. Install Python dependencies (the pipeline will also run this step):

```powershell
python -m pip install -r requirements.txt
```

4. Ensure `.env` exists in the repo root. The pipeline checks for `.env` and will exit if missing. If you do not need secrets for local runs, create an empty placeholder:

```powershell
New-Item -ItemType File -Path .env -Force
```

---

## Running the pipeline

Run the full pipeline from the repository root using PowerShell:

```powershell
./pipeline.ps1
```

What the pipeline does (high level):

1. Validates presence of Python, Docker, Git and `.env`.
2. Installs Python requirements from `requirements.txt`.
3. Runs unit tests with `python -m unittest discover` and writes `logs/test.log` and `logs/test.exit`.
4. Builds the Docker image (`docker build -t myapp .`) and writes `logs/build_docker.log` and `logs/build_docker.exit`.
5. Runs `smoke_test.py` and writes `logs/smoke.log` and `logs/smoke.exit`.
6. Executes `capture_logs.py` which aggregates logs and writes to `logs/runs.json` and `logs/runs.csv`.
7. Runs `post_pipeline.py` to generate additional artifacts (for example, `logs/release_notes.json`).

After a successful pipeline run you should see `0` in `logs/* .exit` files and human-readable outputs in the corresponding `.log` files.

---

## How we verify success

- Each pipeline step writes an exit code file into `logs/` (for example `logs/test.exit`) with a numeric exit code. `0` = success.
- The `smoke.log` contains a textual assertion (e.g., `Smoke test passed!`).
- `logs/runs.json` stores a snapshot of the run with embedded logs and timestamps.

If you need a quick success check:

```powershell
Get-Content logs\test.exit
Get-Content logs\build_docker.exit
Get-Content logs\smoke.exit
``` 

---

## Troubleshooting

- Docker connect/named pipe errors:
  - Symptoms: `error during connect: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.` or `docker info` fails.
  - Fix: Start Docker Desktop and wait until it initializes. If Docker uses WSL2 backend ensure `docker-desktop` distribution is Running (wsl -l -v). If permissions prevent service start, start Docker Desktop from the Start Menu and run the pipeline again.

- Large logs / UTF-16-like output
  - Some log files may contain UTF-16 or embedded null bytes when inspected raw. The exit-code files are authoritative for step success. Use an editor that can detect UTF encodings, or run `Get-Content -Encoding Unicode logs\smoke.log` to read Unicode-encoded logs in PowerShell.

- Build slowness
  - The Docker build can be slow when the build context is large. A `.dockerignore` was added to this repo to exclude `logs/`, `__pycache__`, virtual env directories and other unnecessary files.
  - For faster builds: order Dockerfile layers so that dependencies (e.g., `requirements.txt`) are installed before copying application source, and prefer pinned wheels or cached dependencies.

---

## Developer notes and next steps

- Consider adding a Makefile or a PowerShell task to run timed benchmarks for the pipeline (example: `Measure-Command` around `./pipeline.ps1` or `docker build`).
- Consider moving large or binary logs out of Git history or using artifacts storage for CI systems.
- If you plan to run in CI, ensure credentials and secrets are supplied via CI variables and not via `.env` in the repo.

---

## Contributing

1. Fork the repository.
2. Create a feature branch for your change.
3. Run and test the pipeline locally: `./pipeline.ps1`.
4. Submit a pull request with tests and clear descriptions.

---

If you want, I can also:
- Inspect the `Dockerfile` and propose concrete Docker caching and ordering improvements.
- Add a `Makefile` or `timing.ps1` that runs repeatable benchmarks.
- Add a short `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.
