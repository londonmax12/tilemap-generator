"""
gui.py

This script contains all gui related functionality

Created by Mercury Dev
Created on 2023-12-16

TODO:
- Variant generation
"""

from PIL import ImageTk
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

from serialize import serialize_tilemap, deserialize_tilemap
from gui.popups.settings_popup import Settings
from gui.popups.message_box import MessageBox, PopupType
from gui.popups.generate_variant_popup import GenerateVariant
import tilemap as tm

tilemap_filetypes = [("Tilemap File", "*.tilemap")]
image_filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]

class GUI:
    def __init__(self) -> None:
        initial_width = 32
        initial_height = 32
        tilemap = tm.Tilemap(initial_width, initial_height)

        def open_settings_popup():
            Settings(self.root, tilemap)

        def export_callback():
            filename = fd.asksaveasfilename(initialfile = f'tilemap_{tilemap.tile_width}x{tilemap.tile_height}.png', defaultextension=".png")
            if filename:
                img = tilemap.create_tilemap_img()
                img.save(filename)

        def add_variant(tile, variant, table_id):
            image = tile.get_variant_img(variant)
            resized_img = image.resize((32, 32))
            photo = ImageTk.PhotoImage(resized_img)
            tree_objects.insert(table_id, tk.END, text=variant.name, image=photo, values=(f"{variant.x},{variant.y}"))
            tree_objects.image_references[variant.name] = photo

        def add_tile(tile, table_id=""):
            if not tile.img:
                popup = MessageBox(f"Failed to load tile image: {tile.name}\nWould you like to relocate image?", PopupType.WARNING)
                result = popup.display()
                if result:
                    image_file_path = fd.askopenfilename(filetypes=image_filetypes)
                    if image_file_path:
                        tile.image_path = image_file_path
                        tile.set_image()
                    else:
                        tile.set_image("assets/warning_icon.png")
                else:
                    tile.set_image("assets/warning_icon.png")

            resized_img = tile.img.resize((32, 32))
            
            if table_id == "":
                tilemap.tiles.append(tile)

            photo = ImageTk.PhotoImage(resized_img)
            tree_id = tree_objects.insert(table_id, tk.END, text=tile.name, image=photo, values=(f"{tile.x},{tile.y}"))
            tree_objects.image_references[tile.name] = photo

            for child in tile.children:
                add_tile(child, tree_id)

            for variant in tile.variations:
                add_variant(tile, variant, tree_id)

        def create_tile():
            filename = fd.askopenfilename(filetypes=image_filetypes)
            if filename:
                add_tile(tm.Tile(filename, tilemap.get_next_tile_position()))

        def file_menu_save_callback():
            filename = fd.asksaveasfile(initialfile = 'out.tilemap', defaultextension=".tilemap")
            if filename:
                serialized_tiles = serialize_tilemap(tilemap)
                filename.write(serialized_tiles)

        def file_menu_open_callback():
            global tilemap

            for item in tree_objects.get_children():
                tree_objects.delete(item)
                 
            filename = fd.askopenfilename(filetypes=tilemap_filetypes)
            if filename:
                tilemap = tm.Tilemap(initial_width, initial_height)
                with open(filename, 'r') as file:
                    deserialized_tilemap = deserialize_tilemap(file.read())
                    for tile in deserialized_tilemap.tiles:
                        add_tile(tile)


        def update_right_panel(event):
            global selected_tile
            selected_item = tree_objects.selection()
            
            selected_tile = None
            if selected_item:
                selected_tile_name = tree_objects.item(selected_item)['text']
                selected_tile = tilemap.get_tile_by_name(selected_tile_name)


            for widget in frame_right.winfo_children():
                widget.destroy()

            def add_child_callback():
                filename = fd.askopenfilename(filetypes=image_filetypes)
                if filename:
                    t = tm.Tile(filename, tilemap.get_next_tile_position(selected_tile))
                    add_tile(t, selected_item)
                    selected_tile.add_child(t)
            
            def add_varient_to_table(tile, variant, table_id):
                add_variant(tile, variant, table_id)

            def generate_varient_callback():
                GenerateVariant(self.root, selected_tile, add_varient_to_table, selected_item)
           
            if selected_tile:
                label_tile_name = tk.Label(frame_right, text=f"Tile Name: {selected_tile.name}")
                label_tile_position = tk.Label(frame_right, text=f"Position: {selected_tile.x}, {selected_tile.y}")

                btn_add_variant = ttk.Button(frame_right, text="Create Child", command=add_child_callback)
                btn_generate_variant = ttk.Button(frame_right, text="Generate Variant", command=generate_varient_callback)
                
                label_tile_name.pack()
                label_tile_position.pack()
                btn_add_variant.pack()
                btn_generate_variant.pack()

        self.root = window = tk.Tk()
        self.root.resizable(width=True, height=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=file_menu_open_callback)
        file_menu.add_command(label="Save", command=file_menu_save_callback)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=window.destroy)

        tilemap_menu = tk.Menu(menubar, tearoff=0)
        tilemap_menu.add_command(label="Settings", command=open_settings_popup)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Tilemap", menu=tilemap_menu)

        window.config(menu=menubar)

        label_title = tk.Label(text="Tilemap Generator", font=('Helvetica', 18, 'bold'))
        label_copyright = tk.Label(text="By Mercury Dev")

        frame_columns = tk.Frame(window)

        frame_right = tk.Frame(frame_columns)
        frame_right.grid(row=0, column=1, padx=10)

        columns = ("position")
        tree_objects = ttk.Treeview(frame_columns, columns=columns, height=10)
        tree_objects.heading("#0", text="Tile")
        tree_objects.heading("position", text="Position")
        tree_objects.column("position", width=200)
        tree_objects.image_references = {}
        tree_objects.bind("<ButtonRelease-1>", update_right_panel)

        btn_add_tile = ttk.Button(frame_columns, text="Create Tile", command=create_tile)

        btn_export = ttk.Button(frame_columns, text="Export as PNG", command=export_callback)

        label_title.pack()
        label_copyright.pack()
        frame_columns.pack(padx=10, pady=10)

        tree_objects.grid(row=0, column=0, padx=10, rowspan=8)
        btn_add_tile.grid(row=8, column=0, padx=10)
        btn_export.grid(row=8, column=1, padx=10, pady=(10, 5))

    def start(self):
        self.root.mainloop()