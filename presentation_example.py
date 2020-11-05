import tkinter as tk
import time
import keyboard #py -m pip install keyboard
import save_load

from phidgets_controller import LaserSystem

phidgets_ctlr = LaserSystem()

def move_servo_position(x_dir, y_dir, sensitivity=1):
    if x_dir == 1:
        x_pos = phidgets_ctlr.Get_TargetPosition()[0] + (.01 * sensitivity)
    elif x_dir == -1:
        x_pos = phidgets_ctlr.Get_TargetPosition()[0] - (.01 * sensitivity)

    if y_dir == 1:
        y_pos = phidgets_ctlr.Get_TargetPosition()[1] + (.01 * sensitivity)
    elif y_dir == -1:
        y_pos = phidgets_ctlr.Get_TargetPosition()[1] - (.01 * sensitivity)

    phidgets_ctlr.SetPosition(x_pos, y_pos)
    print(phidgets_ctlr.Get_Angle())

def set_servo_position(x_pos, y_pos):
    phidgets_ctlr.SetPosition(x_pos, y_pos)

class laser_guides:
    def __init__(self, master):
        # Widgets to be used
        self.master = master
        master.attributes('-fullscreen', True)
        self.infobox = tk.Label(master, font=("Arial", 20))
        self.entry = tk.Entry(master, font="Arial 20")
        self.listbox = tk.Listbox(master, font=("Arial", 20))
        
        self.addbutton = tk.Button(master, text='Add Item', command=self.add_item, font=("Arial", 30))
        self.exitbutton = tk.Button(master, text='Exit', command=master.destroy, font=("Arial", 30))
        ############### hardcoded for testing
        self.mappings = all_items
        ###############
        
        
        # Widgets placement
        self.listbox.place(relx=.01, rely=.1, relwidth=.4, relheight=.7)
        self.infobox.place(relx=.45, rely=.1, relwidth=.5, relheight=.5)
        self.entry.place(relx=.01, rely=.05)
        self.exitbutton.place(relx=.55, rely=.8, relwidth=.1, relheight=.05)
        self.addbutton.place(relx=.75, rely=.8, relwidth=.15, relheight=.05)

        # Bindings for widgets
        self.listbox_update(self.mappings)
        self.entry.bind("<KeyRelease>", self.on_keyrelease)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.master.bind("<Key>", self.keypressed)

    
    # Tracking the keys pressed
    def keypressed(self, event):
        #print(event.keysym)
        start = time.time()
        sensitivity = 0      # Sensitivity of the laser movement

        # ARROWKEY Directional Controls
        while keyboard.is_pressed('up'):
            current = time.time()
            sensitivity = current - start + 1
            #print(f'up {sensitivity}')
            move_servo_position(x_dir=0, y_dir=1, sensitivity=sensitivity)

        while keyboard.is_pressed('left'):
            current = time.time()
            sensitivity = current - start + 1
            #print(f'left {sensitivity}')
            move_servo_position(x_dir=-1, y_dir=0, sensitivity=sensitivity)

        while keyboard.is_pressed('down'):
            current = time.time()
            sensitivity = current - start + 1
            #print(f'down {sensitivity}')
            move_servo_position(x_dir=0, y_dir=-1, sensitivity=sensitivity)

        while keyboard.is_pressed('right'):
            current = time.time()
            sensitivity = current - start + 1
            #print(f'right {sensitivity}')
            move_servo_position(x_dir=1, y_dir=0, sensitivity=sensitivity)

    
    #Event for add item button press.
    def add_item(self):
        root1 = tk.Tk()
        add_item_gui = add_item_popup(root1)
        root1.wait_window(root1)
        #Checks if the form was closed correctly.
        if add_item_gui.closed:
            #TODO: Get x,y coords. Popup gui.
            
            root2 = tk.Tk()
            select_location_gui = move_laser_popup(root2)
            root2.wait_window(root2)
            name = add_item_gui.name
            all_items[name] = {'x': select_location_gui.x, 'y': select_location_gui.y}
            self.mappings = all_items
            self.listbox_update(self.mappings)


    # Event for search bar
    def on_keyrelease(self, event):
        # Get text from search bar
        self.value = event.widget.get()
        self.value = self.value.strip().lower()
        
        # Get objects from list that match search text
        if self.value == '':
            self.data = self.mappings
        else:
            self.data = []
            for self.item in self.mappings:
                if self.value in self.item.lower():
                    self.data.append(self.item)
        
        # Displays the items in list that match search text
        self.listbox_update(self.data)


    def listbox_update(self, data):
        # Deletes what's in the listbox
        self.listbox.delete(0, 'end')
        
        # Sorts alphabetically
        data = sorted(data, key=str.lower)

        # Inserts items in to listbox
        for item in data:
            self.listbox.insert('end', item)


    # Event for clicking on item in listbox
    def on_select(self, event):
        # Grabs item from listbox and displays item with its coordinates
        try:
            item = event.widget.get(event.widget.curselection())
            dict_item = self.mappings[item]
            self.infobox['text'] = (item + "\nx coordinate: " + str(dict_item["x"]) + "\ny coordinate: " + str(dict_item["y"]) + "\n")
        except:
            print("No value in listbox selected")


