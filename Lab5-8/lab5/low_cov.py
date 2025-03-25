import json

coverage_file = "coverage_tmp.json"
output_file = "low_coverage_files.txt"

with open(coverage_file, "r") as f:
    data = json.load(f)

files = data.get("files", {})


low_coverage_files = []
for file, details in files.items():
    summary = details.get("summary", {}) 
    percent_covered = summary.get("percent_covered", 0)  

    if percent_covered < 75:  
        low_coverage_files.append((file, percent_covered))

total_files = len(files)
low_coverage_count = len(low_coverage_files)

with open(output_file, "w") as f:
    for file, coverage in low_coverage_files:
        f.write(f"{file}: {coverage:.2f}%\n")
average_low_coverage = sum(coverage for _, coverage in low_coverage_files) / low_coverage_count

print(f"Low coverage files found: {low_coverage_count}, Total files: {total_files}")
print(f"Average coverage across low coverage files: {average_low_coverage:.2f}%")
print(f"Saved low-coverage file list to {output_file}")
