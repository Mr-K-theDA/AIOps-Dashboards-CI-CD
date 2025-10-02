#!/usr/bin/env python3
"""
Simple smoke test after Docker build.
Assumes the Docker image 'myapp' has been built and can run a basic command.
"""

import subprocess
import sys

def smoke_test():
    try:
        # Run docker container and check if it starts
        result = subprocess.run(['docker', 'run', '--rm', 'myapp', 'echo', 'smoke test passed'],
                                capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and 'smoke test passed' in result.stdout:
            print("Smoke test passed!")
            return 0
        else:
            print("Smoke test failed: unexpected output or exit code", result.returncode)
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
            return 1
    except subprocess.TimeoutExpired:
        print("Smoke test failed: timeout")
        return 1
    except Exception as e:
        print(f"Smoke test failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(smoke_test())
