# Topic: Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Nastas Corneliu

----

## Abstract:
In this laboratory work I'll present the Lexer/Tokenizer I've implemented for my PBL group. Our syntax is very C-style inspired.


## Theory:
The first transformation, from source code to tokens, is called “lexical analysis”, or “lexing” for
short. It’s done by a lexer (also called tokenizer or scanner).
Tokens are small, easily categorizable data structures that are then fed to the parser, which
does the second transformation and turns the tokens into an “Abstract Syntax Tree”

## Objectives:
1. Understand what lexical analysis [1] is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.


## Implementation description:
**Tokens**

```python3
"""tokens.py"""
ILLEGAL = "ILLEGAL"
EOF = "EOF"

# Identifiers
IDENT = "IDENT"  # x, y, test, temp, ...
INT = "INT"  # 123456789

# OPERATORS
ASSIGN = "="

# Delimiters
COMMA = ","
DOT = "."
SEMICOLON = ";"
LBRACE = "{"
RBRACE = "}"
COLON = ':'

# Keywords
PLACE = "PLACE"
TRAN = "TRAN"

keywords: dict = {
    "place": PLACE,
    "tran": TRAN
}
```
All the Tokens are predefined in the `tokens.py` file. Some tokens need also a `literal` type for example `IDENTIFIER` token.



```python3
def lookup_ident(ident: str):
    if ident in keywords:
        return keywords[ident]
    return IDENT
```

The `lookup_ident` function checks the keywords dictionary to see whether the given identified is a keyword. If it is it returns its type constant, if it isn't we simply return IDENT type.


```python3
"""tokenizer.py"""
class Token:
    def __init__(self, type: str, literal: str = None) -> any:
        self.type = type
        self.literal = literal

    def __str__(self) -> str:
        if self.literal:
            return f'Type {self.type} : Literal {self.literal}'
        return f'Type {self.type}'
```

A simple Token class used for defining token structure.

## Lexer/Tokenizer/Scanner:
```python3
class Tokenizer:
    def __init__(self, input: str) -> any:
        self.input: str = input  # input text
        # current position in input (points to current character)
        self.cursor: int = 0
        # current reading position in input (after current character)
        self.read_cursor: int = 0
        self.ch = ''  # current character under examination, need to see how to get byte or rune type in python3
        self.read_char()
```

The reason for two pointers: we need to see further beyond the character we currently read. 

`read_cursor` will always point to "next" character of input.

`cursor` will always point to the character in the input that corresponds to ch byte


```python3
  def read_char(self) -> any:
        if self.read_cursor >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.read_cursor]
        self.cursor = self.read_cursor
        self.read_cursor += 1
```

Purpose of `read_char` method is to `get next character` and `advance our position` in `input`.

It begins by checking whether the end of the input has been reached.
If so, the method sets the variable `ch to 0`, which represents the `ASCII` code for the `"NULL"` character and indicates that we have either not yet read anything or have reached the end of the file.

Once `ch` has been set to the appropriate value, the method updates the `cursor` to the `position` just used by `read_cursor` and `increments read_cursor by one`.

This ensures that `read_cursor` always `points to the next position` in the input string that will be read, while `cursor always points to the most recent position` that has been read.


```python3
    def next_token(self) -> any:
        tok: Token = Token(token.EOF, "")
        self.consume_whitespace()

        if self.ch == "=":
            tok = Token(token.ASSIGN)
        elif self.ch == ':':
            tok = Token(token.COLON)
        elif self.ch == ';':
            tok = Token(token.SEMICOLON)
        elif self.ch == ',':
            tok = Token(token.COMMA)
        elif self.ch == '.':  # extend for fields (amm, cap, in, out)
            tok = Token(token.DOT)
        elif self.ch == '{':
            tok = Token(token.LBRACE)
        elif self.ch == '}':
            tok = Token(token.RBRACE)
        elif self.ch == 0:
            tok = Token(token.EOF)
        else:
            if is_letter(self.ch):
                tok.literal = self.read_identifier()
                tok.type = token.lookup_ident(tok.literal)
                return Token(tok.type, tok.literal)
            if is_digit(self.ch) and self.ch != '0':
                tok.literal = self.read_number()
                tok.type = token.INT
                return Token(token.INT, tok.literal)

            tok = Token(token.ILLEGAL, self.ch)

        self.read_char()

        return tok
```
`next_token()` is a method that returns the next token in the input stream. It starts by creating a token object with a type of EOF and an empty literal string, and skips over any whitespace in the input. The method then checks the next character in the input stream and assigns the appropriate token type to the token object. 

