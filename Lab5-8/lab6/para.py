import os
import subprocess
import time
from collections import defaultdict
RESULTS_DIR = "parallel_test_results"
RUNS = 3 

PARALLEL_CONFIGS = [
    {'workers': '-n auto', 'threads': '--parallel-threads auto'},
    {'workers': '-n auto', 'threads': '--parallel-threads 1'},
    {'workers': '-n 1', 'threads': '--parallel-threads auto'},
    {'workers': '-n 1', 'threads': '--parallel-threads 1'}
]

DIST_MODES = ['--dist load', '--dist no']
os.makedirs(RESULTS_DIR, exist_ok=True)

def execute_parallel_tests(worker_config, thread_config, dist_mode, repetition):
    result_file = f"{RESULTS_DIR}/w{worker_config}_t{thread_config}_{dist_mode.replace(' ', '_')}_run_{repetition}.txt"
    command = f"pytest {worker_config} {thread_config} {dist_mode} --disable-warnings"
    start_time = time.time()
    with open(result_file, "w") as f:
        process = subprocess.run(command.split(), stdout=f, stderr=subprocess.STDOUT)
    end_time = time.time()

    return result_file, process.returncode, end_time - start_time

def parse_test_failures(result_file):
    failures = set()
    with open(result_file, 'r') as f:
        for line in f:
            if 'FAILED' in line and '::' in line:
                test_name = line.split('::')[1].split()[0]
                failures.add(test_name)
    return failures
execution_times = defaultdict(lambda: defaultdict(list))
failure_records = defaultdict(lambda: defaultdict(list))
flaky_test_records = defaultdict(lambda: defaultdict(set))
persistent_failures_records = defaultdict(lambda: defaultdict(set))
print("Executing parallel test runs...")

for config in PARALLEL_CONFIGS:
    for dist_mode in DIST_MODES:
        worker_config = config['workers']
        thread_config = config['threads']
        config_times = []
        test_failures = defaultdict(int)

        for repetition in range(1, RUNS + 1):
            print(f"Running tests with {worker_config}, {thread_config}, {dist_mode} (Run {repetition}/{RUNS})...")
            result_file, return_code, exec_time = execute_parallel_tests(worker_config, thread_config, dist_mode, repetition)
            config_times.append(exec_time)
            failures = parse_test_failures(result_file)
            for test in failures:
                test_failures[test] += 1  

            failure_records[f"{worker_config}_{thread_config}"][dist_mode].append(failures)
        Tpar = sum(config_times) / len(config_times)
        execution_times[f"{worker_config}_{thread_config}"][dist_mode] = Tpar
        print(f"Tpar for {worker_config}, {thread_config}, {dist_mode}: {Tpar:.4f} seconds")
        flaky_tests = {test for test, count in test_failures.items() if 0 < count < RUNS}
        persistent_failures = {test for test, count in test_failures.items() if count == RUNS}
        flaky_test_records[f"{worker_config}_{thread_config}"][dist_mode] = flaky_tests
        persistent_failures_records[f"{worker_config}_{thread_config}"][dist_mode] = persistent_failures

        with open(f"{RESULTS_DIR}/flaky_tests_{worker_config}_{thread_config}_{dist_mode.replace(' ', '_')}.txt", "w") as f:
            f.write("Flaky Tests:\n")
            for test in flaky_tests:
                f.write(f"{test}\n")
            f.write("\nPersistent Failures:\n")
            for test in persistent_failures:
                f.write(f"{test}\n")
                
summary_file = os.path.join(RESULTS_DIR, "summary.txt")
with open(summary_file, "w") as f:
    f.write("=== Parallel Test Execution Summary ===\n\n")
    for config, modes in execution_times.items():
        for mode, tpar in modes.items():
            f.write(f"Configuration: {config}, {mode}\n")
            f.write(f"  - Average Execution Time (Tpar): {tpar:.4f} seconds\n")
            flaky_tests = flaky_test_records[config][mode]
            if flaky_tests:
                f.write("  - Flaky Tests:\n")
                for test in flaky_tests:
                    f.write(f"    - {test}\n")
            else:
                f.write("  - No Flaky Tests\n")
            persistent_failures = persistent_failures_records[config][mode]
            if persistent_failures:
                f.write("  - Persistent Failures:\n")
                for test in persistent_failures:
                    f.write(f"    - {test}\n")
            else:
                f.write("  - No Persistent Failures\n")
            f.write("\n")
print("Execution completed. Results saved in 'para_test_results' directory.")

