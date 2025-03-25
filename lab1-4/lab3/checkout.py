import sys
from pydriller import Git

gr=Git(sys.argv[1])
gr.checkout(sys.argv[2])
