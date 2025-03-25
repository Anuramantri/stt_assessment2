import os
import sys 
import csv
import subprocess
from pydriller import Repository
        
columns = [
    'old_file_path', 'new_file_path', 'commit_SHA',
    'parent_commit_SHA', 'commit_message',
     'diff_myers', 'diff_histogram'
]

rows = []
count = 0
last_n = 500

commits = []
repo_path= sys.argv[1]
output_csv= f"{repo_path}_results/commits_info.csv"

for x in Repository(sys.argv[1], only_no_merge=True, order='reverse').traverse_commits():
    if x.in_main_branch:
        count += 1
        commits.append(x)
        if count == last_n:
            break


commits.reverse()

def run_git_diff(diff_type, repo_path, parent_sha, commit_sha, file_path):
    """
    Run git diff command for Myers or Histogram diff (ignoring whitespace) and return the output.
    """
    try:
        cmd = [
            "git", "-C", repo_path, "diff",
            parent_sha, commit_sha, "--", file_path,
            "--ignore-all-space"
        ]
        if diff_type == "histogram":
            cmd.insert(4, "--diff-algorithm=histogram")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

for i, commit in enumerate(commits):
    print(f"{i + 1}/{len(commits)}] Mining commit {commit.hash}")

    for f in commit.modified_files:
        old_path = f.old_path or "N/A"
        new_path = f.new_path or "N/A"

        if old_path == "N/A" and new_path == "N/A":
            continue

        parent_sha = commit.parents[0] if commit.parents else "N/A"
        if parent_sha == "N/A":
            continue

        myers_diff = run_git_diff("myers", repo_path, parent_sha, commit.hash, new_path)
        hist_diff = run_git_diff("histogram", repo_path, parent_sha, commit.hash, new_path)

        rows.append([
            old_path, new_path,
            commit.hash,
            parent_sha,
            commit.msg,
            myers_diff,
            hist_diff
        ])

# Write rows to CSV
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Data written to {output_csv}")
