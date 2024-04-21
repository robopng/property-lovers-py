import json


class DialogController:
    """
    A controller for dialog files intended for use in the dating sim.
    Dating sim dialog files are in a special json format:
      - A list of dictionaries, where each dictionary is a line
      - On an NPC dialog line, each dictionary has three keys: text, from, next
      - On a player dialog line, text is replaced with options, a list of three dictionaries
        in the form {"Option 1": 1, "Option 2", 2}
      - Key 'from' in the first line will always be 'start', and key 'next' in the last will
        always be 'end'
      - On a player line, key 'next' will always be 'jump', and the 3 options following will
        have key 'from' be 1, 2, or 3, corresponding to the values in the 'options' list
    """
    def __init__(self):
        # this is a more inefficient way of performing this, but allows for dynamic
        # jumping across several lines, instead of needing to read one at a time.
        # if dynamic jumping is not required, just use the file directly (no list).
        self.full_text = []
        self.current = 0

    def load_file(self, name):
        with open(f'../dialog/{name}.json', mode='r') as file:
            self.full_text = json.load(file)

    def empty_file(self):
        self.full_text = []
        self.current = 0

    def next(self):
        """
        Proceed to the next line in the dialog sequence.
        If the next line is a player option, then provide those options.
        :return: Either the next NPC dialog line or the next player options
        """
        self.current += 1
        code = self.full_text[self.current]['next']
        if code == 'jump':
            line = self.full_text[self.current]['options'].keys()
        else:
            line = [self.full_text[self.current]['text']]  # convert to list for showrunner to handle
        return line

    def jump(self, pos):
        """
        Jump to a given NPC dialog line from a player selected option.
        :param pos: The corresponding value of the player's choice
        :return: The NPC's response to the player's input choice
        """
        assert self.full_text[self.current + pos]['from'] == str(pos)
        self.current += pos
        return self.full_text[self.current]['text']

    def walk_back(self):
        """
        Walk the scroll back to the nearest non-jump and non-input dialog line.
        """
        # change this if there are ever multiple linked jumps
        self.current -= 1

    def current_line(self):
        """
        :return: the current line of dialog in the loaded file
        """
        return self.full_text[self.current]['text']

    def awaiting(self):
        """
        :return: whether the scroll is awaiting player input at the moment
        """
        return self.full_text[self.current]['text'] == 'player input'

    def has_file(self):
        """
        :return: whether the scroll is currently loaded with a dialog file
        """
        return len(self.full_text) > 0

    def has_next(self):
        """
        :return: whether there is more dialog remaining in the loaded dialog file
        """
        if self.has_file(): return self.full_text[self.current]['next'] != 'end'
