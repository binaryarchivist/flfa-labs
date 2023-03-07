from typing import List, Tuple

from grammar_impl import Grammar
from finite_automaton import FiniteAutomaton


# helper class for lab2 to avoid circular dependency 3.a
class Converter:
    def __init__(self):
        return

    def to_grammar(self, fa: FiniteAutomaton) -> Grammar:
        vt = fa.sigma
        vn = fa.Q
        p = fa.delta
        return Grammar(vn, vt, p)

    def to_automaton(self, grammar: Grammar) -> FiniteAutomaton:
        Q = grammar._vn
        sigma = grammar._vt
        delta = grammar._p

        return FiniteAutomaton(Q, sigma, delta, '0', 'X')


def main() -> int:
    Q: List[str] = ['0', '1', '2', '3']
    sigma: List[str] = ['a', 'b']
    delta: List[Tuple[str, str, str]] = [
        ('0', 'a', '0'),
        ('0', 'a', '1'),
        ('1', 'b', '2'),
        ('2', 'a', '2'),
        ('3', 'a', '3'),
        ('3', 'a', 'X'),
        ('2', 'b', '3'),
        ('2', 'b', 'X')
    ]

    converter: Converter = Converter()

    grammar: Grammar = Grammar(Q, sigma, delta)
    fa: FiniteAutomaton = converter.to_automaton(grammar)
    fa.to_deterministic()
    print(fa.is_nfa())
    print(fa.delta)

    s = grammar.generate_string("0")
    print("string: ", s, " fa:", fa.accepts(s))

    fa.graph()
    # for _ in range(1, 50):
    #     s = grammar.generate_string("0")
    # print("string: ", s, " fa:", fa.accepts(s))

    return 0


main()
