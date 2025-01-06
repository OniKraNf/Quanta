import pynput, pyperclip, time, pyautogui, re, sys
from repositories.affix_repository import AffixRepository
from services.item_service import ItemService
from services.key_tracker_service import KeyTrackerService
from repositories.poe_api_repository import PoeApiRepository
from pynput import keyboard
from views.main_window import QuantaWindow
import sys, json, threading, os, platform
import tkinter as tk
from tkinter import ttk
import sv_ttk

from tkinter import ttk


price_bind = 'ctrl+d'

# key_mapping = {
#     'Linux': {
#         "command": ""
#         "d": ""
#     },
#     'Darwin': {

#     },
#     'Windows': {

#     }
# }

class App:
    def initialize_services(self, affix_file_path): 
        affix_repository = AffixRepository(affix_file_path)
        self.item_service = ItemService(affix_repository)
    
    def process_clipboard_and_show(self, bind, quanta):
        try:
            pyautogui.hotkey('ctrl', 'c')
            copied_data = pyperclip.paste()

            if not copied_data:
                print('Clipboard is empty')
                return

            normalized_text = self.item_service.get_normalized_text(copied_data)
            normalized_affixes = self.item_service.get_normalized_affixes(normalized_text.affixes)
            normalized_text.affixes = normalized_affixes   
            quanta.show_item(normalized_text)
            # api = PoeApiRepository('Standard')
            # response = api.search_item(api.create_query(normalized_text))

            # print(json.dumps(response, indent=4))
        except Exception as e:
            print(f'Error with get item data {e}')

def hotkey_listener(app, tracker, bind, quanta):
    bind_keys = bind.split('+')

    key_mapping = {
        'ctrl': 'Key.ctrl',
        'd': 'd',
    }

    keys = [key_mapping.get(key, key) for key in bind_keys]

    while True:
        if tracker.check_combination(keys) and not tracker.is_hotkey_pressed:
            tracker.is_hotkey_pressed = True 
            app.process_clipboard_and_show(bind, quanta)
            time.sleep(0.5) 
        elif not tracker.check_combination(keys):
            tracker.is_hotkey_pressed = False  

if __name__ == '__main__':
    tracker = KeyTrackerService()
    os_name = platform.system()

    app = App()
    root = tk.Tk()

    app.initialize_services('files/cleared_affix.txt')

    tracker_thread = threading.Thread(target=tracker.start)
    tracker_thread.daemon = True
    tracker_thread.start()

    quanta = QuantaWindow(root=root, width=800, height=600, os_name=os_name, tracker=tracker)

    hotkey_thread = threading.Thread(target=hotkey_listener, args=(app, tracker, price_bind, quanta))
    hotkey_thread.daemon = True
    hotkey_thread.start()
    
    quanta.run()


    
