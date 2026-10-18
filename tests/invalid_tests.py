"""
invalid_tests.py - Invalid Expression Testing (Step 3)

Member 4: Tests 10 invalid expressions against Member 2's
RecursiveDescentParser to verify they are all rejected.

Design decisions:
  - If Member 2's parser is not available on this branch,
    all tests report BLOCKED (not PASS or FAIL).
  - Member 2's parser currently raises plain SyntaxError.
    After integration, it will raise ParserSyntaxError (which
    extends SyntaxError), so we catch SyntaxError to work
    with both the pre- and post-integration versions.
  - We extract error position from the message string when the
    error is a plain SyntaxError (pre-integration).
    Post-integration, we read the .position attribute directly.
  - We do NOT modify Member 2's code.
"""

import sys
import os
import re
import unittest

# ---------------------------------------------------------------------------
# Make the project root importable
# ---------------------------------------------------------------------------
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

# ---------------------------------------------------------------------------
# Attempt to import Member 2's parser
# ---------------------------------------------------------------------------
_PARSER_AVAILABLE = False
_IMPORT_ERROR_MSG = ""

try:
    import importlib.util

    # Check root parser.py (Member 2's current file)
    _parser_path = os.path.join(
        os.path.dirname(__file__), "..", "parser.py"
    )
    # Also check parser/parser.py and parser/recursive_descent_parser.py
    _alt_path1 = os.path.join(
        os.path.dirname(__file__), "..", "parser", "parser.py"
    )
    _alt_path2 = os.path.join(
        os.path.dirname(__file__), "..", "parser", "recursive_descent_parser.py"
    )

    chosen_path = None
    for candidate in [_parser_path, _alt_path1, _alt_path2]:
        if os.path.isfile(candidate):
            chosen_path = candidate
            break

    if chosen_path is not None:
        spec = importlib.util.spec_from_file_location(
            "member2_parser", os.path.abspath(chosen_path)
        )
        _mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_mod)
        RecursiveDescentParser = _mod.RecursiveDescentParser
        _PARSER_AVAILABLE = True
    else:
        _IMPORT_ERROR_MSG = (
            f"Member 2's parser not found at expected locations:\n"
            f"  - {os.path.abspath(_parser_path)}\n"
            f"  - {os.path.abspath(_alt_path1)}\n"
            f"  - {os.path.abspath(_alt_path2)}\n"
            f"Integration testing is BLOCKED until Member 2's branch\n"
            f"is merged or parser.py is copied to this branch."
        )
except Exception as exc:
    _IMPORT_ERROR_MSG = f"Failed to import Member 2's parser: {exc}"

# ---------------------------------------------------------------------------
# Also import our own ParserSyntaxError for post-integration checks
# ---------------------------------------------------------------------------
try:
    from parser.errors import ParserSyntaxError
    _HAS_CUSTOM_ERROR = True
except ImportError:
    _HAS_CUSTOM_ERROR = False


# ---------------------------------------------------------------------------
# Helper: extract position from a SyntaxError
# ---------------------------------------------------------------------------
def _get_position(error):
    """
    Extract the error position from any SyntaxError.

    Post-integration:  error.position attribute exists  -> use it directly.
    Pre-integration:   plain SyntaxError with message   -> regex extract.
    """
    if hasattr(error, "position"):
        return error.position
    match = re.search(r"at position (\d+)", str(error))
    return int(match.group(1)) if match else None


