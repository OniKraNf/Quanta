import pynput, pyperclip, time, pyautogui, re, sys
from repositories.affix_repository import AffixRepository
from services.item_service import ItemService
from services.key_tracker_service import KeyTrackerService
from repositories.poe_api_repository import PoeApiRepository
# from PySide6 import QtCore, QtWidgets, QtGui
from pynput import keyboard
import flet as ft
import sys, json, threading

price_bind = 'command+d'

class App():
    def initialize_services(self, affix_file_path): 
        affix_repository = AffixRepository(affix_file_path)
        self.item_service = ItemService(affix_repository)
    
    def process_clipboard_and_show(self, bind):
        try:
            pyautogui.hotkey('command', 'c')
            copied_data = pyperclip.paste()

            if not copied_data:
                print('Clipboard is empty')
                return

            normalized_text = self.item_service.get_normalized_text(copied_data)
            normalized_affixes = self.item_service.get_normalized_affixes(normalized_text.affixes)
            normalized_text.affixes = normalized_affixes   

            # api = PoeApiRepository('Standard')
            # response = api.search_item(api.create_query(normalized_text))

            # print(json.dumps(response, indent=4))

            self.show_window(normalized_text)

        except Exception as e:
            print(f'Error with get item data {e}')

    def show_window(self, item):
        affixes = item.affixes
        self.page.controls.clear()
        self.page.add(ft.Column([ft.Text(f"Item Name: {item.name}"), 
        ft.Text(f'Item Level: {item.item_level}'),
        ft.Text(f"Affixes:\n{'\n'.join([affix.text.replace('#', str(affix.value)) for affix in affixes])}")
        ]))
        self.page.update()
        
    def run(self, page: ft.Page):
        self.page = page
        page.title = "Quanta"
        page.add(
            ft.Text('Press a hotkey to process and display data.', size=16)
        )
        page.update()

def hotkey_listener(app, tracker, bind):
    bind_keys = bind.split('+')

    key_mapping = {
        'command': 'Key.cmd',
        'd': 'd',
    }

    keys = [key_mapping.get(key, key) for key in bind_keys]

    while True:
        if tracker.check_combination(keys):
            # print(f"Combination {bind} detected!")
            app.process_clipboard_and_show(bind)
            time.sleep(0.5)  

if __name__ == '__main__':
    tracker = KeyTrackerService()
    app = App()
    app.initialize_services('files/cleared_affix.txt')
    
    tracker_thread = threading.Thread(target=tracker.start)
    tracker_thread.daemon = True
    tracker_thread.start()

    hotkey_thread = threading.Thread(target=hotkey_listener, args=(app, tracker, price_bind))
    hotkey_thread.daemon = True
    hotkey_thread.start()

    ft.app(target=app.run)

    
