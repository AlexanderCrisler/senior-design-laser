import os
import random
import save_load
import math

sl = save_load.StartMenu()
old_save = sl.load(file_name='master_save_file')



new_save = {}

for i in range(1000):
    random.seed(i)
    new_save[str(i)] = { 'horizontal' : random.random() * 180.0, 'vertical' : random.random() * 180.0 }

sl.save(items=old_save, file_name='temp_save')    
sl.save(items=new_save, file_name='master_save_file')

os.system('py presentation_example.py')


x = input("Press enter to continue:")

sl.save(items=old_save, file_name='master_save_file')