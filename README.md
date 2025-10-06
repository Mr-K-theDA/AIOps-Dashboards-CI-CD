# Pipeline Pilot Dashboard

This project is a Streamlit-based dashboard designed to monitor and visualize the results of CI/CD pipeline runs. It provides at-a-glance metrics, detailed run history, release notes, and failure analysis. The application is integrated with Sentry for real-time error tracking and performance monitoring.

## Features

*   **Interactive Dashboard**: A web-based UI built with Streamlit to visualize pipeline data.
*   **Run Metrics**: Displays total success and failure counts for all pipeline runs.
*   **Detailed History**: Shows a table of the last 10 pipeline runs with exit codes for different stages (test, build, smoke).
*   **Release Notes**: Displays the latest release notes generated from the pipeline.
*   **Failure Synopsis**: Provides the JSON output of the latest pipeline failure for quick debugging.
*   **Sentry Integration**: Captures errors in real-time and sends them to a Sentry dashboard for analysis. Includes a test button to verify the integration.
*   **Containerized**: Includes a `Dockerfile` to easily containerize and deploy the dashboard.

## How It Works

The dashboard reads data from several JSON files located in the `logs/` directory. These files are generated and updated by the CI/CD pipeline scripts (`run_pipeline.ps1`, `post_pipeline.py`, etc.).

*   `logs/runs.json`: Contains a history of all pipeline runs.
*   `logs/release_notes.json`: Stores the latest release notes.
*   `logs/failure_synopsis.json`: Contains a summary of the most recent pipeline failure.

## Project Structure

| File                 | Description                                                              |
| -------------------- | ------------------------------------------------------------------------ |
| `dashboard.py`       | The main Streamlit application file for the dashboard.                   |
| `requirements.txt`   | A list of Python dependencies for the project.                           |
| `.env`               | Environment variables file (e.g., for Sentry DSN).                       |
| `Dockerfile`         | Defines the Docker image for the application.                            |
| `pipeline.ps1`       | The main CI/CD pipeline script.                                          |
| `run_pipeline.ps1`   | A script to execute the CI/CD pipeline.                                  |
| `post_pipeline.py`   | A script that likely runs after the pipeline to aggregate logs.          |
| `test_app.py`        | Contains unit tests for the application.                                 |
| `smoke_test.py`      | A simple test to verify that the application is running.                 |
| `logs/`              | Directory containing logs and data files for the dashboard.              |

## Prerequisites

Before you begin, ensure you have the following installed:

*   [Python 3.8+](https://www.python.org/downloads/)
*   [Docker](https://www.docker.com/get-started)
*   [PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root of the project and add your Sentry DSN:

```
SENTRY_DSN="your_sentry_dsn_here"
```

## Usage

### Running the Dashboard

To start the dashboard application, run:

```bash
streamlit run dashboard.py
```

The dashboard will be available at `http://localhost:8501`.

### Running the CI/CD Pipeline

To populate the dashboard with data, you need to execute the CI/CD pipeline. This will generate the log files that the dashboard reads.

```powershell
./run_pipeline.ps1
```

After the pipeline runs, refresh the dashboard to see the updated data.
