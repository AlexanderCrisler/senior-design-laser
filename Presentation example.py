import tkinter as tk
#import Phidgets_Controller as phidget_controller

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
        self.mappings = {"apple": {"x": 4.86, "y": 2.3}, "banana": {"x": 2.2, "y": -.15}}
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

    def add_item(self):
        root1 = tk.Tk()
        add_item_gui = add_item_popup(root1)
        root1.wait_window(root1)
        #TODO check if root1 closed correctly, then run the change laser
        #TODO add name, x, y to dictionary

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
        #self.wm_title("Add New Item")
        #self.geometry("300x300")
        
        self.closed=False
        
        self.name_label = tk.Label(master, text="Name:", font=("Arial", 20))
        self.name_label.place(relx=.1, rely=.15, relwidth=.25, relheight=.15)
        
        self.name_input = tk.Entry(master, font=("Arial", 20))
        self.name_input.place(relx=.375,rely=.15,relwidth=.5,relheight=.15)
        
        self.final_button = tk.Button(master, command=self.select_location, text="Select Location", font=("Arial", 20))
        self.final_button.place(relx= .35, rely=.75, relwidth=.3, relheight=.2)
    def select_location(self):
        self.name = self.name_input.get()
        self.closed=True
        self.master.destroy()

root = tk.Tk()
my_gui = laser_guides(root)
root.mainloop()
