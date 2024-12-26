import keyboard, pyperclip, time, pyautogui, re, sys
from repositories.affix_repository import AffixRepository
from services.item_service import ItemService
from views.main_window import MainSanctumWidget
from PySide6 import QtCore, QtWidgets, QtGui
from repositories.bind_repository import BindRepository

price_bind = 'ctrl + d'

if __name__ == '__main__':
    print(f'Program was started, press {price_bind}')

    affix_repo = AffixRepository('files/cleared_affix.txt')
    item_service = ItemService(affix_repo)

    copy_bind = BindRepository()
    copy_bind.add_hotkey('ctrl + d',  lambda: copy_bind.get_item_data('ctrl + d'), item_service)

    keyboard.wait('esc')

    # normalized_affixes = item_service.get_normalized_affixes(raw_affixes)

    # affix_ids = [affix.id for affix in normalized_affixes]


# def print_item_data():
#     item_text = pyperclip.paste()
#     item_data = parse_item_data(item_text=item_text)

#     print(item_data)

