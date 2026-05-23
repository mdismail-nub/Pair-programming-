import subprocess
import tempfile
import time

BLOCKED_IMPORTS = ["import os", "import sys", "import subprocess", "import socket", "from os", "from sys", "from subprocess", "from socket"]


def run_python_code(code: str) -> dict:
    for blocked in BLOCKED_IMPORTS:
        if blocked in code:
            return {"output": "", "error": f"Blocked import detected: {blocked}", "execution_time": 0.0}

    start = time.time()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=True) as tmp:
        tmp.write(code)
        tmp.flush()
        try:
            result = subprocess.run(
                ["python", tmp.name],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return {
                "output": result.stdout.strip(),
                "error": result.stderr.strip(),
                "execution_time": round(time.time() - start, 4),
            }
        except subprocess.TimeoutExpired:
            return {
                "output": "",
                "error": "Execution timed out after 5 seconds",
                "execution_time": round(time.time() - start, 4),
            }
