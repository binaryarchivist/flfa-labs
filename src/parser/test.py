from ast import Parser, PlaceDeclarationNode, AssignmentNode
from tokenizer import Tokenizer
from tokens import EOF



input: str = """
    place p1;
    p1.amm = 10;
"""
tokenizer = Tokenizer(input)
tokens: list = []
token = tokenizer.next_token()
while token.type is not EOF:
    tokens.append(token)
    token = tokenizer.next_token()

p = Parser(tokens)
tree = p.parse()

for node in tree:
    if isinstance(node, PlaceDeclarationNode):
        print(f"Place declared: {node.place_name}")
    elif isinstance(node, AssignmentNode):
        print(f"Assignment: {node.place_name}.{node.attribute} = {node.value}")