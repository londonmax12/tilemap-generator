import tkinter as tk
from tkinter import ttk

class Settings():
    def __init__(self, root, tilemap) -> None:
        def on_validate(p):
            return p.isdigit()

        def save_settings():
            tilemap.tile_width = int(entry_width.get())
            tilemap.tile_height = int(entry_height.get())
            settings_window.destroy()

        validate_num = (root.register(on_validate), '%P')

        settings_window = tk.Toplevel(root)
        settings_window.title("Settings")

        label_width_entry = tk.Label(settings_window, text="Tile Width (px)")
        entry_width = ttk.Entry(settings_window, validate="key", validatecommand=validate_num)
        label_height_entry = tk.Label(settings_window, text="Tile Height (px)")
        entry_height = ttk.Entry(settings_window, validate="key", validatecommand=validate_num)

        entry_width.insert(0, tilemap.tile_width)
        entry_height.insert(0, tilemap.tile_height)

        label_width_entry.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        entry_width.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        label_height_entry.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        entry_height.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        btn_update_settings = ttk.Button(settings_window, text="Save Settings", command=save_settings)
        btn_update_settings.grid(row=2, column=0, columnspan=2, padx=10, pady=5)