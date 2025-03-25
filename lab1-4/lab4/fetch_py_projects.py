import requests
import time
import csv
import subprocess
from more_itertools import unique_everseen

columns = ["Project_name", "URL", "stars"]

rows = []

i=1 # page number
flag=1
pagebound=100
while (flag == 1):
 time.sleep(3)
 url1 = f"https://api.github.com/search/repositories?q=python+language:python&sort=stars&order=desc&page={i}"
 user_data = requests.get(url1).json()
 j=0
 stars_flag=1
 while (j < 30): # fetch 30 projects at a time
  if (i > pagebound) :
    flag=0
    break
  else:
    try:
     name=(user_data['items'][j]).get('full_name')
     url=(user_data['items'][j]).get('html_url')
     stars=str((user_data['items'][j]).get('stargazers_count'))
     stars_flag=int(stars)
     print (name, url, stars)
     rows.append([name, url, stars])
    except:
     pass
  j+=1
 i+=1

i=1 # page number 
flag=1
pagebound=100
while (flag == 1):
 time.sleep(3)
 url1 = f"https://api.github.com/search/repositories?q=python+language:python&sort=stars&order=asc&page={i}"
 user_data = requests.get(url1).json()
 j=0
 stars_flag=1
 while (j < 30): # fetch 30 projects at a time
  if (i > pagebound) :
    flag=0
    break
  else:
    try:
     name=(user_data['items'][j]).get('full_name')
     url=(user_data['items'][j]).get('html_url')
     stars=str((user_data['items'][j]).get('stargazers_count'))
     stars_flag=int(stars)
     print (name, url, stars)
     rows.append([name, url, stars])
    except:
     pass
  j+=1
 i+=1

i=1 # page number 
flag=1
pagebound=100
while (flag == 1):
 time.sleep(3)
 url1 = f"https://api.github.com/search/repositories?q=python+language:python&page={i}"
 user_data = requests.get(url1).json()
 j=0
 stars_flag=1
 while (j < 30): # fetch 30 projects at a time
  if (i > pagebound) :
    flag=0
    break
  else:
    try:
     name=(user_data['items'][j]).get('full_name')
     url=(user_data['items'][j]).get('html_url')
     stars=str((user_data['items'][j]).get('stargazers_count'))
     stars_flag=int(stars)
     print (name, url, stars)
     rows.append([name, url, stars])
    except:
     pass
  j+=1
 i+=1

rows=sorted(rows, key = lambda x: int(x[2]),reverse=True)
 
with open('py_projects.csv', 'a') as csvFile:
 writer = csv.writer(csvFile)
 writer.writerow(columns)
 writer.writerows(rows)

#remove duplicate rows

with open('py_projects.csv', 'r') as f, open('py_projects_unique.csv', 'w') as out_file:
 out_file.writelines(unique_everseen(f))

subprocess.run(["rm", "-f", "py_projects.csv"])
subprocess.run(["mv", "py_projects_unique.csv", "py_projects.csv"])
	
