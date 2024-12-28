import pynput, pyperclip, time, pyautogui, re, sys
from repositories.affix_repository import AffixRepository
from services.item_service import ItemService
from views.main_window import MainSanctumWidget
# from PySide6 import QtCore, QtWidgets, QtGui
from repositories.bind_repository import BindRepository

price_bind = 'ctrl + d'

if __name__ == '__main__':
    print(f'Program was started, press {price_bind}')

    affix_repo = AffixRepository('files/cleared_affix.txt')
    item_service = ItemService(affix_repo)

    bind_repo = BindRepository()
    bind_repo.add_hotkey('<cmd>+d',  lambda: bind_repo.get_item_data('<cmd>+d'), item_service)

    print('Listening for hotkeys. Press ESC to exit.')

    try:
        bind_repo.start_listening()
        while True:
            pass
    except KeyboardInterrupt:
        print('Exiting...')
    finally:
        bind_repo.stop_listening()