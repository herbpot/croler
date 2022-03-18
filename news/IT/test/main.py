import glob
import json
list = glob.glob("../*.json")
print(list)
# d = {}
# d.

for i in list:
    with open(i,'r') as f:
        ij = json.load(f)
        ij.items()[0]