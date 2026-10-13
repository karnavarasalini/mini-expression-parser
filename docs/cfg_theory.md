# Mini Expression Parser — CFG Theory

## 1. Project Overview

The Mini Expression Parser project studies Context-Free Grammar (CFG), derivations, parse trees, and recursive descent parsing. It uses arithmetic expressions to demonstrate how grammar rules describe valid expressions.

## 2. Final Context-Free Grammar (CFG)

The final CFG covers addition, subtraction, multiplication, division, parentheses, identifiers, and numbers.

```text
E → E + T | E - T | T
T → T * F | T / F | F
F → (E) | id | num
```

Here, `E`, `T`, and `F` are non-terminal symbols, while the operators, parentheses, `id`, and `num` represent terminals or terminal tokens.

## 3. Explanation of Symbols

- **E — Expression:** Represents an arithmetic expression containing addition, subtraction, or a term.
- **T — Term:** Represents a term containing multiplication, division, or a factor.
- **F — Factor:** Represents an identifier, a number, or a parenthesized expression.
- **id — Identifier:** A variable such as `a`, `x`, or `variable`.
- **num — Number:** A numeric value such as `5` or `10`.
- **→ — Production:** Indicates that a non-terminal can be replaced according to a grammar rule.
- **| — Alternative:** Indicates a choice between production rules.

## 4. Explanation of Production Rules

### Expression

`E → E + T | E - T | T`

An expression can be an addition, a subtraction, or a term. Addition and subtraction are handled at the expression level.

### Term

`T → T * F | T / F | F`

A term can be a multiplication, a division, or a factor. Multiplication and division are handled at the term level.

### Factor

`F → (E) | id | num`

A factor can be a parenthesized expression, an identifier, or a number.

## 5. Operator Precedence and Associativity

The grammar separates expressions, terms, and factors to represent operator precedence.

- **Highest level:** Parentheses determine which expression is grouped first.
- **Higher precedence:** Multiplication (`*`) and division (`/`).
- **Lower precedence:** Addition (`+`) and subtraction (`-`).

Examples:

- `a + b * c` is grouped as `a + (b * c)`.
- `a - b / c` is grouped as `a - (b / c)`.
- `(a + b) * c` groups `a + b` before multiplication.
- `a - b - c` is grouped as `(a - b) - c` under the left-associative interpretation of the grammar.

Multiplication and division have equal precedence in this grammar, as do addition and subtraction.

## 6. Scope and Grammar Considerations

The final grammar includes all four arithmetic operators, parentheses, identifiers, and numbers, as required by the project description.

The grammar is left-recursive. This form is suitable for explaining CFG derivations and parse trees, but a conventional recursive descent parser cannot implement it directly without transformation. Member 2 is responsible for using an equivalent non-left-recursive grammar in the parser implementation.

The theory grammar and the implementation grammar should describe the same language and preserve the intended operator precedence and associativity.
## 7. Member 1 Responsibility

Member 1 is responsible for documenting the CFG rules, tracing derivations for three expressions, and preparing parse trees by hand.

## 8. Derivations and Parse Trees

Three example expressions will be selected to demonstrate how valid expressions are generated using the CFG. Each derivation will show the sequence of production rules applied, and each corresponding parse tree will show the hierarchical structure of the expression.

The selected examples should demonstrate operator precedence and the use of parentheses. The derivations and parse trees will be completed as part of Member 1's theory work.

### 8.1 Derivation of `a + b * c`

**Expression:** `a + b * c`

**Leftmost derivation:**

```text
E
⇒ E + T
⇒ T + T
⇒ F + T
⇒ id + T
⇒ id + T * F
⇒ id + F * F
⇒ id + id * F
⇒ id + id * id
```

Replacing `id` with the identifiers `a`, `b`, and `c` gives:

```text
a + b * c
```

**Result:** The expression is valid according to the CFG. The grammar places multiplication inside `T`, so `b * c` is grouped before addition.

### 8.2 Derivation of `(a + b) * c`

**Expression:** `(a + b) * c`

**Leftmost derivation:**

```text
E
⇒ T
⇒ T * F
⇒ F * F
⇒ (E) * F
⇒ (E + T) * F
⇒ (T + T) * F
⇒ (F + T) * F
⇒ (id + T) * F
⇒ (id + F) * F
⇒ (id + id) * F
⇒ (id + id) * id
```

