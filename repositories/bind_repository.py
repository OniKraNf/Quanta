import pyautogui, pyperclip, keyboard

class BindRepository:
    def __init__(self):
        self.binds = {}
        self.saved_data = {}
        self.items_service = {}

    def add_hotkey(self, bind, handler, item_service):
        self.binds[bind] = handler
        self.items_service[bind] = item_service
        keyboard.add_hotkey(bind, handler)

    def get_item_data(self, bind, event=None):
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

            normalized_text = item_service.get_normalized_text(copied_data)
            normalized_affixes = item_service.get_normalized_affixes(normalized_text)
            normalized_text['suffixes'] = normalized_affixes   
            print(normalized_text)

            query = {
                "query": {
                    "status": {
                        "option": "online"
                    },
                    "type": normalized_text.get('name', ''),
                    "stats": [{
                        "type": "and",
                        "filters": [
                        {
                            "id": affix.id,
                            "value": {"min": affix.value}
                        }
                        for affix in normalized_text.get('suffixes', []) if affix.value is not None
                        ]
                    }],
                    "filters": {
                        "misc_filters": {
                            "filters": {
                                "ilvl": {"min": int(normalized_text.get('item_level', 0))}
                            }
                        }
                    }
                },
                "sort": {
                    "price": "asc"
                }
            }

            print(query)

            # print(f'Try print: {normalized_text['suffixes'][0].id}')

        except Exception as e:
            print(f'Error with copy the data: {e}')
    
    def get_saved_data(self, bind):
        return self.saved_data.get(bind, 'Data is empty')

    def __str__(self):
        return ', '.join([str(v) for v, k in self.binds.items()])
        

    