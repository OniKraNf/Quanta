from pynput import keyboard

class KeyTrackerService:
    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.pressed_keys = set()
        self.is_hotkey_pressed = False

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                print(f'Pressed: {key}')
                self.pressed_keys.add(key.char)
            else:
                print(f'Pressed: {key}')
                self.pressed_keys.add(str(key))
        except AttributeError:
            self.pressed_keys.add(str(key))

    def on_release(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                print(f'Released: {key}')
                self.pressed_keys.discard(key.char)
            else:
                print(f'Released: {key}')
                self.pressed_keys.discard(str(key))
        except AttributeError:
            self.pressed_keys.discard(str(key))

    def check_combination(self, keys):
        return all(key in self.pressed_keys for key in keys)
    
    def start(self):
        with self.listener as listener:
            listener.join()

    def stop(self):
        self.listener.stop()



    