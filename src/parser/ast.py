class PlaceDeclarationNode:
    def __init__(self, place_name):
        self.place_name = place_name

class AssignmentNode:
    def __init__(self, place_name, attribute, value):
        self.place_name = place_name
        self.attribute = attribute
        self.value = value

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.next()

    def next(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        nodes = []
        while self.current_token is not None:
            if self.current_token.type == "PLACE":
                nodes.append(self.parse_place_declaration())
            else:
                nodes.append(self.parse_assignment())
        return nodes

    def parse_place_declaration(self):
        self.next()  # consume the "PLACE" token
        place_name = self.current_token.literal
        self.next()  # consume the "IDENT" token
        if self.current_token.type != ';':
            raise Exception("Invalid Syntax, expected ';'")

        self.next()  # consume the ";" token
        return PlaceDeclarationNode(place_name)

    def parse_assignment(self):
        place_name = self.current_token.literal
        self.next()  # consume the "IDENT" token
        if self.current_token.type != '.':
            raise Exception("Invalid Syntax, expected '.'")

        self.next()  # consume the "." token
        attribute = self.current_token.literal
        self.next()  # consume the "IDENT" token
        if self.current_token.type != '=':
            raise Exception("Invalid Syntax, expected '='")

        self.next()  # consume the "=" token
        value = self.current_token.literal
        self.next()  # consume the "INT" token
        if self.current_token.type != ';':
            raise Exception("Invalid Syntax, expected ';'")

        self.next()  # consume the ";" token
        return AssignmentNode(place_name, attribute, value)
