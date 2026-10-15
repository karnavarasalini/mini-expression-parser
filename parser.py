class RecursiveDescentParser:
    def __init__(self, expression):
        self.expression = expression
        self.pos = 0

    def current(self):
        if self.pos < len(self.expression):
            return self.expression[self.pos]
        return None

    def eat(self, expected):
        if self.current() == expected:
            self.pos += 1
        else:
            raise SyntaxError(
                f"Expected '{expected}' at position {self.pos}"
            )

    # E -> T E'
    def E(self):
        self.T()
        self.E_prime()

    # E' -> + T E' | - T E' | epsilon
    def E_prime(self):
        while self.current() in ("+", "-"):
            operator = self.current()
            self.eat(operator)
            self.T()

    # T -> F T'
    def T(self):
        self.F()
        self.T_prime()

    # T' -> * F T' | / F T' | epsilon
    def T_prime(self):
        while self.current() in ("*", "/"):
            operator = self.current()
            self.eat(operator)
            self.F()

    # F -> (E) | id | num
    def F(self):
        current = self.current()

        if current == "(":
            self.eat("(")
            self.E()
            self.eat(")")

        elif current is not None and current.isalpha():
            while (
                self.current() is not None
                and self.current().isalnum()
            ):
                self.pos += 1

        elif current is not None and current.isdigit():
            while (
                self.current() is not None
                and self.current().isdigit()
            ):
                self.pos += 1

        else:
            raise SyntaxError(
                f"Expected an identifier, number, or '(' "
                f"at position {self.pos}"
            )

    def parse(self):
        self.E()

        if self.current() is not None:
            raise SyntaxError(
                f"Unexpected symbol '{self.current()}' "
                f"at position {self.pos}"
            )


def main():
    expression = input("Enter an arithmetic expression: ")

    # Remove spaces before parsing
    expression = "".join(expression.split())

    parser = RecursiveDescentParser(expression)

    try:
        parser.parse()
        print("Valid expression!")
    except SyntaxError as error:
        print("Invalid expression!")
        print("Error:", error)


if __name__ == "__main__":
    main()