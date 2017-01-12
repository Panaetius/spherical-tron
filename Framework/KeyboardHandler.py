class KeyboardHandler(object):
    def __init__(self):
        self.pressed_keys = set()
        self.down_keys = set()

    def keyboard(self, ch, x, y):
        ch = ord(ch)
        if not ch in self.pressed_keys:
            self.down_keys.add(ch)
        self.pressed_keys.add(ch)
        return

    def keyboardUp(self, ch, x, y):
        ch = ord(ch)
        self.pressed_keys.remove(ch)
        return

    def keyboard_special(self, ch, x, y):
        if not 255 + ch in self.pressed_keys:
            self.down_keys.add(255 + ch)

        self.pressed_keys.add(255 + ch)
        return

    def keyboard_specialUp(self, ch, x, y):
        self.pressed_keys.remove(255 + ch)
        return

    def keyPressed(self, ch):
        return ch in self.pressed_keys

    def keyDown(self, ch):
        return ch in self.down_keys


class Keys:
    LEFT = 355
    RIGHT = 357
    UP = 356
    DOWN = 358
    SPACE = 32