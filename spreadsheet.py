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
        if cell in self._evaluating:
            return "#Circular"
        try:
            return int(content)
        except ValueError:
            pass
        if content.startswith("'") and content.endswith("'") and len(content) > 1:
            return content[1:-1]
        if content.startswith("="):
            formula_content = content[1:]
            try:
                return int(formula_content)
            except ValueError:
                if formula_content.startswith("'") and formula_content.endswith("'") and len(formula_content) > 1:
                    return formula_content[1:-1]
                else:
                    return "#Error"
        if content.startswith("="):
            ref_cell = content[1:]
            if ref_cell in self._cells:
                self._evaluating.add(cell)
                result = self.evaluate(ref_cell)
                self._evaluating.remove(cell)
                return result
            else:
                return "#Error"

        return "#Error"
