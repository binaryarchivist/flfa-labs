from typing import Tuple, List

Transition = Tuple[str, str, str]


class FiniteAutomaton:
    def __init__(self, vn: List[str], vt: List[str], tran: List[Transition]):
        self.transitions: List[Transition] = tran
        self.alphabet: List[str] = vt
        self.states: List[str] = vn
        self.start_state: str = 'S'
        self.accept_states: set = {'X'}

    def to_deterministic(self) -> None:
        current_states: List[str] = [self.start_state]
        transitions: List[Transition] = []
        new_states: List[str] = []
        while len(current_states) > 0:
            temp: List[Transition] = self.get_transitions(current_states[0])
            temp2: List = [[current_states[0], i, ''] for i in self.alphabet]
            for i in temp:
                for j in temp2:
                    if i[1] == j[1]:
                        j[2] = j[2] + i[2]
            new_states.append(current_states[0])
            current_states.pop(0)
            for i in temp2:
                if i[2] != '':
                    transitions.append(i)
                    if i[2] not in new_states:
                        current_states.append(i[2])
        self.states = new_states
        self.transitions = transitions

    def get_transitions(self, state) -> List[Transition]:
        transitions: List = []
        for j in state:
            for i in self.transitions:
                if i[0] == j:
                    transitions.append([state, i[1], i[2]])
            return transitions

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
