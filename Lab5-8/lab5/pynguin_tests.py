import os
import subprocess
import signal

LOW_COVERAGE_FILE = "low_coverage_files.txt" 
OUTPUT_DIR = "test_suite_B"                
LOG_DIR = os.path.join(OUTPUT_DIR, "logs")
TIMEOUT = 30  # 30 sec timeout per module
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
with open(LOW_COVERAGE_FILE, "r") as f:
    low_coverage_files = [line.split(":")[0].strip() for line in f]
print(f"Found {len(low_coverage_files)} Python files with low coverage.")
def run_with_timeout(cmd, log_file, timeout=TIMEOUT):
    """Run a command with a timeout and log the output."""
    with open(log_file, "w") as log:
        process = subprocess.Popen(cmd, stdout=log, stderr=log)
        try:
            process.wait(timeout=timeout)
            return process.returncode
        except subprocess.TimeoutExpired:
            process.kill()
            log.write("\n[ERROR] Timeout expired for command:\n" + " ".join(cmd) + "\n")
            return -1
PROJECT_PATH = "."
for file in low_coverage_files:
    module_name = file.replace("/", ".").replace(".py", "")
    log_file = os.path.join(LOG_DIR, f"{module_name}.log")
    
    cmd = [
        "pynguin",
        "--project-path", PROJECT_PATH,
        "--module-name", module_name,
        "--output-path", OUTPUT_DIR
    ]

    print(f"Running: {' '.join(cmd)}")
    return_code = run_with_timeout(cmd, log_file)
    if return_code == 0:
        print(f"Successfully generated tests for {module_name}")
    else:
        print(f"Pynguin failed or timed out for {module_name}. Check logs at {log_file}")

