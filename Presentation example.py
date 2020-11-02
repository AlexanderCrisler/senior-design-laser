import tkinter as tk
import time
import keyboard #py -m pip install keyboard

class laser_guides:
    def __init__(self, master):
        # Widgets to be used
        self.master = master
        master.attributes('-fullscreen', True)
        self.infobox = tk.Label(master, font=("Arial", 20))
        self.entry = tk.Entry(master, font="Arial 20")
        self.listbox = tk.Listbox(master, font=("Arial", 20))
        
        self.exitbutton = tk.Button(master, text='Exit', command=master.destroy, font=("Arial", 30))
        ############### hardcoded for testing
        self.mappings = {"apple": {"x": 4.86, "y": 2.3}, "banana": {"x": 2.2, "y": -.15}}
        ###############
        
        
        # Widgets placement
        self.listbox.place(relx=.01, rely=.1, relwidth=.4, relheight=.7)
        self.infobox.place(relx=.45, rely=.1, relwidth=.5, relheight=.5)
        self.entry.place(relx=.01, rely=.05)
        self.exitbutton.place(relx=.55, rely=.8, relwidth=.1, relheight=.05)
        
        # Bindings for widgets
        self.listbox_update(self.mappings)
        self.entry.bind("<KeyRelease>", self.on_keyrelease)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.master.bind("<Key>", self.keypressed)

    def keypressed(self, event):
        #print(event.keysym)
        

        #key = event.keysym
        start = time.time()
        sensitivity = 0
        
        # ARROWKEY Directional Controls
        while keyboard.is_pressed('up'):
            current = time.time()
            sensitivity = current - start + 1
            print(f'up {sensitivity}')
        while keyboard.is_pressed('left'):
            current = time.time()
            sensitivity = current - start + 1
            print(f'left {sensitivity}')
        while keyboard.is_pressed('down'):
            current = time.time()
            sensitivity = current - start + 1
            print(f'down {sensitivity}')
        while keyboard.is_pressed('right'):
            current = time.time()
            sensitivity = current - start + 1
            print(f'right {sensitivity}')
        
        
        """
        while event.keysym == 'Up':             #UP
            current = time.time()
            sensitivity = current - start
            print(f'UP {sensitivity}')
            event.keysym = None       
            time.sleep(1)   
        while event.keysym == 'Left':           #LEFT
            current = time.time()
            sensitivity = current - start
            print(f'LEFT {sensitivity}')
        while event.keysym == 'Down':           #DOWN
            current = time.time()
            sensitivity = current - start
            print(f'DOWN {sensitivity}')
        while event.keysym == 'Right':           #RIGHT
            current = time.time()
            sensitivity = current - start
            print(f'RIGHT {sensitivity}')
        sensitivity = 0
        """
    """
    def _sensitivityCt(start):
        current = time.time()

        sensitivity = current - start
        #TODO pass sensitivity to keypressed, call jason's funciton
        #1) get current position
        #2) add degrees*sensitivity
    """

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


root = tk.Tk()
my_gui = laser_guides(root)
root.mainloop()
