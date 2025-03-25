import json
import matplotlib.pyplot as plt
import re

coverage_file = "coverage_tmp.json"

with open(coverage_file, "r") as f:
    data = json.load(f)
totals = data.get("totals", {})
print("\nCoverage Summary:")
for key, value in totals.items():
    print(f"{key}: {value}")
line_coverage = totals.get("percent_covered", 0)
covered_branches = totals.get("covered_branches", 0)
num_branches = totals.get("num_branches", 0)
branch_coverage = (covered_branches / num_branches) * 100
print(f"computed branch coverage: {branch_coverage:.2f}%")
pytest_output_file = "pytest_output.txt"
func_coverages = []

with open(pytest_output_file, "r") as f:
    for line in f:
        match = re.search(r"(\d+)%$", line.strip()) 
        if match:
            func_coverages.append(int(match.group(1)))
avg_func_coverage = sum(func_coverages) / len(func_coverages)

print(f"computed function coverage: {avg_func_coverage:.2f}%")
categories = ["Line Coverage", "Branch Coverage", "Avg. Func Coverage"]
values = [line_coverage, branch_coverage, avg_func_coverage]

plt.figure(figsize=(6, 4))
bars = plt.bar(categories, values, color=["blue", "orange", "green"])

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}%", 
             ha="center", va="bottom", fontsize=12, fontweight="bold")

plt.ylim(0, 100)
plt.ylabel("Coverage (%)")
plt.title("Coverage Comparison (Line, Branch, Function)")
plt.grid(axis="y", linestyle="--", alpha=0.7)

output_file = "coverage_visualization.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")

print(f"\nCoverage visualization saved as {output_file}")

