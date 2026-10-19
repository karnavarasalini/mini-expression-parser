"""
errors.py - Custom Exception and Error Handling Helpers for Mini Expression Parser.

Member 4 Responsibility: Error Handling + LLM Connection
Based on Project 10: Mini Expression Parser Specification (Section 12 & 14).
"""


class ParserSyntaxError(SyntaxError):
    """
    Custom syntax error raised when an arithmetic expression violates
    the Context-Free Grammar (CFG) rules.

    Extends Python's built-in SyntaxError.

    Attributes:
        position (int): Zero-based character index where the error occurred.
        found (str): The unexpected token or character found in the input.
        expected (str): Description of the token or category that was expected.
        reason (str): Human-readable explanation of why this is invalid.
    """

    def __init__(self, position: int, found: str, expected: str, reason: str):
        self.position = position
        self.found = found
        self.expected = expected
        self.reason = reason

        # Construct standard multi-line error message matching project specification
        found_display = f"'{found}'" if found is not None else "None"
        message = (
            f"INVALID EXPRESSION\n"
            f"Error position: {self.position}\n"
            f"Found: {found_display}\n"
            f"Expected: {self.expected}\n"
            f"Reason: {self.reason}"
        )
        super().__init__(message)

    def __str__(self) -> str:
        """Return the formatted multi-line error report."""
        return self.msg if hasattr(self, "msg") and self.msg else super().__str__()


# =====================================================================
# Helper Factory Functions
# =====================================================================

def unexpected_operator(
    position: int,
    found: str,
    expected: str = "identifier, number, or '('",
    reason: str = "Unexpected operator where an operand is required."
) -> ParserSyntaxError:
    """
    Creates an error when an operator (+, -, *, /) appears where an operand
    (identifier, number, or parenthesized sub-expression) was expected.

    Example: 'a+*b' at position 2 (found '*').
    """
    return ParserSyntaxError(
        position=position,
        found=found,
        expected=expected,
        reason=reason
    )


def missing_operand(
    position: int,
    found: str = "EOF",
    expected: str = "identifier, number, or '('",
    reason: str = "Missing operand at end of expression."
) -> ParserSyntaxError:
    """
    Creates an error when an expression ends abruptly after an operator.

    Example: 'a+' at position 2 (found 'EOF').
    """
    return ParserSyntaxError(
        position=position,
        found=found,
        expected=expected,
        reason=reason
    )


def missing_closing_parenthesis(
    position: int,
    found: str = "EOF",
    expected: str = "')'",
    reason: str = "Missing closing parenthesis ')'."
) -> ParserSyntaxError:
    """
    Creates an error when an open parenthesis '(' is not closed before
    the end of the expression or before an invalid boundary.

    Example: '(a+b' at position 4 (found 'EOF').
    """
    return ParserSyntaxError(
        position=position,
        found=found,
        expected=expected,
        reason=reason
    )


def unexpected_closing_parenthesis(
    position: int,
    found: str = "')'",
    expected: str = "operator (+, -, *, /) or end of input",
    reason: str = "Unexpected closing parenthesis ')' without a matching opening parenthesis."
) -> ParserSyntaxError:
    """
    Creates an error when an unmatched ')' is encountered.

    Example: 'a+b)' at position 3 (found ')').
    """
    return ParserSyntaxError(
        position=position,
        found=found,
        expected=expected,
        reason=reason
    )


def unexpected_token(
    position: int,
    found: str,
    expected: str,
    reason: str = "Unexpected token encountered."
) -> ParserSyntaxError:
    """
    Generic helper for unexpected tokens (e.g. empty parentheses '()' or repeated tokens).
    """
    return ParserSyntaxError(
        position=position,
        found=found,
        expected=expected,
        reason=reason
    )


def invalid_character(
    position: int,
    found: str,
    expected: str = "identifier, number, operator (+, -, *, /), or parenthesis",
    reason: str = "Invalid character not recognized by grammar."
) -> ParserSyntaxError:
    """
    Creates an error when a character is not valid in our grammar alphabet.

    Example: 'a + @b' at position 4 (found '@').
    """
    return ParserSyntaxError(
        position=position,
        found=found,
        expected=expected,
        reason=reason
    )