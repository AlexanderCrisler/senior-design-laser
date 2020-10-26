import unittest
import json
import os

from save_load import StartMenu

class LoadTestCase(unittest.TestCase):
    """Tests for 'save_load.py'"""
    def setUp(self):
        self.startmenu = StartMenu()
        self.startmenu.save = self.startmenu.save
        self.startmenu.load = self.startmenu.load

        self.test_dict = {"apple": {"x": 4.86, "y": 2.3}, "banana": {"x": 2.2, "y": -0.15}}

        self.non_empty_file = open("non_empty_file.json", 'w')
        json.dump(self.test_dict, self.non_empty_file)
        self.non_empty_file.close()

        self.empty_file = open("empty_file.json", 'w')
        self.empty_file.close()

    
    def tearDown(self):
        os.remove("non_empty_file.json")
        os.remove("empty_file.json")
        
    
    def test_01_load_file(self):
        """What if the file object is used?"""
        file_object = open("non_empty_file.json", 'r')
        items_dict = self.startmenu.load(read_file=file_object, file_name=None)
        file_object.close()
        self.assertEqual(items_dict, self.test_dict)


    def test_02_load_file_name(self):
        """What if the name of the file is used?"""
        items_dict = self.startmenu.load(read_file=None, file_name="non_empty_file.json")
        self.assertEqual(items_dict, self.test_dict)
    

    def test_03_load_from_non_existant_file(self):
        """What if the file doesn't exist?"""
        items_dict = self.startmenu.load(read_file=None, file_name="non_existent_file.json")
        self.assertEqual(items_dict, {})

    
    def test_04_load_from_empty_file(self):
        """What if the file is empty?"""
        items_dict = self.startmenu.load(read_file=None, file_name="empty_file.json")
        self.assertEqual(items_dict, {})

    
    def test_05_load_from_write_file(self):
        """What if the file object is set to 'w'?"""
        file_object = open("non_empty_file.json", 'w')
        items_dict = self.startmenu.load(read_file=file_object, file_name=None)
        file_object.close()
        self.assertEqual(items_dict, {})
        
    
    def test_06_save_file_name(self):
        """What if the name of the file is used?"""
        self.assertTrue(self.startmenu.save(items=self.test_dict, write_file=None, file_name="non_empty_file.json"))

    
    def test_07_save_file(self):
        """What if the file object is used?"""
        file_object = open("non_empty_file.json", 'w')
        test = self.startmenu.save(items=self.test_dict, write_file=file_object, file_name=None)
        file_object.close()
        self.assertTrue(test)
        
    
    def test_08_save_to_read_file(self):
        """What if the file is opened as a read file?"""
        file_object = open("non_empty_file.json", 'r')
        test = self.startmenu.save(items=self.test_dict, write_file=file_object, file_name=None)
        file_object.close()
        self.assertFalse(test)


    def test_09_multiple_saves(self):
        """What if we save multiple times to the same file?"""
        self.assertTrue(self.startmenu.save(items=self.test_dict, write_file=None, file_name="non_empty_file.json"))
        self.assertTrue(self.startmenu.save(items=self.test_dict, write_file=None, file_name="non_empty_file.json"))
        self.assertTrue(self.startmenu.save(items=self.test_dict, write_file=None, file_name="non_empty_file.json"))
        items_dict = self.startmenu.load(read_file=None, file_name="non_empty_file.json")
        self.assertEqual(items_dict, self.test_dict)


    def test_10_load_save(self):
        """What if we load then save?"""
        file_object = open("non_empty_file.json", 'r')
        items_dict = self.startmenu.load(read_file=file_object, file_name=None)
        file_object.close()
        self.assertEqual(items_dict, self.test_dict)

        file_object = open("non_empty_file.json", 'w')
        test = self.startmenu.save(items=items_dict, write_file=file_object, file_name=None)
        file_object.close()
        self.assertTrue(test)


if __name__ == '__main__':
    unittest.main()


# Possible use cases:
# Saving file with file object
# Saving file with file name
# Loading file with file object
# Loading file with file name
# Saving multiple times during runtime
# Loading a file that doesn't exist
# Loading a file that doesn't have a dictionary
# Loading from a write file
# Saving to a read file
# Loading then saving to the same file