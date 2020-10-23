import json

items = {"apple": {"x": 4.86, "y": 2.3}, "banana": {"x": 2.2, "y": -.15}} 

afile = open("person", 'w')
json.dump(items, afile)
afile.close()



bfile = open("person", 'r')
newitems = json.load(bfile)
bfile.close()

print(newitems)
