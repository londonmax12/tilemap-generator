from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import tilemap as tm
import os

tiles = []

def export():
    img = tm.create_tilemap_img(tiles, tilesize)
    img.save("out.png")
    
def add_tile():
    filename = fd.askopenfilename()
    img = Image.open(filename)
    tile = tm.Tile(len(tiles), 0, img)
    tiles.append(tile)
    base = os.path.basename(filename)
    name = os.path.splitext(base)[0]
    
    photo = ImageTk.PhotoImage(img)
    tree_objects.insert("", tk.END, text=name, image=photo)
    tree_objects.image_references[name] = photo

def on_validate(p):
    return p.isdigit()


window = tk.Tk()
window.resizable(width=True, height=True)

style = ttk.Style()
style.configure("Treeview", rowheight=40)

validate_num = (window.register(on_validate), '%P')

label_title = tk.Label(text="Tilemap Generator")
label_copyright = tk.Label(text="By Mercury Dev")

frame_columns = tk.Frame(window)

columns = ("position")
tree_objects = ttk.Treeview(frame_columns, columns=columns, height=10)
tree_objects.heading("#0", text="Tile")
tree_objects.heading("position", text="Position")
tree_objects.image_references = {}

btn_add_tile = ttk.Button(frame_columns, text="Add Tile", command=add_tile)

label_width_entry = tk.Label(frame_columns, text="Tile Width (px)")
entry_width = ttk.Entry(frame_columns, validate="key", validatecommand=validate_num)
label_height_entry = tk.Label(frame_columns, text="Tile Height (px)")
entry_height = ttk.Entry(frame_columns, validate="key", validatecommand=validate_num)
btn_export = ttk.Button(frame_columns, text="Export", command=export)

label_title.pack()
label_copyright.pack()

frame_columns.pack(padx=10, pady=10)

tree_objects.grid(row=0, column=0, padx=10, rowspan=8)

btn_add_tile.grid(row=8, column=0, padx=10)

label_width_entry.grid(row=0, column=1, padx=10, pady=(10, 5), sticky='s')
entry_width.grid(row=1, column=1, padx=10, pady=(0, 5), sticky='ew')
label_height_entry.grid(row=2, column=1, padx=10, pady=(10, 5), sticky='s')
entry_height.grid(row=3, column=1, padx=10, pady=(0, 5), sticky='ew')
btn_export.grid(row=8, column=1, padx=10, pady=(10, 5))

window.mainloop()