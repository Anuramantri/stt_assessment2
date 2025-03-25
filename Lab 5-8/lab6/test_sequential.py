import os
import subprocess
import time
from datetime import datetime

TEST_SUITE_COMMAND = "pytest --disable-warnings"
RESULTS_DIR = "sequential_test_results"
RUNS = 10  
FINAL_RUNS = 3  
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_test_suite(run_id):
    """Run the test suite and save results."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = os.path.join(RESULTS_DIR, f"run_{run_id}_{timestamp}.txt")

    exclude_file = os.path.join(RESULTS_DIR, "exclude.txt")
    modified_command = TEST_SUITE_COMMAND
    if os.path.exists(exclude_file):
        with open(exclude_file, "r") as f:
            excluded_tests = [line.strip() for line in f if line.strip()]
        for test in excluded_tests:
            modified_command += f" --deselect={test}"
    
    start_time = time.time()
    with open(result_file, "w") as f:
        process = subprocess.run(modified_command.split(), stdout=f, stderr=subprocess.STDOUT)
    end_time = time.time()
    
    return result_file, process.returncode, end_time - start_time

def parse_test_results(result_file):
    """Parse the test results file to identify failing or flaky tests."""
    failed_tests = set()
    with open(result_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "FAILED" in line and "::" in line:
                test_name = line.split("FAILED ")[1].split("::")[0].strip()
                failed_tests.add(test_name)
    return failed_tests

def execute_sequential_tests(runs):
    """Execute the test suite sequentially and collect results."""
    all_failed_tests = {}
    execution_times = []
    
    for i in range(1, runs + 1):
        print(f"Running test suite (Run {i}/{runs})...")
        result_file, return_code, exec_time = run_test_suite(i)
        execution_times.append(exec_time)
        
        if return_code != 0:  
            failed_tests = parse_test_results(result_file)
            for test in failed_tests:
                if test not in all_failed_tests:
                    all_failed_tests[test] = 0
                all_failed_tests[test] += 1
    
    return all_failed_tests, execution_times

def identify_flaky_tests(all_failed_tests):
    flaky_tests = {test for test, count in all_failed_tests.items() if count > 0 and count < RUNS}
    return flaky_tests

def remove_failing_and_flaky_tests(failing_and_flaky_tests):
    exclude_file = os.path.join(RESULTS_DIR, "exclude.txt")
    with open(exclude_file, "w") as f:
        for test in failing_and_flaky_tests:
            f.write(f"{test}\n")
    
    print(f"Excluding {len(failing_and_flaky_tests)} tests. Exclude list saved to {exclude_file}.")
def calculate_average_execution_time(times):
    return sum(times) / len(times)
if __name__ == "__main__":
    print("Executing initial sequential tests...")
    all_failed_tests, initial_execution_times = execute_sequential_tests(RUNS)
    flaky_tests = identify_flaky_tests(all_failed_tests)
    failing_and_flaky_tests = set(all_failed_tests.keys()).union(flaky_tests)
    print(f"Identified {len(all_failed_tests)} failing tests.")
    print(f"Identified {len(flaky_tests)} flaky tests.")
    if failing_and_flaky_tests:
        print(f"Total {len(failing_and_flaky_tests)} failing/flaky tests identified. Removing these from the test suite...")
        remove_failing_and_flaky_tests(failing_and_flaky_tests)
        print("Executing final sequential tests after removing failing/flaky tests...")
        _, final_execution_times = execute_sequential_tests(FINAL_RUNS)
        Tseq = calculate_average_execution_time(final_execution_times)
        print(f"Average execution time (Tseq) after removing failing/flaky tests: {Tseq:.2f} seconds.")
        summary_file = os.path.join(RESULTS_DIR, "summary.txt")
        with open(summary_file, "w") as f:
            f.write(f"Tseq: {Tseq:.2f} seconds\n")
            f.write("Failing/Flaky Tests Removed:\n")
            for test in failing_and_flaky_tests:
                f.write(f"{test}\n")
        print(f"Summary saved to {summary_file}.")
    else:
        print("No failing or flaky tests identified. Test suite is stable.")