Replacing `id` with `a`, `b`, and `c` gives `(a + b) * c`.

**Result:** The expression is valid according to the CFG. The parentheses force `a + b` to be evaluated as a group before multiplication by `c`.


### 8.3 Derivation of `((x - y) / z) + 1`

**Expression:** `((x - y) / z) + 1`

**Leftmost derivation:**

```text
E
⇒ E + T
⇒ T + T
⇒ F + T
⇒ (E) + T
⇒ (T) + T
⇒ (T / F) + T
⇒ (F / F) + T
⇒ ((E) / F) + T
⇒ ((E - T) / F) + T
⇒ ((T - T) / F) + T
⇒ ((F - T) / F) + T
⇒ ((id - T) / F) + T
⇒ ((id - F) / F) + T
⇒ ((id - id) / F) + T
⇒ ((id - id) / id) + T
⇒ ((id - id) / id) + F
⇒ ((id - id) / id) + num
```

Replacing `id` with `x`, `y`, and `z`, and `num` with `1`, gives:

```text
((x - y) / z) + 1
```

**Result:** The expression is valid according to the CFG. The grammar allows subtraction inside the parentheses, division by `z`, and addition of `1`. The parentheses determine the grouping of the expression.

## 9. Parse Trees

### 9.1 Parse Tree for `a + b * c`

```text
                 E
              /  |  \
             E   +   T
             |      / | \
             T     T  *  F
             |     |     |
             F     F    id(c)
             |     |
           id(a) id(b)
```

### 9.2 Parse Tree for `(a + b) * c`

```text
                 E
                 |
                 T
              /  |  \
             T   *   F
             |       |
             F     id(c)
          /  |  \
         (   E   )
            / | \
           E  +  T
           |     |
           T     F
           |     |
           F    id(b)
           |
          id(a)
```

### 9.3 Parse Tree for `((x - y) / z) + 1`

```text
                         E
                      /  |  \
                     E   +   T
                     |       |
                     T       F
                     |       |
                     F     num(1)
                  /  |  \
                 (   E   )
                    / | \
                   T  /  F
                   |     |
                   F    id(z)
                /  |  \
               (   E   )
                  / | \
                 E  -  T
                 |     |
                 T     F
                 |     |
                 F    id(y)
                 |
               id(x)
```

**Note:** `id` represents an identifier, and `num` represents a number. Each parse tree illustrates how the expression is structured according to the CFG.



## 10. Pushdown Automaton (PDA) Theory

### 10.1 What is a PDA?

A Pushdown Automaton (PDA) is a computational model that uses a stack to recognize languages. Unlike a finite automaton, a PDA has additional memory in the form of a stack.

A PDA is important in parsing because it can handle nested structures, such as parentheses in arithmetic expressions.

### 10.2 Role of PDA in the Mini Expression Parser

The Mini Expression Parser uses a Context-Free Grammar (CFG) to define valid arithmetic expressions. A PDA can recognize the language described by a CFG by using its stack to track grammar symbols and match the input according to production rules.

For this project, the PDA concept helps explain how an expression such as `((x - y) / z) + 1` can be processed while respecting nested parentheses and the grammatical structure of arithmetic operations.

### 10.3 Basic Working Principle

1. The input expression is provided to the automaton.
2. The stack stores grammar symbols that still need to be processed.
3. A non-terminal symbol can be replaced according to an applicable production rule.
4. Terminal symbols are matched against the input symbols.
5. Processing succeeds when the input has been consumed and the stack has been handled according to the chosen acceptance convention.

A CFG can be converted into an equivalent PDA. This explains the theoretical relationship between the grammar used to describe expressions and the stack-based model used to recognize them.

### 10.4 Example: Parentheses

Consider the expression `(a + b) * c`.

The PDA concept helps explain how nested parentheses are handled. The opening parenthesis introduces a grouped expression, and the matching closing parenthesis completes that group. The stack provides memory for tracking nested grammatical structures.

Tracking parentheses alone is not enough to validate the entire arithmetic expression. The operators, operands, and their arrangement must also satisfy the grammar.

### 10.5 Conclusion

The CFG defines the syntax of valid expressions, derivations show how expressions can be generated from the grammar, and parse trees represent their hierarchical structure. PDA theory explains how stack-based computation can recognize context-free languages and handle nested structures.