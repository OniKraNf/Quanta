import pyautogui, pyperclip
from pynput import keyboard
from services.price_service import PriceService
from repositories.poe_api_repository import PoeApiRepository

class BindRepository:
    def __init__(self):
        self.binds = {}
        self.saved_data = {}
        self.items_service = {}
        self.listener = None

    def add_hotkey(self, bind, handler, item_service):
        """Adds a hotkey"""
        self.binds[bind] = handler
        self.items_service[bind] = item_service

    def get_item_data(self, bind, event=None):
        """Get item data from text"""
        try:
            pyautogui.hotkey('ctrl', 'c')
            copied_data = pyperclip.paste()

            if not copied_data:
                print('Clipboard is empty')
                return

            self.saved_data[bind] = copied_data

            item_service = self.items_service.get(bind, "No item service")
            if item_service == 'No item service':
                print(f'No service available for bind: {bind}')
                return
            
            print(f'Item service: {item_service}')

            normalized_text = item_service.get_normalized_text(copied_data)
            print(f'Normalized_text: {normalized_text}')
            
            normalized_affixes = item_service.get_normalized_affixes(normalized_text.affixes)
            normalized_text.affixes = normalized_affixes   

            poe_api_rep = PoeApiRepository()
            price_service = PriceService(poe_api_repository=poe_api_rep)

            price_service.create_query(normalized_text)
            # poe_api_rep.search_item(price_service.query)
            print(price_service.query)
            
        except Exception as e:
            print(f'Error with copy the data: {e}')
    
    def get_saved_data(self, bind):
        return self.saved_data.get(bind, 'Data is empty')

    def __str__(self):
        return ', '.join([str(v) for v, k in self.binds.items()])
        
    def start_listening(self):
        """Starting listener """
        def on_press(key):
            # Check, aktivated combination or no
            for hotkey, handler in self.binds.items():
                if self._is_hotkey_pressed(hotkey, key):
                    handler()

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def stop_listening(self):
        """Stopping listener"""
        if self.listener:
            self.listener.stop()

    def _is_hotkey_pressed(self, hotkey, key):
        try:
            key_combination = keyboard.HotKey.parse(hotkey)
            return key in key_combination
        except ValueError:
            return False

    