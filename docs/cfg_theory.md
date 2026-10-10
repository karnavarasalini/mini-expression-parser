# Mini Expression Parser — CFG Theory

## 1. Project Overview

The Mini Expression Parser project studies Context-Free Grammar (CFG), derivations, parse trees, and recursive descent parsing. It uses arithmetic expressions to demonstrate how grammar rules describe valid expressions.

## 2. Context-Free Grammar (CFG)

The CFG given in the project specification is:

```text
E → E + T | T
T → T * F | F
F → (E) | id | num
```

## 3. Explanation of Symbols

- **E — Expression:** Represents an arithmetic expression.
- **T — Term:** Represents a term in an expression.
- **F — Factor:** Represents a basic operand or a parenthesized expression.
- **id — Identifier:** A variable such as `a`, `x`, or `variable`.
- **num — Number:** A numeric value such as `5` or `10`.
- **→ — Production:** Indicates that a symbol can be replaced according to a grammar rule.
- **| — Alternative:** Indicates a choice between production rules.

## 4. Explanation of Production Rules

### Expression

`E → E + T | T`

An expression can consist of an expression followed by `+` and a term, or it can be a term.

### Term

`T → T * F | F`

A term can consist of a term followed by `*` and a factor, or it can be a factor.

### Factor

`F → (E) | id | num`

A factor can be a parenthesized expression, an identifier, or a number.

## 5. Operator Precedence

The grammar places multiplication at the term level and addition at the expression level. This represents multiplication as having higher precedence than addition.

For example:

- `a + b * c` is grouped as `a + (b * c)`.
- `(a + b) * c` groups `a + b` before multiplication.

## 6. Scope of the Given Grammar

The specified grammar explicitly includes addition, multiplication, parentheses, identifiers, and numbers. The complete project description also requires subtraction and division. Those operators must be addressed in the final grammar used by the implementation.

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

### 8.3 Derivation of `(x) + 5`

**Expression:** `(x) + 5`

**Leftmost derivation:**

```text
E
⇒ E + T
⇒ T + T
⇒ F + T
⇒ (E) + T
⇒ (T) + T
⇒ (F) + T
⇒ (id) + T
⇒ (id) + F
⇒ (id) + num
```

Replacing `id` with `x` and `num` with `5` gives `(x) + 5`.

**Result:** The expression is valid according to the CFG. The grammar permits a parenthesized expression as a factor and allows identifiers and numbers as operands.

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
              /   |   \
             T    *    F
             |         |
             F        id(c)
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

### 9.3 Parse Tree for `(x) + 5`

```text
                 E
              /  |  \
             E   +   T
             |       |
             T       F
             |       |
             F     num(5)
          /  |  \
         (   E   )
             |
             T
             |
             F
             |
           id(x)
```

**Note:** `id` represents an identifier, and `num` represents a number. The trees illustrate the hierarchical structure of each expression according to the given grammar.