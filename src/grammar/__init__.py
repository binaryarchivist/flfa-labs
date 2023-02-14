from typing import List

from .grammar import Grammar


def init() -> Grammar:
    vn: List[str] = ["S", "A", "B", "C"]
    vt: List[str] = ["a", "b"]
    p: List[List[str]] = [
        ["S", "aA"],
        ["A", "bS"],
        ["S", "aB"],
        ["B", "aC"],
        ["C", "a"],
        ["C", "bS"]
    ]

    grammar: Grammar = Grammar(vn, vt, p)
    grammar.generate_string("S")
    return grammar

