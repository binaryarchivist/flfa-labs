from grammar import Grammar
import unittest


class TestGrammar(unittest.TestCase):
    _grammar: Grammar

    def __init__(self, grammar: Grammar) -> None:
        super().__init__()
        self._grammar = grammar

    def test(self):
        result: str = self._grammar.generate_string()
        self.assertEqual('S', 'S')


def run_tests() -> None:
    unittest.main()
