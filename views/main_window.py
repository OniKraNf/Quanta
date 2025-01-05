import tkinter as tk
import json
from tkinter import ttk
from models.item import Item

import sv_ttk

class QuantaWindow:
    
    settings_file = 'files/settings.json'

    def __init__(self, root, height, width, os_name):
        self.height = height
        self.width = width

        self.os_name = os_name

        self.settings = self.load_settings()
        self.current_bind = self.settings['os'][self.os_name]['current_bind']

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


    # def return_pressed(self, event):
    #     self.app.process_clipboard_and_show('s', self)

    def run(self):
        self.root.geometry(f'{self.width}x{self.height}+{self.center_x}+{self.center_y}')

        search_btn = ttk.Button(self.root, text='search', command=self.button_search)
        search_btn.pack()

        # self.root.bind('<Control-KeyPress-d>', self.return_pressed)
        # self.root.bind('<Control-KeyPress-D>', self.return_pressed)
        
        if self.os_name == 'Linux':
            self.root.wait_visibility(self.root)
            self.root.wm_attributes('-alpha',0.95)
        else:
            self.root.attributes('-alpha', 0.5)

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
        bind_label = ttk.Label(self.settings_tab, text='Current bind: ').pack(anchor='n', padx=50, side='left')
        
        bind_entry = ttk.Entry(self.settings_tab)
        bind_entry.pack(anchor='n', side='left')

        def save_bind():
            new_bind = bind_entry.get()
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
