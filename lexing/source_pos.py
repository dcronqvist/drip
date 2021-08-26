class SourcePosition:
    def __init__(self, source:str, file_name: str):
        self.line = 1
        self.column = -1
        self.index = -1
        self.source = source
        self.file_name = file_name
        self.char = None

    def set_position(self, line: int, column: int, index: int):
        self.line = line
        self.column = column
        self.index = index
        self.char = self.source[index] if index < len(self.source) else None
        return self

    def advance(self) -> str:
        """
        Advances the position by one character in the source and returns the character.
        """

        self.column += 1
        self.index += 1
        if self.index > len(self.source):
            self.char = None
        else:
            self.char = self.source[self.index]
        return self.char

    def previous(self) -> str:
        """
        Returns the character that was previously returned by advance().
        """

        return self.source[self.index - 1]

    def copy(self):
        return SourcePosition(self.source, self.file_name).set_position(self.line, self.column, self.index)