If `the character is a letter`, it reads the entire identifier and assigns the appropriate token type. If the character is a non-zero digit, it reads the entire number and assigns the INT token type.

If `the character is illegal`, the token object is assigned an ILLEGAL type. 

The method then advances to the next character in the input stream and returns the token object.

```python3
    def read_identifier(self) -> str:
        cursor: int = self.cursor

        while is_letter(self.ch) or is_digit(self.ch):
            self.read_char()

        return self.input[cursor: self.cursor]
```

The method `read_identifier()` reads a string of characters from the current cursor position until it encounters a non-letter or non-digit character, and returns the substring starting from the initial cursor position.

```python3
    def read_number(self) -> str:
        cursor: int = self.cursor

        while is_digit(self.ch):
            self.read_char()

        return self.input[cursor: self.cursor]
```

The method `read_number() `reads a string of digits from the current cursor position until it encounters a non-digit character, and returns the substring starting from the initial cursor position.

```python3
    def consume_whitespace(self) -> None:
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
            self.read_char()
```

The method `consume_whitespace()` reads and discards any consecutive whitespace characters, including spaces, tabs, newlines, and carriage returns, until a non-whitespace character is encountered.

**Helper functions:**
```python3
def is_letter(ch: str) -> bool:
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == '_'


def is_digit(ch: str) -> bool:
    return '0' <= ch <= '9'
```

## Results:

Tokenizer will tokenize the following input:
```python3
input: str = """
        place p1, p2;
        place p3, p4;
        tran t1, t2;
        p1.amm = 3;
        p1.cap = 4;
        p2.cap = 4;
        t1.out = {p1 : 2, p2 : 3};
        p1.out = {t2 : 5};
        p2.in = {t1, t2};
        t2.in = {p3, p4};"""
```

Tokens:
```python3
[Type PLACE : Literal place,
 Type IDENT : Literal p1,
 Type ,,
 Type IDENT : Literal p2,
 Type ;,
 Type PLACE : Literal place,
 Type IDENT : Literal p3,
 Type ,,
 Type IDENT : Literal p4,
 Type ;,
 Type TRAN : Literal tran,
 Type IDENT : Literal t1,
 Type ,,
 Type IDENT : Literal t2,
 Type ;,
 Type IDENT : Literal p1,
 Type .,
 Type IDENT : Literal amm,
 Type =,
 Type INT : Literal 3,
 Type ;,
 Type IDENT : Literal p1,
 Type .,
 Type IDENT : Literal cap,
 Type =,
 Type INT : Literal 4,
 Type ;,
 Type IDENT : Literal p2,
 Type .,
 Type IDENT : Literal cap,
 Type =,
 Type INT : Literal 4,
 Type ;,
 Type IDENT : Literal t1,
 Type .,
 Type IDENT : Literal out,
 Type =,
 Type {,
 Type IDENT : Literal p1,
 Type :,
 Type INT : Literal 2,
 Type ,,
 Type IDENT : Literal p2,
 Type :,
 Type INT : Literal 3,
 Type },
 Type ;,
 Type IDENT : Literal p1,
 Type .,
 Type IDENT : Literal out,
 Type =,
 Type {,
 Type IDENT : Literal t2,
 Type :,
 Type INT : Literal 5,
 Type },
 Type ;,
 Type IDENT : Literal p2,
 Type .,
 Type IDENT : Literal in,
 Type =,
 Type {,
 Type IDENT : Literal t1,
 Type ,,
 Type IDENT : Literal t2,
 Type },
 Type ;,
 Type IDENT : Literal t2,
 Type .,
 Type IDENT : Literal in,
 Type =,
 Type {,
 Type IDENT : Literal p3,
 Type ,,
 Type IDENT : Literal p4,
 Type },
 Type ;,
 Type EOF]

```
## Conclusions
In this laboratory work I've implemented a Tokenizer that is used by my PBL team and it is inspired by a book regarding writing interpreters. I had to predefine the tokens I am going to use and find a way to process identifiers, numbers and special tokens. Overall it was a learning experience build my own tokenizer.



## References:
[1] [Writing an interpreter in Go](https://interpreterbook.com/)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)
 