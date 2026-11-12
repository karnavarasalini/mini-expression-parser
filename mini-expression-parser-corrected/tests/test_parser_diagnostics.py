"""Regression tests for the root parser's actual error reports and CLI."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from errors import ParserSyntaxError, unexpected_operator


# `import parser` selects the parser/ package, so load parser.py explicitly.
_spec = importlib.util.spec_from_file_location(
    "member4_parser_diagnostics_target", ROOT / "parser.py"
)
_parser = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_parser)


class TestParserDiagnostics(unittest.TestCase):
    def test_parser_uses_root_error_helpers(self):
        self.assertIs(_parser.unexpected_operator, unexpected_operator)

    def test_consecutive_operators_report_actual_character(self):
        for first in "+-*/":
            for second in "+-*/":
                expression = "a" + first + second + "b"
                with self.subTest(expression=expression):
                    with self.assertRaises(ParserSyntaxError) as caught:
                        _parser.parse(expression)
                    error = caught.exception
                    self.assertEqual(error.position, 2)
                    self.assertEqual(error.found, second)
                    self.assertEqual(error.expected, "identifier, number, or '('")
                    self.assertEqual(
                        error.reason,
                        "Unexpected operator where an operand is required.",
                    )

    def test_end_of_input_keeps_missing_operand_details(self):
        for expression in ("", "(", "a+", "a-", "a*", "a/"):
            with self.subTest(expression=expression):
                with self.assertRaises(ParserSyntaxError) as caught:
                    _parser.parse(expression)
                error = caught.exception
                self.assertEqual(error.position, len(expression))
                self.assertEqual(error.found, "EOF")
                self.assertEqual(error.expected, "identifier, number, or '('")
                self.assertEqual(
                    error.reason, "Missing operand at end of expression."
                )

    def test_missing_operand_before_parenthesis_reports_actual_character(self):
        expressions = ["()"]
        expressions += ["(a" + operator + ")" for operator in "+-*/"]
        expressions += ["a" + operator + ")" for operator in "+-*/"]
        for expression in expressions:
            with self.subTest(expression=expression):
                with self.assertRaises(ParserSyntaxError) as caught:
                    _parser.parse(expression)
                error = caught.exception
                self.assertEqual(error.position, expression.index(")"))
                self.assertEqual(error.found, ")")
                self.assertEqual(error.expected, "identifier, number, or '('")
                self.assertEqual(
                    error.reason, "Missing operand before closing parenthesis."
                )

    def test_invalid_command_line_and_interactive_reports(self):
        expected = (
            "Invalid expression: INVALID EXPRESSION\n"
            "Error position: 2\n"
            "Found: '*'\n"
            "Expected: identifier, number, or '('\n"
            "Reason: Unexpected operator where an operand is required.\n"
        )
        for interactive in (False, True):
            with self.subTest(interactive=interactive):
                command = [sys.executable, str(ROOT / "parser.py")]
                if not interactive:
                    command.append("a+*b")
                result = subprocess.run(
                    command,
                    input="a+*b\n" if interactive else None,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=10,
                )
                prompt = "Enter an expression: " if interactive else ""
                self.assertEqual(result.stdout, prompt + expected)
                self.assertEqual(result.stderr, "")

    def test_valid_expressions_remain_accepted(self):
        expressions = (
            "a", "x1", "_var", "0", "42", "3.14", "a+b", "a-b",
            "a*b", "a/b", "a+b*c", "(a+b)*c", "a/(b-c)", "((a))",
            "1+2*(3-4)/5", "var_1+12.5*y2", "a-b-c", "a/b/c",
            "(a+b)*(c-d)", "a*(b+c/(d-e))",
        )
        for expression in expressions:
            with self.subTest(expression=expression):
                self.assertIs(_parser.parse(expression), True)

    def test_valid_command_line_and_interactive_reports(self):
        for interactive in (False, True):
            with self.subTest(interactive=interactive):
                command = [sys.executable, str(ROOT / "parser.py")]
                if not interactive:
                    command.append("a+b*c")
                result = subprocess.run(
                    command,
                    input="a+b*c\n" if interactive else None,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=10,
                )
                prompt = "Enter an expression: " if interactive else ""
                self.assertEqual(result.stdout, prompt + "Valid expression\n")
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
