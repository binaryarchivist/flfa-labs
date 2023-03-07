from typing import Tuple, List
import networkx as nx
import matplotlib.pyplot as plt

Transition = Tuple[str, str, str]


class FiniteAutomaton:
    def __init__(self, Q: List[str], sigma: List[str], delta: List[Transition], start_state: str,
                 accept_states: str) -> None:
        self.delta: List[Transition] = delta
        self.sigma: List[str] = sigma
        self.Q: List[str] = Q
        self.start_state: str = start_state
        self.accept_states: str = accept_states

    # lab2 3.c
    def to_deterministic(self) -> None:
        current_states: List[str] = [self.start_state]
        delta: List[Transition] = []
        new_states: List[str] = []

        while len(current_states) > 0:
            temp: List[Transition] = self.get_transitions(current_states[0])
            temp2: List = [[current_states[0], i, ''] for i in self.sigma]
            for i in temp:
                for j in temp2:
                    if i[1] == j[1]:
                        j[2] = j[2] + i[2]
            new_states.append(current_states[0])
            current_states.pop(0)
            for i in temp2:
                if i[2] != '':
                    delta.append(i)
                    if i[2] not in new_states:
                        current_states.append(i[2])
                        if self.accept_states in i[2]:
                            self.accept_states = i[2]
        self.Q = new_states
        self.delta = delta

    def get_transitions(self, state) -> List[Transition]:
        delta: List = []
        for temp_state in state:
            for curr_state, char, next_state in self.delta:
                if curr_state == temp_state:
                    delta.append([state, char, next_state])
        return delta

    def accepts(self, input_str: str) -> bool:
        current_state: str = self.start_state
        for symbol in input_str:
            temp_state: any = None
            for curr_state, char, next_state in self.delta:
                if curr_state == current_state and char == symbol:
                    temp_state = next_state
                    break
            if temp_state is None:
                return False
            current_state = temp_state
        return current_state in self.accept_states

    # lab2 3.b
    def is_nfa(self) -> bool:
        for tran in self.delta:
            for t in self.delta:
                if (tran[0], tran[1]) == (t[0], t[1]) and self.delta.index(tran) != self.delta.index(t):
                    return True
        return False
    
    # lab2 3.d
    def graph(self) -> None:
        G = nx.DiGraph()

        for state in self.Q:
            G.add_node(state)
        
        print(self.delta)
        for current_state, char, next_state in self.delta:
            if next_state != 'X':
              G.add_edge(current_state, next_state, weight=char)
            
        graph = nx.circular_layout(G)
        nx.draw(G, graph, with_labels = True)
        nx.draw_networkx_edge_labels(G, graph)
        plt.show()

            