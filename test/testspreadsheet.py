from unittest import TestCase
from spreadsheet import SpreadSheet


class TestSpreadSheet(TestCase):

    def setUp(self):
        self.spreadsheet = SpreadSheet()

    def test_valid_integer(self):
        self.spreadsheet.set('A1', '1')
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 1)

    def test_invalid_integer_with_decimal(self):
        self.spreadsheet.set('A1', '1.5')
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, '#Error')

    def test_invalid_integer_with_text(self):
        self.spreadsheet.set('A1', 'abc')
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, '#Error')
        
    def test_valid_string(self):
        self.spreadsheet.set('A1', "'Apple'")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "Apple")

    def test_invalid_string_missing_end_quote(self):
        self.spreadsheet.set('A1', "'Apple")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")

    def test_invalid_string_missing_start_quote(self):
        self.spreadsheet.set('A1', "Apple'")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")

    def test_simple_formula_integer(self):
        self.spreadsheet.set('A1', "=1")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 1)

    def test_simple_formula_string(self):
        self.spreadsheet.set('A1', "='Apple'")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "Apple")

    def test_invalid_simple_formula(self):
        self.spreadsheet.set('A1', "='Apple")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")
        
    def test_simple_reference(self):
        self.spreadsheet.set('A1', "=B1")
        self.spreadsheet.set('B1', "42")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 42)

    def test_invalid_reference(self):
        self.spreadsheet.set('A1', "=B1")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")

    def test_circular_reference(self):
        self.spreadsheet.set('A1', "=B1")
        self.spreadsheet.set('B1', "=A1")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Circular")