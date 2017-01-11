class KeyboardHandler(object):
    def __init__(self):
        self.pressed_keys = set()

    def keyboard(self, ch, x, y):
        self.pressed_keys.add(ch)
        return

    def keyboardUp(self, ch, x, y):
        self.pressed_keys.remove(ch)
        return

    def keyboard_special(self, ch, x, y):
        self.pressed_keys.add(255 + ch)
        return

    def keyboard_specialUp(self, ch, x, y):
        self.pressed_keys.remove(255 + ch)
        return

    def keyPressed(self, ch):
        return ch in self.pressed_keys


class Keys:
    LEFT = 355
    RIGHT = 357
    UP = 356
    DOWN = 358