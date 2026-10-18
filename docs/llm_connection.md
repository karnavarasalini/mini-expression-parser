# LLM Structured Output and Grammar-Constrained Generation

**Mini Expression Parser — Member 4 Documentation**
**Topic:** How Context-Free Grammars relate to LLM structured output

---

## 1. What Is a Large Language Model (LLM)?

A **Large Language Model** (LLM) is an AI system trained on massive amounts of
text data. Given some input (called a **prompt**), it generates text one token
at a time by predicting the most likely next word or character.

Popular examples include ChatGPT, Gemini, and LLaMA.

**Simple analogy:** Imagine auto-complete on your phone, but far more powerful.
Your phone predicts the next word based on a few previous words. An LLM does
the same thing, but it has read billions of sentences and can generate entire
paragraphs, code, or structured data.

**Key point:** LLMs generate text that *looks* correct, but they do not
inherently guarantee that the output follows a strict structure or grammar.
This is where grammar constraints become important.

---

## 2. What Is Grammar-Constrained Generation?

When we ask an LLM to produce output in a specific format — such as JSON, XML,
a mathematical expression, or a programming language — we need the output to
follow exact structural rules.

**Grammar-constrained generation** means restricting what the LLM is allowed to
produce at each step, so that the final output always conforms to a defined
grammar.

**Without constraints:**

```
Prompt:  "Write an arithmetic expression"
LLM:     "a + * b"    ← looks like math, but it is INVALID
```

**With grammar constraints:**

```
Prompt:  "Write an arithmetic expression"
LLM:     "a + b * c"  ← follows the grammar rules, VALID
```

The grammar acts like a set of guardrails — the LLM can still be creative
within the rules, but it cannot produce structurally broken output.

---

## 3. How a Context-Free Grammar (CFG) Helps Generate Structured Output

Our project uses the following **Context-Free Grammar** for arithmetic
expressions:

```
E  → T E'
E' → + T E' | - T E' | ε
T  → F T'
T' → * F T' | / F T' | ε
F  → ( E ) | id | num
```

### What does this grammar do?

Each rule tells us **how to build a valid expression**, step by step:

| Rule | Meaning in simple words |
|------|------------------------|
| `E → T E'` | An expression is a term, optionally followed by `+` or `-` and more terms |
| `T → F T'` | A term is a factor, optionally followed by `*` or `/` and more factors |
| `F → (E) \| id \| num` | A factor is a parenthesized expression, a variable name, or a number |

### Why does this matter for structured output?

If an LLM uses these rules when generating an arithmetic expression, it is
**impossible** for the output to contain errors like:

- Two operators in a row (`a + * b`)
- Missing operands (`a +`)
- Unmatched parentheses (`(a + b`)

The grammar defines a **tree-shaped structure**, which guarantees that every
operator has the right number of operands and every opening parenthesis has a
closing one.

---

## 4. How a Recursive Descent Parser Validates Expressions

A **recursive descent parser** is a program that reads an expression
character by character and checks whether it matches the grammar rules.

Each grammar rule becomes a **function** in the parser:

```
Grammar Rule          Parser Function
─────────────         ───────────────
E  → T E'             parse_E()
E' → + T E' | ε       parse_E_prime()
T  → F T'             parse_T()
T' → * F T' | ε       parse_T_prime()
F  → (E) | id | num   parse_F()
```

### How it works (step by step):

1. The parser starts at position 0 of the input string.
2. It calls `parse_E()`, which calls `parse_T()`, which calls `parse_F()`.
3. `parse_F()` checks: Is the current character a letter (identifier), a
   digit (number), or `(`? If yes, consume it and move forward.
4. After returning from `parse_F()`, `parse_T_prime()` checks: Is the next
   character `*` or `/`? If yes, consume it and call `parse_F()` again.
5. This process continues until the entire input is consumed.
6. If at any point the parser finds a character that does not match what the
   grammar expects, it **rejects** the expression and reports an error.

### What makes it "recursive"?

When the parser encounters `(`, it calls `parse_E()` again — from inside
`parse_F()`. This is a function calling itself indirectly, which is called
**recursion**. This is exactly what allows the parser to handle nested
parentheses like `((a + b) * c)`.

---

## 5. How Our Mini Expression Parser Relates to LLM Structured Output

Our project does **not** implement an actual LLM. What it demonstrates is the
**validation side** of the grammar-constrained generation pipeline.

