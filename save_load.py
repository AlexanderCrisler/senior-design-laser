import json

#Reads json information from file given file name. Returns as dictionary.
#   file_name : Name of file to be opened and read from.
def load_file_name(file_name) -> dict:
    try:
        read_file = open(file_name, 'r')
        items = json.load(read_file)
        read_file.close()
        return items
    except:
        return None

#Reads json information from the file, returns as dictionary.
#   read_file : File object that is open to be read.
def load_file(read_file) -> dict:
    try:
        items = json.load(read_file)
        return items
    except:
        return None

#Saves dictionary to file in json format. Returns if no exceptions are raised.
#   item_dict : Dictionary of items to be saved in json format.
#   write_file : File object that is open to be written to.
def save_file(items_dict, write_file) -> bool:
    try:
        json.dump(items_dict, write_file)
        return True
    except:
        return False

#Saves dictionary to file given file name. Saves in json format. Returns True if no exceptions are raised.
#   items_dict : Dictionary of items to be saved in json format.
#   write_file_name : File name to be opened and written to.
def save_file_name(items_dict, write_file_name) -> bool:
    try:
        write_file = open(write_file_name, 'w')
        json.dump(items_dict, write_file)
        write_file.close()
        return True
    except:
        return False




