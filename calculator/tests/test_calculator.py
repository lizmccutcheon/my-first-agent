# tests/test_calculator.py

import unittest
from calculator.pkg.calculator import Calculator
import random

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()
        self.calculator.set_testing_mode(True) # Disable random operand substitution for consistent testing

    def test_addition(self):
        self.assertEqual(self.calculator.evaluate("1 + 1"), 2)
        self.assertEqual(self.calculator.evaluate("1+1"), 2)
        self.assertEqual(self.calculator.evaluate(" 1+1 "), 2)
        self.assertEqual(self.calculator.evaluate("2 + 3"), 5)
        self.assertEqual(self.calculator.evaluate("10 + -5"), 5)
        self.assertEqual(self.calculator.evaluate("-10 + 5"), -5)
        self.assertEqual(self.calculator.evaluate("0.5 + 0.5"), 1.0)
        self.assertEqual(self.calculator.evaluate("1 + -1"), 0)

    def test_subtraction(self):
        self.assertEqual(self.calculator.evaluate("5 - 3"), 2)
        self.assertEqual(self.calculator.evaluate("3-5"), -2)
        self.assertEqual(self.calculator.evaluate("10 - -5"), 15)
        self.assertEqual(self.calculator.evaluate("-10 - 5"), -15)
        self.assertEqual(self.calculator.evaluate("0.5 - 0.25"), 0.25)
        self.assertEqual(self.calculator.evaluate("1 - 1"), 0)

    def test_multiplication(self):
        self.assertEqual(self.calculator.evaluate("2 * 3"), 6)
        self.assertEqual(self.calculator.evaluate("2*3"), 6)
        self.assertEqual(self.calculator.evaluate("2 * -3"), -6)
        self.assertEqual(self.calculator.evaluate("-2 * 3"), -6)
        self.assertEqual(self.calculator.evaluate("0.5 * 2"), 1.0)
        self.assertEqual(self.calculator.evaluate("0 * 5"), 0)

    def test_division(self):
        self.assertEqual(self.calculator.evaluate("6 / 3"), 2)
        self.assertEqual(self.calculator.evaluate("6/3"), 2)
        self.assertEqual(self.calculator.evaluate("6 / -3"), -2)
        self.assertEqual(self.calculator.evaluate("-6 / 3"), -2)
        self.assertEqual(self.calculator.evaluate("1 / 2"), 0.5)
        self.assertEqual(self.calculator.evaluate("10 / 0.5"), 20)

    def test_mixed_operations(self):
        self.assertEqual(self.calculator.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(self.calculator.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(self.calculator.evaluate("10 - 4 / 2"), 8)
        self.assertEqual(self.calculator.evaluate("(10 - 4) / 2"), 3)
        self.assertEqual(self.calculator.evaluate("2 + 3 * 4 - 1"), 13)
        self.assertEqual(self.calculator.evaluate("2 * 3 + 4 / 2"), 8)

    def test_parentheses(self):
        self.assertEqual(self.calculator.evaluate("(1 + 2) * 3"), 9)
        self.assertEqual(self.calculator.evaluate("((1 + 2) * 3)"), 9)
        self.assertEqual(self.calculator.evaluate("1 + (2 * 3)"), 7)
        self.assertEqual(self.calculator.evaluate("(5 - 2) / (3 - 2)"), 3)

    def test_unary_operators(self):
        self.assertEqual(self.calculator.evaluate("-5"), -5)
        self.assertEqual(self.calculator.evaluate("+5"), 5)
        self.assertEqual(self.calculator.evaluate("-(5)"), -5)
        self.assertEqual(self.calculator.evaluate("-(2 + 3)"), -5)
        self.assertEqual(self.calculator.evaluate("5 + -3"), 2)
        self.assertEqual(self.calculator.evaluate("5 - -3"), 8)
        self.assertEqual(self.calculator.evaluate("-(-5)"), 5)
        self.assertEqual(self.calculator.evaluate("-5 * 2"), -10)
        self.assertEqual(self.calculator.evaluate("5 * -2"), -10)
        self.assertEqual(self.calculator.evaluate("5 + -(2)"), 3)
        self.assertEqual(self.calculator.evaluate("5 - -(2)"), 7)
        self.assertEqual(self.calculator.evaluate("2 + - 3"), -1) # handles spaces after unary operator

    def test_floating_point_numbers(self):
        self.assertAlmostEqual(self.calculator.evaluate("0.1 + 0.2"), 0.3)
        self.assertAlmostEqual(self.calculator.evaluate("1.5 * 2.0"), 3.0)
        self.assertAlmostEqual(self.calculator.evaluate("7.0 / 2.0"), 3.5)
        self.assertAlmostEqual(self.calculator.evaluate("-1.0 / 2.0"), -0.5)

    def test_errors(self):
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("1 +")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("1 1")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("(1 + 2")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("1 / 0")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("abc")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("   ")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("1 + (2 * 3")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("1 + )")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("1 (2 + 3)")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("(1 + 2) 3")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("2 ^ 3") # Unsupported operator


    def test_comparison_operators(self):
        self.assertTrue(self.calculator.evaluate("5 = 5"))
        self.assertFalse(self.calculator.evaluate("5 = 6"))
        self.assertTrue(self.calculator.evaluate("10 > 5"))
        self.assertFalse(self.calculator.evaluate("5 > 10"))
        self.assertTrue(self.calculator.evaluate("5 < 10"))
        self.assertFalse(self.calculator.evaluate("10 < 5"))
        self.assertTrue(self.calculator.evaluate("5 >= 5"))
        self.assertTrue(self.calculator.evaluate("10 >= 5"))
        self.assertFalse(self.calculator.evaluate("5 >= 10"))
        self.assertTrue(self.calculator.evaluate("5 <= 5"))
        self.assertTrue(self.calculator.evaluate("5 <= 10"))
        self.assertFalse(self.calculator.evaluate("10 <= 5"))
        self.assertTrue(self.calculator.evaluate("2 + 3 = 5"))
        self.assertFalse(self.calculator.evaluate("2 + 3 = 6"))
        self.assertTrue(self.calculator.evaluate("2 * 3 > 5"))
        self.assertFalse(self.calculator.evaluate("2 * 3 < 5"))
        self.assertTrue(self.calculator.evaluate("(1 + 2) * 3 = 9"))
        self.assertTrue(self.calculator.evaluate("10 / 2 = 5"))
        self.assertTrue(self.calculator.evaluate("10 / 2 + 1 = 6"))
        self.assertTrue(self.calculator.evaluate("  2 +2   = 4")) # Test case for the reported issue

    def test_comparison_operator_errors(self):\
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("2 =")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("= 2")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("2 == 2") # Only single '=' for equality check
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("2 + = 4")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("= 2 + 4")
        with self.assertRaises(ValueError):\
            self.calculator.evaluate("2 + 2 =")

if __name__ == "__main__":
    unittest.main()