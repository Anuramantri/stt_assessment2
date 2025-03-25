import csv
import lizard
from pydriller import Repository
import subprocess
import pandas as pd
import sys 
import os

def git_diff(diff_type, repo_path, parent_sha, commit_sha, file_path):
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

def get_mcc_from_git(file_path, repo_path, commit_sha):
    try:
        cmd = ["git", "-C", repo_path, "show", f"{commit_sha}:{file_path}"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        analysis = lizard.analyze_file.analyze_source_code(file_path, result.stdout)
        mcc_value = sum(func.cyclomatic_complexity for func in analysis.function_list)
        print(f"File: {file_path} at {commit_sha}, MCC: {mcc_value}")
        return mcc_value
    except subprocess.CalledProcessError:
        print(f"Could not retrieve {file_path} at {commit_sha}")
        return None
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return None
        
columns = [
    'old_file_path', 'new_file_path', 'commit_SHA',
    'parent_commit_SHA', 'commit_message', 'diff_histogram', 'old_file_MCC', 'new_file_MCC'
]
rows = []
count = 0
last_n = 500  
commits = []
for commit in Repository(sys.argv[1], only_no_merge=True, order='reverse').traverse_commits():
    if commit.in_main_branch:
        count += 1
        commits.append(commit)
        if count == last_n:
            break

in_order = []
for value in range(len(commits)):
    in_order.append(commits.pop())

commits = in_order
i = -1

repo_path = sys.argv[1]

for commit in commits:
    i += 1
    print(f'[{i + 1}/{len(commits)}] Mining commit {sys.argv[1]} {commit.hash}')

    for m in commit.modified_files:
        old_file_path = m.old_path
        new_file_path = m.filename
        commit_sha = commit.hash
        parent_sha = commit.parents[0] if commit.parents else None
        commit_message = commit.msg

        if new_file_path is None and old_file_path is None:
            continue
        
        target_path = new_file_path
        if new_file_path is None:
            target_path = old_file_path

        diff_hist = git_diff("histogram", repo_path, parent_sha, commit_sha, target_path)
        print(new_file_path)
        old_file_MCC = None
        if old_file_path:
            old_file_MCC = get_mcc_from_git( old_file_path,repo_path,parent_sha)
        new_file_MCC = get_mcc_from_git(old_file_path,repo_path,commit_sha)
        rows.append([old_file_path, new_file_path, commit_sha, parent_sha, commit_message, diff_hist, old_file_MCC, new_file_MCC])

with open(sys.argv[1] + '_results/commits_info.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    if count == last_n:  
        writer.writerow(columns)
    writer.writerows(rows)