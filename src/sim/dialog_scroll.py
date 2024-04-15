import json


class DialogController:
    def __init__(self, path):
        self.path = path
        # this is a more inefficient way of performing this, but allows for dynamic
        # jumping across several lines, instead of needing to read one at a time.
        # if dynamic jumping is not required, just use the file directly (no list).
        with open(path, mode='r') as file:
            self.full_text = json.load(file)
        self.current = 0

    def next(self):
        self.current += 1
        code = self.full_text[self.current]['next']
        if code == 'jump':
            line = self.full_text[self.current]['options']
        else:
            line = [self.full_text[self.current]['text']]  # convert to list for showrunner to handle
        return line

    def jump(self, pos):
        assert self.full_text[self.current + pos]['from'] == pos
        self.current += pos
        return self.full_text[self.current]['text']

    def current_line(self):
        return self.full_text[self.current]['text']

    def has_next(self):
        return self.full_text[self.current]['next'] != 'end'
