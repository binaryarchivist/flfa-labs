from typing import Tuple, List


class FiniteAutomaton:
    def __init__(self, tran: List[Tuple[str, str, str]]):
        self.transitions: List[Tuple[str, str, str]] = tran
        self.start_state: str = 'S'
        self.accept_states: set = {'X'}

    def accepts(self, input_str: str) -> bool:
        current_state: str = self.start_state
        for symbol in input_str:
            next_state: any = None
            for transition in self.transitions:
                if transition[0] == current_state and transition[1] == symbol:
                    next_state = transition[2]
                    break
            if next_state is None:
                return False
            current_state = next_state
        return current_state in self.accept_states
