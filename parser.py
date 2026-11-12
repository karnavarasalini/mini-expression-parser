
import sys

from errors import (
    invalid_character,
    missing_closing_parenthesis,
    missing_operand,
    unexpected_closing_parenthesis,
    unexpected_operator,
    unexpected_token,
)


class Parser:
    def __init__(self, expression):
        self.expression = expression
        self.pos = 0

    def current(self):
        if self.pos < len(self.expression):
            return self.expression[self.pos]
        return None

    def eat(self, expected):
        current = self.current()

        if current == expected:
            self.pos += 1
            return

        if expected == ")" and current is None:
            position = self.pos
            if self.expression.startswith("("):
                position = len(self.expression)
            else:
                position = max(0, self.pos - 1)
            raise missing_closing_parenthesis(position)

        if current == ")":
            raise unexpected_closing_parenthesis(
                self.pos, found=")"
            )

        if current in ("+", "-", "*", "/"):
            raise unexpected_operator(
                self.pos, found=current
            )

        raise unexpected_token(
            self.pos,
            found=current,
            expected=repr(expected),
        )

    # E -> T E'
    def E(self):
        self.T()
        self.E_prime()

    # E' -> + T E' | - T E' | epsilon
    def E_prime(self):
        while self.current() in ("+", "-"):
            self.pos += 1

            if self.current() is None or self.current() in (
                "+", "-", "*", "/", ")"
            ):
                if self.current() == ")":
                    raise missing_operand(self.pos)
                raise missing_operand(self.pos)

            self.T()

    # T -> F T'
    def T(self):
        self.F()
        self.T_prime()

    # T' -> * F T' | / F T' | epsilon
    def T_prime(self):
        while self.current() in ("*", "/"):
            self.pos += 1

            if self.current() is None or self.current() in (
                "+", "-", "*", "/", ")"
            ):
                raise missing_operand(self.pos)

            self.F()

    # F -> (E) | id | num
    def F(self):
        current = self.current()

        if current is None:
            raise missing_operand(self.pos)

        if current == "(":
            self.pos += 1

            if self.current() == ")":
                raise missing_operand(self.pos)

            self.E()

            if self.current() is None:
                # Report the missing ')' position.
                if self.expression.startswith("("):
                    position = len(self.expression)
                else:
                    position = max(0, self.pos - 1)

                raise missing_closing_parenthesis(position)

            self.eat(")")
            return

        if current.isalpha() or current == "_":
            while self.current() is not None and (
                self.current().isalnum() or self.current() == "_"
            ):
                self.pos += 1
            return

        if current.isdigit():
            decimal_points = 0

            while self.current() is not None and (
                self.current().isdigit() or self.current() == "."
            ):
                if self.current() == ".":
                    decimal_points += 1

                    if decimal_points > 1:
                        raise invalid_character(
                            self.pos, found="."
                        )

                self.pos += 1

            if self.expression[self.pos - 1] == ".":
                raise invalid_character(
                    self.pos - 1, found="."
                )

            return

        if current == ")":
            raise unexpected_closing_parenthesis(
                self.pos, found=")"
            )

        if current in ("+", "-", "*", "/"):
            raise unexpected_operator(
                self.pos, found=current
            )

        if not current.isalnum() and current not in (
            "_", ".", "(", ")"
        ):
            raise invalid_character(
                self.pos, found=current
            )

        raise unexpected_token(
            self.pos,
            found=current,
            expected="identifier, number, or '('",
        )

    def parse(self):
        self.E()

        if self.current() is not None:
            current = self.current()

            if current == ")":
                raise unexpected_closing_parenthesis(
                    self.pos, found=")"
                )

            if current in ("+", "-", "*", "/"):
                raise unexpected_operator(
                    self.pos, found=current
                )

            raise unexpected_token(
                self.pos,
                found=current,
                expected="operator or end of expression",
            )

        return True


def parse(expression):
    parser = Parser(expression)
    return parser.parse()
RecursiveDescentParser = Parser


def main():
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
    else:
        expression = input("Enter an expression: ")

    try:
        parse(expression)
        print("Valid expression")
    except SyntaxError as error:
        print(f"Invalid expression: {error}")


if __name__ == "__main__":
    main()
