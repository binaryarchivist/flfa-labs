from typing import List, Tuple

from modules import Grammar, FiniteAutomaton
import networkx as nx
import matplotlib.pyplot as plt

# helper class for lab2 to avoid circular dependency 3.a
class Converter:
    def __init__(self):
        return
    
    def to_grammar(self, fa: FiniteAutomaton) -> Grammar:
        return Grammar(fa.states, fa.alphabet, fa.transitions)

    def to_automaton(self, grammar: Grammar) -> FiniteAutomaton:
        return FiniteAutomaton(grammar._vn, grammar._vt, grammar._p, 'Q0', {'Q3'})

def main() -> int:
    vn: List[str] = ["Q0", "Q1", "Q2", "Q3"]
    vt: List[str] = ["a", "b"]
    p: List[Tuple[str, str, str]] = [
        ('Q0', 'a', 'Q0'),
        ('Q0', 'a', 'Q1'),
        ('Q1', 'b', 'Q2'),
        ('Q2', 'a', 'Q2'),
        ('Q3', 'a', 'Q3'),
        ('Q2', 'b', 'Q3'),
    ]
    converter: Converter = Converter()

    grammar: Grammar = Grammar(vn, vt, p)
    fa: FiniteAutomaton = converter.to_automaton(grammar)
    fa.to_deterministic()
    print(fa.transitions)
    return 0


main()
