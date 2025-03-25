#!/bin/bash

REPO_NAME="textual"
RESULTS_DIR="../bandit_results/$REPO_NAME"
mkdir -p "$RESULTS_DIR"
CSV_FILE="$RESULTS_DIR/bandit_results_textual.csv"

echo "commit,high_conf,medium_conf,low_conf,high_sev,med_sev,low_sev,unique_cwes,unique_cwe_ids" > "$CSV_FILE"

git log --no-merges --format="%H" -n 100 > "$RESULTS_DIR/commits.txt"

while read commit; do
    echo "Checking commit: $commit"
    git checkout -f "$commit"
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    bandit -r . --exit-zero -f json -o temp_bandit.json || { 
        echo "Bandit failed for commit $commit. Skipping." 
        continue
    }
    if [ -s temp_bandit.json ]; then
        jq -r --arg commit "$commit" '
        [
          $commit,
          ([.results[] | select(.issue_confidence == "HIGH")] | length),
         ([.results[] | select(.issue_confidence == "MEDIUM")] | length),
         ([.results[] | select(.issue_confidence == "LOW")] | length),
          ([.results[] | select(.issue_severity == "HIGH")] | length),
          ([.results[] | select(.issue_severity == "MEDIUM")] | length),
          ([.results[] | select(.issue_severity == "LOW")] | length),
          ([.results[].issue_cwe.id] | unique | length),
          ([.results[].issue_cwe.id] | unique | join("|"))
        ] | @csv' temp_bandit.json >> "$CSV_FILE"
    else
        echo "$commit,ERROR,ERROR,ERROR,ERROR,ERROR" >> "$CSV_FILE"
    fi
    rm -f temp_bandit.json
done < "$RESULTS_DIR/commits.txt"

git checkout master 

echo "Bandit analysis complete. CSV file is stored at $CSV_FILE"
