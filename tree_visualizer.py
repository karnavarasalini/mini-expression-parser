
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []


def print_tree(node, prefix="", is_last=True, is_root=True):
    if is_root:
        print(node.value)
    else:
        branch = "└── " if is_last else "├── "
        print(prefix + branch + node.value)

    if is_root:
        child_prefix = ""
    else:
        child_prefix = prefix + ("    " if is_last else "│   ")

    for i, child in enumerate(node.children):
        last_child = i == len(node.children) - 1
        print_tree(child, child_prefix, last_child, False)


class RecursiveDescentParser:
    def __init__(self, expression):
        self.expression = expression
        self.pos = 0

    def skip_spaces(self):
        while (
            self.pos < len(self.expression)
            and self.expression[self.pos].isspace()
        ):
            self.pos += 1

    def current(self):
        self.skip_spaces()
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
        return Node("E", [self.T(), self.E_prime()])

    # E' -> + T E' | - T E' | epsilon
    def E_prime(self):
        if self.current() in ("+", "-"):
            operator = self.current()
            self.eat(operator)
            return Node(
                "E'",
                [Node(operator), self.T(), self.E_prime()]
            )

        return Node("E'", [Node("ε")])

    # T -> F T'
    def T(self):
        return Node("T", [self.F(), self.T_prime()])

    # T' -> * F T' | / F T' | epsilon
    def T_prime(self):
        if self.current() in ("*", "/"):
            operator = self.current()
            self.eat(operator)
            return Node(
                "T'",
                [Node(operator), self.F(), self.T_prime()]
            )

        return Node("T'", [Node("ε")])

    # F -> (E) | id | num
        # F -> (E) | id | num
    def F(self):
        current = self.current()

        if current == "(":
            self.eat("(")
            expression_node = self.E()
            self.eat(")")
            return Node(
                "F",
                [Node("("), expression_node, Node(")")]
            )

        if current is not None and (
            current.isalpha() or current == "_"
        ):
            start = self.pos

            while self.pos < len(self.expression) and (
                self.expression[self.pos].isalnum()
                or self.expression[self.pos] == "_"
            ):
                self.pos += 1

            identifier = self.expression[start:self.pos]
            return Node("F", [Node("id: " + identifier)])

        if current is not None and current.isdigit():
            start = self.pos
            decimal_points = 0

            while self.current() is not None and (
                self.current().isdigit() or self.current() == "."
            ):
                if self.current() == ".":
                    decimal_points += 1
                    if decimal_points > 1:
                        raise SyntaxError(
                            f"Invalid number at position {self.pos}"
                        )
                self.pos += 1

            number = self.expression[start:self.pos]

            if number.endswith("."):
                raise SyntaxError(
                    f"Invalid number at position {self.pos - 1}"
                )

            return Node("F", [Node("num: " + number)])

        found = self.current()

        if found is None:
            message = "found end of expression"
        else:
            message = f"found '{found}'"

        raise SyntaxError(
            f"Expected an identifier, number, or '(' "
            f"at position {self.pos}, {message}"
        )
    def parse(self):
        if not self.expression:
            raise SyntaxError("Expression cannot be empty")

        root = self.E()

        if self.current() is not None:
            raise SyntaxError(
                f"Unexpected symbol '{self.current()}' "
                f"at position {self.pos}"
            )

        return root


def main():
    expression = input("Enter an arithmetic expression: ")

    try:
        parser = RecursiveDescentParser(expression)
        root = parser.parse()

        print("\nValid expression!")
        print("\nGrammar Parse Tree:")
        print_tree(root)

    except SyntaxError as error:
        print("\nInvalid expression!")
        print("Error:", error)


if __name__ == "__main__":
    main()
