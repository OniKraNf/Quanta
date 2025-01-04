from pynput import keyboard

class KeyTrackerService:
    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.pressed_keys = set()

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.pressed_keys.add(key.char)
            else:
                self.pressed_keys.add(str(key))
            # print(f'Key pressed: {key}, current keys {self.pressed_keys}')
        except AttributeError:
            self.pressed_keys.add(str(key))

    def on_release(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.pressed_keys.discard(key.char)
            else:
                self.pressed_keys.discard(str(key))
            # print(f'Key released: {key}, current keys {self.pressed_keys}')
        except AttributeError:
            self.pressed_keys.discard(str(key))

    def check_combination(self, keys):
        return all(key in self.pressed_keys for key in keys)
    
    def start(self):
        with self.listener as listener:
            listener.join()

    def stop(self):
        self.listener.stop()



    