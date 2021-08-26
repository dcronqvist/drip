from lexing.source_pos import SourcePosition

class Error:
    def __init__(self, error_name: str, exit_code: int, start_pos: SourcePosition, end_pos: SourcePosition, message: str):
        self.error_name = error_name
        self.exit_code = exit_code
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.message = message

    def arrows_below_error(self):
        characters_around = 20

        before = self.start_pos.source[max(self.start_pos.index - characters_around, 0):self.start_pos.index]

        part_of_code = self.start_pos.source[self.start_pos.index:self.end_pos.index + 1]

        after = self.start_pos.source[self.end_pos.index + 1:min(self.end_pos.index + characters_around, len(self.start_pos.source))]

        line_of_code = before + part_of_code + after
        below = ' ' * len(before) + '^' * len(part_of_code) + ' ' * len(after)

        return f"  {line_of_code}\n  {below}"
        

    def __repr__(self) -> str:
        return f"{self.error_name} @ line {self.start_pos.line}, column {self.start_pos.column} in {self.start_pos.file_name}: {self.message}\n\n{self.arrows_below_error()}"