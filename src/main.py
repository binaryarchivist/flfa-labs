from typing import List, Tuple

from grammar import Grammar, FiniteAutomaton


def main() -> int:
    vn: List[str] = ["S", "A", "B", "C"]
    vt: List[str] = ["a", "b"]
    p: List[Tuple[str, str, str]] = [
        ('S', 'a', 'A'),
        ('A', 'b', 'S'),
        ('S', 'a', 'B'),
        ('B', 'a', 'C'),
        ('C', 'a', 'X'),
        ('C', 'b', 'S'),
        ('A', 'a', 'C'),
    ]

    gram: Grammar = Grammar(vn, vt, p)
    fa: FiniteAutomaton = gram.to_finite_automaton()
    fa.to_deterministic()

    print("Generated by grammar class: \n")
    for _ in range(1, 50):
        s = gram.generate_string("S")
        print("string: ", s, " fa:", fa.accepts(s))

    print("\n\nFalse cases: \n")
    false_cases: List[str] = ['ab', 'abbaaaa', 'aa', 'ababababababb', 'abaaaa', 'baaaaaaa']
    for s in false_cases:
        print(s, ':', fa.accepts(s))

    return 0


main()
