import json

people = [{"name" : "Spencer", "languages" : ["English", "Spanish", "Italian"]},{"name": "Jason", "languages" : ["English", "Something"]}]

afile = open("person", 'w')
json.dump(people, afile)
afile.close()



bfile = open("person", 'r')
newpeople = json.load(bfile)
bfile.close()

for a, b in zip(people, newpeople):
    print(a)
    print(b)
    print('\n')
