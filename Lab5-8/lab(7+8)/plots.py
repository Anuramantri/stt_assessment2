import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"\\wsl.localhost\Ubuntu\home\anura2004\bandit_results_scrapy\scrapy\bandit_results_scrapy.csv")  

plt.figure(figsize=(12, 6))
plt.plot(df["commit"], df["med_sev"], label='Medium Severity', color='orange')
plt.plot(df["commit"], df["high_sev"], label='High Severity', color='red')

plt.plot(df["commit"], df["low_sev"], label='Low Severity', color='yellow')

plt.xlabel('Commit Hash')
plt.ylabel('Number of Issues')
plt.title('Trend of Vulnerabilities Over Commits (Severity)')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(df["commit"], df["high_conf"], label='High Confidence', color='blue')
plt.plot(df["commit"], df["medium_conf"], label='Medium Confidence', color='indigo')
plt.plot(df["commit"], df["low_conf"], label='Low Confidence', color='green')

plt.xlabel('Commit Hash')
plt.ylabel('Number of Issues')
plt.title('Trend of Vulnerabilities Over Commits (Confidence)')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.show()

