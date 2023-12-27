import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk

class GenerateVariant:
    def __init__(self, root, tile, add_variant_callback, table_id) -> None:
        self.root = root
        self.tile = tile

        self.add_variant_callback = add_variant_callback
        self.table_id = table_id

        self.window = tk.Toplevel(root)
        self.window.title("Generate Variant")

        self.frame_rotation = tk.Frame(self.window)
        self.label_rotation = tk.Label(self.frame_rotation, text="Rotation (Deg)")
        self.label_rotation.grid(row=0, column=0)
        self.scale_rotation = ttk.Scale(self.frame_rotation, from_=0, to=360, command=self.update_image)
        self.scale_rotation.grid(row=1, column=0, padx=3)
        self.entry_rotation = tk.Entry(self.frame_rotation, width=4, validate="key", validatecommand=(root.register(self.validate_entry), "%P"))
        self.entry_rotation.grid(row=1, column=1)
        self.entry_rotation.bind("<Return>", self.update_from_entry)

        self.frame_rotation.grid(row=1, column=0, padx=10, sticky="n")

        self.rotation_angle = 0

        self.label_tile_name = tk.Label(self.window, text=tile.name)
        self.label_tile_name.grid(row=0, column=1)

        self.photo_image = ImageTk.PhotoImage(tile.img.rotate(self.rotation_angle))
        self.label_image = tk.Label(self.window, image=self.photo_image)
        self.label_image.image = self.photo_image
        self.label_image.grid(row=1, column=1, pady=10, padx=10)
        
        self.button_apply = ttk.Button(self.window, text="Apply", command=self.apply)
        self.button_apply.grid(row=2, column=0, pady=10, padx=10, columnspan=2)
        
    def validate_entry(self, new_value):
        try:
            if not new_value:
                return True
            angle = int(new_value)
            return 0 <= angle <= 360
        except ValueError:
            return False

    def update_image(self, angle):
        self.rotation_angle = int(float(angle))
        rotated_image = self.tile.img.rotate(-self.rotation_angle)

        self.photo_image = ImageTk.PhotoImage(rotated_image)
        self.label_image.config(image=self.photo_image)
        self.label_image.image = self.photo_image 

        self.update_entry()

    def update_from_entry(self, event):
        try:
            angle = int(self.entry_rotation.get())
            self.rotation_angle = angle
            self.scale_rotation.set(angle)
            self.update_image(angle)
        except ValueError:
            pass

    def update_entry(self):
        self.entry_rotation.delete(0, tk.END)
        self.entry_rotation.insert(0, str(self.rotation_angle))
    
    def apply(self):
        v = self.tile.add_variation(self.rotation_angle)

        if self.add_variant_callback:
            self.add_variant_callback(self.tile, v, self.table_id)

        self.window.destroy()