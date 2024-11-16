class SpreadSheet:

    def __init__(self):
        self._cells = {}
        self._evaluating = set()

    def set(self, cell: str, value: str) -> None:
        self._cells[cell] = value

    def get(self, cell: str) -> str:
        return self._cells.get(cell, '')

    def evaluate(self, cell: str) -> int | str:
        content = self.get(cell)
        try:
            return int(content)
        except ValueError:
            pass
        if content.startswith("'") and content.endswith("'") and len(content) > 1:
            return content[1:-1]

        return "#Error"