# ---------------------------------------------------------------------------
# Test class for 10 invalid expressions
# ---------------------------------------------------------------------------
@unittest.skipUnless(
    _PARSER_AVAILABLE,
    f"BLOCKED - Member 2's RecursiveDescentParser is not available. "
    f"{_IMPORT_ERROR_MSG}"
)
class TestInvalidExpressions(unittest.TestCase):
    """
    Each test feeds one invalid expression into Member 2's parser
    and asserts that a SyntaxError is raised (the expression is
    correctly rejected). Error position is verified where possible.
    """

    def _parse(self, expression: str):
        """Strip spaces and parse using Member 2's parser."""
        cleaned = "".join(expression.split())
        p = RecursiveDescentParser(cleaned)
        p.parse()

    # ---------------------------------------------------------------
    # 1. Unexpected operator: a+*b
    # ---------------------------------------------------------------
    def test_01_unexpected_operator_a_plus_star_b(self):
        """a+*b -> '*' appears where an operand is expected (pos 2)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("a+*b")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 2, "Error should be at position 2")

    # ---------------------------------------------------------------
    # 2. Repeated operator: a++b
    # ---------------------------------------------------------------
    def test_02_repeated_operator_a_plus_plus_b(self):
        """a++b -> second '+' where an operand is expected (pos 2)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("a++b")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 2, "Error should be at position 2")

    # ---------------------------------------------------------------
    # 3. Leading operator: *a+b
    # ---------------------------------------------------------------
    def test_03_leading_operator_star_a_plus_b(self):
        """*a+b -> expression starts with '*' (pos 0)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("*a+b")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 0, "Error should be at position 0")

    # ---------------------------------------------------------------
    # 4. Unexpected closing parenthesis: a+b)
    # ---------------------------------------------------------------
    def test_04_unexpected_closing_paren_a_plus_b_rparen(self):
        """a+b) -> unmatched ')' after valid expression (pos 3)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("a+b)")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 3, "Error should be at position 3")

    # ---------------------------------------------------------------
    # 5. Missing closing parenthesis: (a+b
    # ---------------------------------------------------------------
    def test_05_missing_closing_paren_lparen_a_plus_b(self):
        """(a+b -> no matching ')' (pos 4)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("(a+b")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 4, "Error should be at position 4")

    # ---------------------------------------------------------------
    # 6. Missing closing parenthesis (nested): a/(b-c
    # ---------------------------------------------------------------
    def test_06_missing_closing_paren_nested_a_div_b_minus_c(self):
        """a/(b-c -> missing ')' after sub-expression (pos 5)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("a/(b-c")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 5, "Error should be at position 5")

    # ---------------------------------------------------------------
    # 7. Double operator: a//b
    # ---------------------------------------------------------------
    def test_07_double_operator_a_slash_slash_b(self):
        """a//b -> second '/' where an operand is expected (pos 2)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("a//b")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 2, "Error should be at position 2")

    # ---------------------------------------------------------------
    # 8. Missing operand at end: a+
    # ---------------------------------------------------------------
    def test_08_missing_operand_a_plus(self):
        """a+ -> expression ends after operator (pos 2)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("a+")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 2, "Error should be at position 2")

    # ---------------------------------------------------------------
    # 9. Empty parentheses: ()
    # ---------------------------------------------------------------
    def test_09_empty_parentheses(self):
        """() -> nothing inside parentheses (pos 1)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("()")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 1, "Error should be at position 1")

    # ---------------------------------------------------------------
    # 10. Implicit multiplication: a(b+c)
    # ---------------------------------------------------------------
    def test_10_implicit_multiplication_a_lparen_b_plus_c_rparen(self):
        """a(b+c) -> missing operator between 'a' and '(' (pos 1)."""
        with self.assertRaises(SyntaxError) as ctx:
            self._parse("a(b+c)")
        pos = _get_position(ctx.exception)
        self.assertEqual(pos, 1, "Error should be at position 1")


# ===================================================================
# Standalone runner with PASS / FAIL / BLOCKED summary
# ===================================================================
if __name__ == "__main__":

    # -- Blocked: parser not available ---------------------------------
    if not _PARSER_AVAILABLE:
        print("=" * 64)
        print("  BLOCKED: Member 2's RecursiveDescentParser is not available")
        print("=" * 64)
        print()
        print(_IMPORT_ERROR_MSG)
        print()

        cases = [
            "a+*b", "a++b", "*a+b", "a+b)", "(a+b",
            "a/(b-c", "a//b", "a+", "()", "a(b+c)",
        ]
        for expr in cases:
            print(f"  BLOCKED  |  {expr}")

        print("-" * 64)
        print(f"  Total  : 10")
        print(f"  Passed : 0")
        print(f"  Failed : 0")
        print(f"  Blocked: 10")
        print("=" * 64)
        sys.exit(0)

    # -- Parser available: run tests and collect results ---------------
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestInvalidExpressions)

    import io
    silent_stream = io.StringIO()
    runner = unittest.TextTestRunner(verbosity=2, stream=silent_stream)
    result = runner.run(suite)

    # Build ordered list matching the 10 expressions
    all_cases = [
        ("a+*b",    "Unexpected operator",           "test_01"),
        ("a++b",    "Repeated operator",             "test_02"),
        ("*a+b",    "Leading operator",              "test_03"),
        ("a+b)",    "Unexpected closing paren",      "test_04"),
        ("(a+b",    "Missing closing paren",         "test_05"),
        ("a/(b-c",  "Missing closing paren (nested)","test_06"),
        ("a//b",    "Double operator",               "test_07"),
        ("a+",      "Missing operand at end",        "test_08"),
        ("()",      "Empty parentheses",             "test_09"),
        ("a(b+c)",  "Implicit multiplication",       "test_10"),
    ]

    failed_names = set()
    for test_case, _ in result.failures + result.errors:
        failed_names.add(test_case._testMethodName)

    passed = 0
    failed = 0

    print("=" * 64)
    print("  INVALID EXPRESSION TEST RESULTS")
    print("=" * 64)

    for expr, desc, prefix in all_cases:
        is_fail = any(prefix in name for name in failed_names)
        status = "FAIL" if is_fail else "PASS"
        if status == "PASS":
            passed += 1
        else:
            failed += 1
        print(f"  {status}    |  {expr:<12s}  |  {desc}")

    print("-" * 64)
    print(f"  Total  : {passed + failed}")
    print(f"  Passed : {passed}")
    print(f"  Failed : {failed}")
    print(f"  Blocked: 0")
    print("=" * 64)

    if result.failures:
        print("\n  FAILURE DETAILS:")
        for test_case, tb in result.failures:
            print(f"\n  {test_case}:")
            for line in tb.strip().splitlines():
                print(f"    {line}")

    if result.errors:
        print("\n  ERROR DETAILS:")
        for test_case, tb in result.errors:
            print(f"\n  {test_case}:")
            for line in tb.strip().splitlines():
                print(f"    {line}")

    sys.exit(0 if failed == 0 else 1)
