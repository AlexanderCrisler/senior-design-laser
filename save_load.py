import json

"""
items = {"apple": {"x": 4.86, "y": 2.3}, "banana": {"x": 2.2, "y": -.15}} 

afile = open("person.json", 'w')
json.dump(items, afile, sort_keys=True, indent=4)
afile.close()



bfile = open("person.json", 'r')
newitems = json.load(bfile)
bfile.close()

print(newitems)
"""

# Name
# XY coordinate
# saved in ever expanding JSON file
# using dictionary of dictionaries

#TODO: function to save/append to JSON file
#TODO: function to read from existing JSON file
#TODO: function to delete saved object

def save_object(name, x, y, list_of_saved_objects):
    """Saving a newly created object to list of saved objects"""
    new_dict = {"name": name, "x": x, "y": y}

    # Adding the new dictionary to the working list of all objects
    list_of_saved_objects.append(new_dict)
    list_of_saved_objects = sorted(list_of_saved_objects, key = lambda i: (i['name']))

    # Adding the new dictionary to the save file
    file_name = open("stored_objects.json", 'w')
    json.dump(list_of_saved_objects, file_name, sort_keys=True, indent=4)
    file_name.close()

    return


def load_saved_objects():
    """Loading the save file to a dictionary"""
    # Handling a non existent file
    try:
        file_name = open("stored_objects.json", 'r')
    except:
        file_name = open("stored_objects.json", 'x')
        #save_object("origin", 90, 90, list_of_saved_objects) #need to take list of saved objects out of function call

    # Handling an empty file
    #TODO: change to if satement or except for only the expected exception
    try:
        new_list_of_dicts = json.load(file_name)
    except:
        return [{}]

    file_name.close()
    return new_list_of_dicts

list_of_saved_objects = load_saved_objects()

print(list_of_saved_objects)

user_name = input("name:")
user_x = input("x-value:")
user_y = input("y-value:")

list_of_saved_objects = save_object(user_name, user_x, user_y, list_of_saved_objects)

