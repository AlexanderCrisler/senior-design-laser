import tkinter as tk

def on_keyrelease(event):
    
    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()
    
    # get data from test_list
    if value == '':
        data = mappings
    else:
        data = []
        for item in mappings:
            if value in item.lower():
                data.append(item)                

    # update data in listbox
    listbox_update(data)
    
    
def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')
    
    # sorting data 
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item)


def on_select(event):
    item = event.widget.get(event.widget.curselection())
    dict_item = mappings[item]
    infobox.delete("1.0", "end")
    infobox.insert(tk.END, item + "\nx coordinate: " + str(dict_item["x"]) + "\ny coordinate: " + str(dict_item["y"]) + "\n")
    print(dict_item["x"])
    print(dict_item["y"])
        


# --- main ---
mappings = {"apple": {"x": 4.86, "y": 2.3}, "banana": {"x": 2.2, "y": -.15}}

root = tk.Tk()
root.geometry("500x500")
entry = tk.Entry(root)
entry.place(x=20, y=50)
entry.bind('<KeyRelease>', on_keyrelease)

infobox = tk.Text(root)
infobox.place(x=200, y=100, width=275, height=300)
listbox = tk.Listbox(root)
listbox.place(x=20, y=100)
#listbox.bind('<Double-Button-1>', on_select)
listbox.bind('<<ListboxSelect>>', on_select)
listbox_update(mappings)

root.mainloop()