Here is the connection:

```
┌─────────────────────────────────────────────────────────────────┐
│              GRAMMAR-CONSTRAINED LLM PIPELINE                  │
│                                                                 │
│  Step 1: Define the grammar                                     │
│          E → T E'                                               │
│          T → F T'     ← Our project defines this grammar       │
│          F → (E) | id | num                                     │
│                                                                 │
│  Step 2: LLM generates candidate output                        │
│          "a + b * c"  ← An LLM or a user provides this         │
│                                                                 │
│  Step 3: Parser validates the output                            │
│          RecursiveDescentParser checks the expression            │
│          ← Our project implements this step                     │
│                                                                 │
│  Step 4: Accept or reject                                       │
│          VALID   → use the expression                           │
│          INVALID → report error with position and reason        │
│          ← Our project implements this step (errors.py)         │
└─────────────────────────────────────────────────────────────────┘
```

In a real LLM system:
- **Step 1** would be provided to the LLM as a constraint.
- **Step 2** is done by the LLM itself.
- **Steps 3–4** are done by a parser/validator — exactly like our project.

Our project covers **Steps 1, 3, and 4**. Step 2 is simulated by the user
typing an expression.

---

## 6. Generating Valid Output vs. Validating Generated Output

These are two different but complementary tasks:

| Aspect | Generation | Validation |
|--------|-----------|------------|
| **Who does it?** | The LLM (or the user) | The parser |
| **What happens?** | Produce an expression | Check if it follows the grammar |
| **When does it happen?** | Before parsing | During parsing |
| **Uses grammar to...** | Restrict what can be produced | Verify what was produced |
| **Our project does this?** | No (user types the input) | **Yes** (parser checks it) |

### Why are both needed?

- **Generation alone** is not enough — even with constraints, bugs or
  edge cases might produce invalid output.
- **Validation alone** is not enough — rejecting bad output without the
  ability to regenerate is a dead end.

In a complete system, the LLM generates a candidate, the parser validates it,
and if it is invalid, the LLM is asked to try again. This loop continues until
valid output is produced.

```
         ┌──────────────┐
         │  LLM / User  │
         │  generates    │
         │  expression   │
         └──────┬───────┘
                │
                v
         ┌──────────────┐
         │   Parser      │
         │   validates   │
         └──────┬───────┘
                │
          ┌─────┴─────┐
          │           │
       VALID       INVALID
          │           │
          v           v
       Accept     Reject +
       & Use      Report Error
                      │
                      v
                  Retry / Fix
```

---

## 7. Practical Example: Valid and Invalid Expressions

### Example 1: Valid Expression — `a+b*c`

```
Input: a+b*c

Parser trace:
  parse_E()
    parse_T()
      parse_F() → reads 'a' (identifier)
      parse_T_prime() → no * or / → done
    parse_E_prime()
      reads '+' → calls parse_T()
        parse_F() → reads 'b' (identifier)
        parse_T_prime()
          reads '*' → calls parse_F()
            parse_F() → reads 'c' (identifier)
          parse_T_prime() → no more * or / → done
      parse_E_prime() → no more + or - → done

Result: VALID

Parse Tree:
  E
  ├── T
  │   └── F
  │       └── a
  └── E'
      ├── +
      └── T
          ├── F
          │   └── b
          ├── *
          └── F
              └── c
```

The grammar ensures that `*` binds `b` and `c` together before `+` combines
the result with `a`. This gives us the correct grouping: `a + (b * c)`.

### Example 2: Invalid Expression — `a+*b`

```
Input: a+*b

Parser trace:
  parse_E()
    parse_T()
      parse_F() → reads 'a' (identifier) ✓
      parse_T_prime() → no * or / → done
    parse_E_prime()
      reads '+' ✓ → calls parse_T()
        parse_F() → current character is '*'
                     '*' is NOT an identifier, number, or '('
                     ✗ ERROR!

Result: INVALID EXPRESSION

  Error position: 2
  Found: '*'
  Expected: identifier, number, or '('
  Reason: Unexpected operator where an operand is required.
```

The grammar rule `F → (E) | id | num` requires a factor (operand) after the
`+` operator. But the parser found `*` instead — another operator. This
violates the grammar, so the expression is rejected with a clear error message
showing exactly where and why it failed.

### More Invalid Examples from Our Test Set

