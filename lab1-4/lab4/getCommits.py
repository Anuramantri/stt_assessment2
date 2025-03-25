import sys
from pydriller import Repository
count=0
last_n=500
commit_reverse=[]
for commit in Repository(sys.argv[1],only_no_merge=True,order='reverse').traverse_commits():
  if (commit.in_main_branch==True):
    count=count+1
    #print(commit.hash)
    commit_reverse.append(commit.hash)
    if count == last_n:
      break
      
in_order = []
for value in range(len(commit_reverse)):
  in_order.append(commit_reverse.pop())
  
in_order='\n'.join(in_order)
print(in_order)
