import tkinter as tk
import json
from tkinter import ttk
from models.item import Item
from services.key_tracker_service import KeyTrackerService
import threading

import sv_ttk

class QuantaWindow:
    
    settings_file = 'files/settings.json'

    def __init__(self, root, height, width, os_name, tracker: KeyTrackerService):
        self.height = height
        self.width = width

        self.tracker = tracker

        self.os_name = os_name

        self.settings = self.load_settings()
        self.current_bind = self.settings['os'][self.os_name]['current_bind'].split('+')

        self.root = root
        self.root.title = 'Quanta'

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main")

        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        
        self.center_x = int(self.screen_width / 2 - self.width / 2)
        self.center_y = int(self.screen_height / 2 - self.height / 2)

        self.create_main_page()
        self.create_settings_page()

    def run(self):
        self.root.geometry(f'{self.width}x{self.height}+{self.center_x}+{self.center_y}')

        search_btn = ttk.Button(self.root, text='search', command=self.button_search)
        search_btn.pack()

        if self.os_name == 'Linux':
            self.root.wait_visibility(self.root)
            self.root.wm_attributes('-alpha',0.95)
        else:
            self.root.attributes('-alpha', 0.95)

        sv_ttk.set_theme('dark')
        self.root.mainloop()

    def show_item(self, item: Item):
        item_frame = ttk.Labelframe(self.left_frame)  # Create item frame
        item_frame.pack(side='top', anchor='w', padx=5, pady=5, fill='x')  # Pack it inside left_frame

        item_radio = ttk.Radiobutton(item_frame)  # Create a radio button
        item_radio.pack(side='left')  # Pack it left inside item_frame

        item_name = ttk.Label(item_frame, text=item.name)  # Create label with item name
        item_name.pack(side='left', padx=5)  # Pack it left inside item_frame


    def button_search(self):
        print('Searching...')

    def create_main_page(self):
        self.left_frame = ttk.Frame(self.main_tab)
        self.left_frame.pack(side='left', fill='both', expand=True)

        self.right_frame = ttk.Frame(self.main_tab)
        self.right_frame.pack(side='right', fill='both', expand=True)

    def create_settings_page(self):
        bind_frame = ttk.Labelframe(self.settings_tab)
        bind_label = ttk.Label(bind_frame, text='Current bind: ')
        bind_field = ttk.Button(bind_frame, text=f'{[bind for bind in self.current_bind]}')

        def activate_binding():
            if self.tracker.pressed_keys is not None:
                self.tracker.pressed_keys.clear()  

            def wait_for_key():
                while not self.tracker.pressed_keys:
                    pass
                
                pressed_key = next(iter(self.tracker.pressed_keys))
                print("Pressed key: ", pressed_key)
                self.current_bind = pressed_key
                bind_field.config(text=f"{pressed_key}")
            
            threading.Thread(target=wait_for_key, daemon=True).start()

        bind_field.config(command=activate_binding)
        bind_label.pack(expand=True)
        bind_field.pack(expand=True)
        bind_frame.pack(expand=True, anchor='n', padx=50, pady=50, side='left', ipadx=50, ipady=50)
        def save_bind():
            new_bind = bind_field.get()
            if new_bind:
                self.settings['os'][self.os_name]['current_bind'] = new_bind
                self.save_settings(self.settings)

        save_bind_btn = ttk.Button(self.settings_tab, text='Save', command=save_bind).pack(anchor='n', side='left')
            
    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                'os': {
                    self.os_name: {
                        'current_bind': 'ctrl+d'
                    }
                }
            }
        return self.settings
    
    def save_settings(self, settings):
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