| # | Expression | Position | Found | Error Category |
|---|-----------|----------|-------|---------------|
| 1 | `a+*b` | 2 | `*` | Unexpected operator |
| 2 | `a++b` | 2 | `+` | Repeated operator |
| 3 | `*a+b` | 0 | `*` | Leading operator |
| 4 | `a+b)` | 3 | `)` | Unexpected closing parenthesis |
| 5 | `(a+b` | 4 | EOF | Missing closing parenthesis |
| 6 | `a/(b-c` | 5 | EOF | Missing closing parenthesis |
| 7 | `a//b` | 2 | `/` | Repeated operator |
| 8 | `a+` | 2 | EOF | Missing operand |
| 9 | `()` | 1 | `)` | Empty parentheses |
| 10 | `a(b+c)` | 1 | `(` | Missing operator |

Each of these is caught because the grammar's rules are precise: every operator
needs operands on both sides, every `(` needs a matching `)`, and only valid
characters are accepted.

---

## 8. Real-World Applications of Grammar-Constrained Generation

Grammar-constrained generation is not just a classroom concept. It is used in
real systems today:

### 8.1 JSON Output from LLMs

Many applications need LLMs to return data in JSON format. A JSON grammar
ensures that the output always has matching braces, correct key-value syntax,
and proper comma placement.

```
Grammar constraint:  JSON object must have { "key": value } structure
LLM output:          {"name": "Alice", "age": 25}    ← VALID
Without constraint:  {name: Alice, age 25}            ← INVALID JSON
```

### 8.2 Code Generation

When an LLM generates Python, JavaScript, or SQL code, a grammar can ensure
that the output is syntactically valid — matching parentheses, correct keyword
usage, and proper indentation.

### 8.3 Form and Query Validation

Web forms that accept mathematical formulas, search queries, or filter
expressions use parsers to validate user input before processing it — exactly
like our project.

### 8.4 Tools Using This Concept

| Tool / System | How it uses grammar constraints |
|--------------|-------------------------------|
| OpenAI Structured Outputs | Forces LLM output to match a JSON schema |
| Guidance (Microsoft) | Applies grammar rules during text generation |
| LMQL | Adds query-language constraints to LLM prompts |
| Outlines (Python library) | Uses CFGs/regex to constrain LLM generation |
| Guardrails AI | Validates and re-asks when LLM output breaks format |

---

## 9. Limitations of Our Project

It is important to be honest about what our project does and does not do:

| What our project DOES | What our project does NOT do |
|-----------------------|-----------------------------|
| Defines a CFG for arithmetic expressions | Does not implement or connect to an actual LLM |
| Implements a recursive descent parser | Does not generate expressions automatically |
| Validates expressions and reports precise errors | Does not perform grammar-constrained generation |
| Explains the concept of CFG-constrained output | Does not build a production validation system |

**Our project demonstrates the validation half of the pipeline.** A real
grammar-constrained LLM system would combine our parser with an actual
language model that generates candidate expressions. Our project shows that
the parser can reliably accept valid expressions and reject invalid ones —
which is exactly what the validation component needs to do.

---

## 10. Conclusion

The Mini Expression Parser project demonstrates a fundamental concept from
the Theory of Computation: **Context-Free Grammars can define the structure of
a language, and recursive descent parsers can validate whether a given string
belongs to that language.**

This same principle is now used in modern AI systems. When a Large Language
Model needs to produce structured output (like JSON, code, or mathematical
expressions), a grammar defines what "valid" means, and a parser checks whether
the generated output follows those rules.

Our project covers:

1. **The grammar** — production rules that define valid arithmetic expressions
   (Member 1).
2. **The parser** — a recursive descent parser that processes expressions
   according to the grammar (Member 2).
3. **The visualization** — a parse tree that makes the structure visible
   (Member 3).
4. **The validation** — precise error messages when expressions are invalid,
   and this explanation of how the same ideas apply to LLM structured output
   (Member 4).

```
THEORY OF COMPUTATION          MODERN AI APPLICATION
─────────────────────          ─────────────────────
Context-Free Grammar    ←→    Output format specification
Recursive Descent Parser ←→   Grammar-constrained validator
Parse Tree              ←→    Structured output representation
Error Handler           ←→    Rejection + retry mechanism
```

The connection is clear: **the Theory of Computation provides the foundation
for building reliable, structured AI output systems.**

---

*Document prepared by Member 4 — Error Handling + LLM Connection*
*Mini Expression Parser | Theory of Computation Mini Project*
