import os
import random
import math
import save_load
import unittest

class Storage_Stress(unittest.TestCase):
    def setUp(self):
        self.sl = save_load.StartMenu()
        self.old_save = self.sl.load(file_name='master_save_file')
        self.sl.save(items=self.old_save, file_name='../temp_save')
        print(os.getcwd())
    def tearDown(self):
        self.sl.save(items=self.old_save, file_name='../master_save_file')
    
    def test_01_1000_cases(self):
        self.new_save = {}
        for i in range(1000):
            random.seed(i)
            self.new_save[str(i)] = { 'horizontal' : random.random() * 180.0, 'vertical' : random.random() * 180.0 }
        self.sl.save(items=self.new_save, file_name='../master_save_file')
        os.system('py presentation_example.py')
        input("Press enter to continue:")

        self.sl.save(items=self.old_save, file_name='../master_save_file')

if __name__ == '__main__':
    unittest.main()