class add_item_popup:
    def __init__(self, master):
        self.master = master
        master.title("Add New Item")
        master.geometry("400x400")
        
        self.closed=False
        
        self.name_label = tk.Label(master, text="Name:", font=("Arial", 20))
        self.name_label.place(relx=.1, rely=.15, relwidth=.25, relheight=.15)
        
        self.name_input = tk.Entry(master, font=("Arial", 20))
        self.name_input.place(relx=.355,rely=.15,relwidth=.5,relheight=.15)
        
        self.final_button = tk.Button(master, command=self.select_location, text="Select Location", font=("Arial", 20))
        self.final_button.place(relx= .25, rely=.75, relwidth=.5, relheight=.2)
    
    #Event for select location button press
    def select_location(self):
        self.name = self.name_input.get()
        self.closed=True
        self.master.destroy()

class move_laser_popup:
    def __init__(self, master):
        self.master = master
        master.title("Select Laser Location")
        master.geometry("400x400")
        
        self.closed=False
        self.x = 0
        self.y = 0
        
        
        self.left_button = tk.Button(master, command=self.left_button_click, text="<", font=("Arial", 20))
        self.left_button.place(relx=0, rely=.2, relwidth=.2, relheight=.6)
        
        self.right_button = tk.Button(master, command=self.right_button_click, text=">", font=("Arial", 20))
        self.right_button.place(relx=.8, rely=.2, relwidth=.2, relheight=.6)
        
        self.up_button = tk.Button(master, command=self.up_button_click, text="/\\", font=("Arial", 20))
        self.up_button.place(relx=.2, rely=0, relwidth=.6, relheight=.2)
        
        self.down_button = tk.Button(master, command=self.down_button_click, text="\\/", font=("Arial", 20))
        self.down_button.place(relx=.2, rely=.8, relwidth=.6, relheight=.2)
        
        self.set_button = tk.Button(master, command=self.set_location, text="Set", font=("Arial", 20))
        self.set_button.place(relx=.35, rely=.35, relwidth=.3, relheight=.3)
        
    def left_button_click(self):
        self.x = self.x - 1
    
    def right_button_click(self):
        self.x = self.x + 1
        
    def up_button_click(self):
        self.y = self.x + 1
        
    def down_button_click(self):
        self.y = self.x - 1
    
    def set_location(self):
        self.closed=True
        self.master.destroy()
        
start_menu = save_load.StartMenu()
all_items = start_menu.load(file_name='master_save_file')
root = tk.Tk()
my_gui = laser_guides(root)
root.mainloop()