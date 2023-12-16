from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

import serialize as sz
import tilemap as tm

tiles = []

def export_callback():
    tile_width = int(entry_width.get())
    tile_height = int(entry_height.get())
    filename = fd.asksaveasfilename(initialfile = 'out.png', defaultextension=".png")
    img = tm.create_tilemap_img(tiles, tile_width, tile_height)
    img.save(filename)

def add_tile(tile):
    tiles.append(tile)
    photo = ImageTk.PhotoImage(tile.img)
    tree_objects.insert("", tk.END, text=tile.name, image=photo, values=(f"{tile.x},{tile.y}"))
    
    tree_objects.image_references[tile.name] = photo

def create_tile_callback():
    filename = fd.askopenfilename()
    add_tile(tm.Tile(0, len(tiles), filename))

def on_validate(p):
    return p.isdigit()

def file_menu_save_callback():
    file = fd.asksaveasfile(initialfile = 'out.tilemap', defaultextension=".tilemap")
    serialized_tiles = sz.serialize_tilemap(tiles)
    file.write(serialized_tiles)
    
def file_menu_open_callback():
    filename = fd.askopenfilename()
    with open(filename, 'r') as file:
        t = sz.deserialize_tilemap(file.read())
        for tile in t:
            add_tile(tile)

window = tk.Tk()
window.resizable(width=True, height=True)

style = ttk.Style()
style.configure("Treeview", rowheight=40)

menubar = tk.Menu(window)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open", command=file_menu_open_callback)
file_menu.add_command(label="Save", command=file_menu_save_callback)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.destroy)
menubar.add_cascade(label="File", menu=file_menu)
window.config(menu=menubar)

validate_num = (window.register(on_validate), '%P')

label_title = tk.Label(text="Tilemap Generator", font=('Helvetica', 18, 'bold'))
label_copyright = tk.Label(text="By Mercury Dev")

frame_columns = tk.Frame(window)

columns = ("position")
tree_objects = ttk.Treeview(frame_columns, columns=columns, height=10)
tree_objects.heading("#0", text="Tile")
tree_objects.heading("position", text="Position")
tree_objects.column("position", width=200)
tree_objects.image_references = {}

btn_add_tile = ttk.Button(frame_columns, text="Create Tile", command=create_tile_callback)

label_width_entry = tk.Label(frame_columns, text="Tile Width (px)")
entry_width = ttk.Entry(frame_columns, validate="key", validatecommand=validate_num)
label_height_entry = tk.Label(frame_columns, text="Tile Height (px)")
entry_height = ttk.Entry(frame_columns, validate="key", validatecommand=validate_num)
btn_export = ttk.Button(frame_columns, text="Export as PNG", command=export_callback)
entry_width.insert(0, "32")
entry_height.insert(0, "32")

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