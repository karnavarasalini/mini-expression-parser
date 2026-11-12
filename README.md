# Mini Expression Parser

A Python-based Mini Expression Parser using a Context-Free Grammar (CFG) and Recursive Descent Parsing.

## Features

- Supports addition (+), subtraction (-), multiplication (*), and division (/).
- Supports parentheses for grouping expressions.
- Supports identifiers and numeric values, including decimal numbers.
- Follows operator precedence: multiplication and division before addition and subtraction.
- Includes a parse-tree visualizer.
- Detects invalid expressions and reports syntax errors.

## Requirements

- Python 3
- No external libraries are required for the basic parser.

## Setup

Clone the repository:

```bash
git clone https://github.com/karnavarasalini/mini-expression-parser.git
cd mini-expression-parser
```

## Grammar

The parser uses the following grammar, rewritten to avoid left recursion for recursive descent parsing:

```text
E  -> T E'
E' -> + T E' | - T E' | epsilon
T  -> F T'
T' -> * F T' | / F T' | epsilon
F  -> (E) | id | num
```

Where:
- `E` represents an expression.
- `T` represents a term.
- `F` represents a factor.
- `id` represents an identifier.
- `num` represents a number.
- `epsilon` represents an empty production.

## Running the Parser

Validate an expression:

```bash
python parser.py "a+b*c"
```

Expected result: the expression is accepted as valid.

Try a decimal expression:

```bash
python parser.py "3.14*x+10"
```

## Running the Parse-Tree Visualizer

Run:

```bash
python tree_visualizer.py
```

Enter an expression when prompted, for example:

```text
3.14*x+10
```

The program displays whether the expression is valid and prints its grammar parse tree.

## Valid Test Cases

| No. | Expression | Expected Result |
|---:|---|---|
| 1 | `a` | Valid |
| 2 | `5` | Valid |
| 3 | `10+20` | Valid |
| 4 | `a+b` | Valid |
| 5 | `a-b` | Valid |
| 6 | `a*b` | Valid |
| 7 | `a/b` | Valid |
| 8 | `a+b*c` | Valid |
| 9 | `(a+b)*c` | Valid |
| 10 | `a-b-c` | Valid |
| 11 | `a/b*c` | Valid |
| 12 | `((x-y)/z)+1` | Valid |
| 13 | `3.14` | Valid |
| 14 | `3.14*x+10` | Valid |
| 15 | `variable_1+25` | Valid |

## Invalid Test Cases

| No. | Expression | Expected Result |
|---:|---|---|
| 1 | `a+*b` | Invalid |
| 2 | `(a+b` | Invalid |
| 3 | `3.1.4*x` | Invalid in the parse-tree visualizer |

## Running Tests

Run the error-handling unit tests:

```bash
python -m unittest discover -s tests -v
```

Run the invalid-expression tests:

```bash
python tests/invalid_tests.py
```

Previously verified development results:
- 31 error-handling unit tests passed.
- 15 valid expressions passed in the parse-tree visualizer.
- 3 invalid expressions were rejected by the parse-tree visualizer.

Run these commands again before submission to confirm the current results.

## Project Structure

```text
mini-expression-parser/
├── docs/
│   └── cfg_theory.md
├── parser/
├── parser.py
├── tree_visualizer.py
├── errors.py
├── tests/
│   ├── invalid_tests.py
│   └── test_errors.py
└── README.md
```

## Conclusion

This project demonstrates how Context-Free Grammars and Recursive Descent Parsing can be used to recognize arithmetic expressions, apply operator precedence, construct parse trees, and identify syntax errors.
