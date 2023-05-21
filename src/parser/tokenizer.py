import tokens as token


class Tokenizer:
    def __init__(self, input: str) -> any:
        self.input: str = input  # input text
        # current position in input (points to current character)
        self.cursor: int = 0
        # current reading position in input (after current character)
        self.read_cursor: int = 0
        self.ch = ''  # current character under examination, need to see how to get byte or rune type in python3
        self.read_char()
        '''
        the reason for two pointers: we need to see further beyond the character we currently read. 
        read_cursor will always point to "next" character of input.
        cursor will always point to the character in the input that corresponds to ch byte
        '''

    '''
    Purpose of read_char method is to get next character and advance our position in input.
    '''

    def read_char(self) -> any:
        if self.read_cursor >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.read_cursor]
        self.cursor = self.read_cursor
        self.read_cursor += 1

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

    def read_identifier(self) -> str:
        cursor: int = self.cursor

        while is_letter(self.ch) or is_digit(self.ch):
            self.read_char()

        return self.input[cursor: self.cursor]

    def read_number(self) -> str:
        cursor: int = self.cursor

        while is_digit(self.ch):
            self.read_char()

        return self.input[cursor: self.cursor]

    def consume_whitespace(self) -> None:
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
            self.read_char()


class Token:
    def __init__(self, type: str, literal: str = None) -> any:
        self.type = type
        self.literal = literal

    def __str__(self) -> str:
        if self.literal:
            return f'Type {self.type} : Literal {self.literal}'
        return f'Type {self.type}'

    __repr__ = __str__


def is_letter(ch: str) -> bool:
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == '_'


def is_digit(ch: str) -> bool:
    return '0' <= ch <= '9'
