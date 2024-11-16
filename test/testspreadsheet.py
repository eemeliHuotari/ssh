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
        
    def test_arithmetic_addition(self):
        self.spreadsheet.set('A1', "=1+3")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 4)

    def test_arithmetic_multiplication_precedence(self):
        self.spreadsheet.set('A1', "=1+3*2")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 7)

    def test_arithmetic_error_non_integer(self):
        self.spreadsheet.set('A1', "=1+3.5")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")

    def test_arithmetic_error_division_by_zero(self):
        self.spreadsheet.set('A1', "=1/0")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")

    def test_arithmetic_modulus(self):
        self.spreadsheet.set('A1', "=10%3")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 1)
         
    def test_arithmetic_with_reference(self):
        self.spreadsheet.set('A1', "=1+B1")
        self.spreadsheet.set('B1', "3")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 4)

    def test_arithmetic_with_invalid_reference(self):
        self.spreadsheet.set('A1', "=1+B1")
        self.spreadsheet.set('B1', "3.1")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")

    def test_circular_reference(self):
        self.spreadsheet.set('A1', "=B1")
        self.spreadsheet.set('B1', "=A1")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Circular")
        
    def test_string_concatenation(self):
        self.spreadsheet.set('A1', "='Hello'&' World'")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "Hello World")

    def test_invalid_string_concatenation(self):
        self.spreadsheet.set('A1', "='Hello'&' World")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")
        
    def test_string_concatenation_with_references(self):
        self.spreadsheet.set('A1', "='Hello'&B1")
        self.spreadsheet.set('B1', "' World'")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "Hello World")

    def test_invalid_string_concatenation_with_references(self):
        self.spreadsheet.set('A1', "='Hello'&B1")
        self.spreadsheet.set('B1', " World")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")

    def test_circular_reference_in_concatenation(self):
        self.spreadsheet.set('A1', "='Hello'&B1")
        self.spreadsheet.set('B1', "=A1")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Circular")
        
    def test_formula_with_parentheses(self):
        self.spreadsheet.set('A1', "=2*(1+2)")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 6)

    def test_formula_with_parentheses_and_whitespace(self):
        self.spreadsheet.set('A1', "= 2 * ( 1 + 2 )")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 6)

    def test_unbalanced_parentheses(self):
        self.spreadsheet.set('A1', "=2*(1+2")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")
        
    def test_formula_with_parentheses_and_references(self):
        self.spreadsheet.set('A1', "=2*(1+B1)")
        self.spreadsheet.set('B1', "2")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 6)

    def test_formula_with_parentheses_and_references_and_whitespace(self):
        self.spreadsheet.set('A1', "= 2 * ( 1 + B1 )")
        self.spreadsheet.set('B1', "2")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, 6)

    def test_circular_reference_in_parentheses(self):
        self.spreadsheet.set('A1', "=2*(1+B1)")
        self.spreadsheet.set('B1', "=A1")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Circular")

    def test_unbalanced_parentheses_in_formula_with_references(self):
        self.spreadsheet.set('A1', "=2*(1+B1")
        result = self.spreadsheet.evaluate('A1')
        self.assertEqual(result, "#Error")