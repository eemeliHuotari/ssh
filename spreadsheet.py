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
        
        if '&' in content:
            parts = content.split('&')
            if len(parts) == 2:
                left, right = parts[0].strip(), parts[1].strip()
                if left.startswith("'") and left.endswith("'"):
                    left_result = left[1:-1]
                else:
                    left_result = self.evaluate(left[1:] if left.startswith("=") else left)

                if right.startswith("'") and right.endswith("'"):
                    right_result = right[1:-1]
                else:
                    right_result = self.evaluate(right[1:] if right.startswith("=") else right)
                if left_result == "#Error" or right_result == "#Error":
                    return "#Error"

                return left_result + right_result
                
        if content.startswith("="):
            ref_cell = content[1:]
            if ref_cell in self._cells:
                self._evaluating.add(cell)
                result = self.evaluate(ref_cell)
                self._evaluating.remove(cell)
                return result
            else:
                return "#Error"
        try:
            result = eval(content)
            if isinstance(result, int):
                return result
            else:
                return "#Error"
        except (ZeroDivisionError, ValueError, SyntaxError):
            return "#Error"