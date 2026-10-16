"""
test_errors.py - Unit tests for parser/errors.py

Member 4: Independent Error Handling Testing (Step 2)

These tests verify that each error helper function returns a
ParserSyntaxError with the correct attributes. They do NOT
invoke Member 2's parser; they call the helper functions directly
with the position and token values a parser would provide.
"""

import unittest
import sys
import os

# ---------------------------------------------------------------------------
# Make the project root importable so `from parser.errors import ...` works
# regardless of where the test runner's working directory is.
# ---------------------------------------------------------------------------
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from parser.errors import (
    ParserSyntaxError,
    unexpected_operator,
    missing_operand,
    missing_closing_parenthesis,
    unexpected_closing_parenthesis,
    unexpected_token,
    invalid_character,
)


class TestParserSyntaxErrorClass(unittest.TestCase):
    """Basic tests for the ParserSyntaxError class itself."""

    def test_inherits_from_syntax_error(self):
        """ParserSyntaxError must be a subclass of SyntaxError."""
        err = ParserSyntaxError(0, "x", "y", "reason")
        self.assertIsInstance(err, SyntaxError)

    def test_can_be_raised_and_caught(self):
        """The error can be raised and caught as both
        ParserSyntaxError and SyntaxError."""
        with self.assertRaises(SyntaxError):
            raise ParserSyntaxError(0, "x", "y", "reason")

        with self.assertRaises(ParserSyntaxError):
            raise ParserSyntaxError(0, "x", "y", "reason")

    def test_str_contains_required_sections(self):
        """str(error) must include all five required lines."""
        err = ParserSyntaxError(5, "?", "number", "Bad token")
        text = str(err)
        self.assertIn("INVALID EXPRESSION", text)
        self.assertIn("Error position: 5", text)
        self.assertIn("Found: '?'", text)
        self.assertIn("Expected: number", text)
        self.assertIn("Reason: Bad token", text)


# ===================================================================
# Test Case 1: Unexpected operator — simulates `a+*b`
# ===================================================================
class TestUnexpectedOperator(unittest.TestCase):
    """
    Scenario: the expression is `a+*b`.
    At position 2 the parser finds '*' where an operand was expected.
    """

    def setUp(self):
        # Simulate what the parser would do at position 2 of "a+*b"
        self.err = unexpected_operator(position=2, found="*")

    def test_position(self):
        self.assertEqual(self.err.position, 2)

    def test_found(self):
        self.assertEqual(self.err.found, "*")

    def test_expected(self):
        self.assertEqual(self.err.expected, "identifier, number, or '('")

    def test_reason(self):
        self.assertEqual(
            self.err.reason,
            "Unexpected operator where an operand is required."
        )

    def test_str_output(self):
        text = str(self.err)
        self.assertIn("INVALID EXPRESSION", text)
        self.assertIn("Error position: 2", text)
        self.assertIn("Found: '*'", text)


# ===================================================================
# Test Case 2: Repeated operator — simulates `a++b`
# ===================================================================
class TestRepeatedOperator(unittest.TestCase):
    """
    Scenario: the expression is `a++b`.
    At position 2 the parser finds '+' where an operand was expected.
    This is the same helper as Case 1, just with a different operator.
    """

    def setUp(self):
        self.err = unexpected_operator(position=2, found="+")

    def test_position(self):
        self.assertEqual(self.err.position, 2)

    def test_found(self):
        self.assertEqual(self.err.found, "+")

    def test_expected(self):
        self.assertEqual(self.err.expected, "identifier, number, or '('")

    def test_reason(self):
        self.assertEqual(
            self.err.reason,
            "Unexpected operator where an operand is required."
        )


# ===================================================================
# Test Case 3: Missing operand — simulates `a+`
# ===================================================================
class TestMissingOperand(unittest.TestCase):
    """
    Scenario: the expression is `a+`.
    At position 2 the parser reaches end-of-input instead of an operand.
    """

    def setUp(self):
        self.err = missing_operand(position=2)

    def test_position(self):
        self.assertEqual(self.err.position, 2)

    def test_found_defaults_to_eof(self):
        self.assertEqual(self.err.found, "EOF")

    def test_expected(self):
        self.assertEqual(self.err.expected, "identifier, number, or '('")

    def test_reason(self):
        self.assertEqual(
            self.err.reason,
            "Missing operand at end of expression."
        )

    def test_str_output(self):
        text = str(self.err)
        self.assertIn("Found: 'EOF'", text)
        self.assertIn("Error position: 2", text)


# ===================================================================
# Test Case 4: Missing closing parenthesis — simulates `(a+b`
# ===================================================================
class TestMissingClosingParenthesis(unittest.TestCase):
    """
    Scenario: the expression is `(a+b`.
    At position 4 the parser reaches end-of-input but expected ')'.
    """

    def setUp(self):
        self.err = missing_closing_parenthesis(position=4)

    def test_position(self):
        self.assertEqual(self.err.position, 4)

    def test_found_defaults_to_eof(self):
        self.assertEqual(self.err.found, "EOF")

    def test_expected(self):
        self.assertEqual(self.err.expected, "')'")

    def test_reason(self):
        self.assertEqual(
            self.err.reason,
            "Missing closing parenthesis ')'."
        )

    def test_str_output(self):
        text = str(self.err)
        self.assertIn("Expected: ')'", text)


# ===================================================================
# Test Case 5: Unexpected closing parenthesis — simulates `a+b)`
# ===================================================================
class TestUnexpectedClosingParenthesis(unittest.TestCase):
    """
    Scenario: the expression is `a+b)`.
    At position 3 the parser finds ')' with no matching '('.
    """

    def setUp(self):
        self.err = unexpected_closing_parenthesis(position=3)

    def test_position(self):
        self.assertEqual(self.err.position, 3)

    def test_found(self):
        self.assertEqual(self.err.found, "')'")

    def test_expected(self):
        self.assertEqual(
            self.err.expected,
            "operator (+, -, *, /) or end of input"
        )

    def test_reason(self):
        self.assertEqual(
            self.err.reason,
            "Unexpected closing parenthesis ')' without a matching opening parenthesis."
        )


# ===================================================================
# Test Case 6: Invalid character — simulates `a@b`
# ===================================================================
class TestInvalidCharacter(unittest.TestCase):
    """
    Scenario: the expression is `a@b`.
    At position 1 the parser finds '@' which is not in the grammar.
    """

    def setUp(self):
        self.err = invalid_character(position=1, found="@")

    def test_position(self):
        self.assertEqual(self.err.position, 1)

    def test_found(self):
        self.assertEqual(self.err.found, "@")

    def test_expected(self):
        self.assertEqual(
            self.err.expected,
            "identifier, number, operator (+, -, *, /), or parenthesis"
        )

    def test_reason(self):
        self.assertEqual(
            self.err.reason,
            "Invalid character not recognized by grammar."
        )

    def test_str_output(self):
        text = str(self.err)
        self.assertIn("Found: '@'", text)


# ===================================================================
# Entry point — allows `python tests/test_errors.py`
# ===================================================================
if __name__ == "__main__":
    unittest.main()
