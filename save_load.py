import json
import io

# Tests for this class can be run from 'test_save_load.py'
# #TODO: function to delete saved object

class StartMenu():
    def save(self, items={}, write_file=None, file_name=None) -> bool:
        _sort_dict(items)

        if write_file:
            try:
                json.dump(items, write_file)
                return True
            except Exception as e:
                print(e)
                pass
            finally:
                write_file.close()
        elif file_name:
            try:
                write_file = open(file_name, 'w')
                json.dump(items, write_file)
                return True
            except Exception as e:
                print(e)
                pass
            finally:
                if write_file:
                    write_file.close()
        else:
            write_file.close()
        
        return False

    def load(self, read_file=None, file_name=None) -> dict:
        if read_file:
            try:
                return json.load(read_file)
            except Exception as e:
                print(e)
                pass
            finally:
                read_file.close()
        elif file_name:
            try:
                read_file = open(file_name, 'r')
                items = json.load(read_file)
                read_file.close()
                return items
            except Exception as e:
                print(e)
                pass
            finally:
                if read_file:
                    read_file.close()
        else:
            write_file.close()

        return {}

"""
def load_file(read_file) -> dict:
    Reads json information from file name.
    #   read_file : Either Name of file to be opened and read from or File object that is open to be read.
    if isinstance(read_file, io.TextIOWrapper) and read_file.mode == 'r':
        items = json.load(read_file)
        return items
    elif type(read_file) == str:
        try:
            read_file = open(read_file, 'r')
            items = json.load(read_file)
            read_file.close()
            return items
        except FileNotFoundError:
            save_file({}, read_file)
            return {}
        except json.JSONDecodeError:
            save_file({}, read_file)
            return {}
    else:
        return None


def save_file(items_dict, write_file) -> bool:
    #Saves dictionary to file in json format. Returns if no exceptions are raised.
    #   items_dict : Dictionary of items to be saved in json format.
    #   write_file : Either Name of file to be written or File object that is open to be written to.

    # Sorting the dictionary
    _sort_dict(items_dict)

    if isinstance(write_file, io.TextIOWrapper) and write_file.mode == 'w':
        json.dump(items_dict, write_file, sort_keys=True, indent=4)
        return True
    elif type(write_file) == str:
            write_file = open(write_file, 'w')

            json.dump(items_dict, write_file, sort_keys=True, indent=4)
            write_file.close()
            return True
    else:
        return False
"""

def _sort_dict(items_dict):
    if items_dict:
        return {key: val for key, val in sorted(items_dict.items(), key = lambda ele: ele[0])}
    else:
        return {}