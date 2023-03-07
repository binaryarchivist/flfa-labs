# Laboratory Work no.2 V.18

### Course: Formal Languages & Finite Automata

### Author: Corneliu Nastas

----

## Theory

0. The most important part of this laboratory work is to understand how grammar and finite automata works, also it is
   important to mention that both of them are closely related and work pretty much the same in one way or another.
1. Grammar: <br/>
   <b>VN</b> set of non-terminal symbols<br/>
   <b>VT</b> set of terminal symbols<br/>
   <b>P</b> set of production rules<br/>
   In my case it is a <b>type 3 grammar</b>
   <br/>
    <hr/>
According to Noam Chomosky, there are four types of grammars − Type 0, Type 1, Type 2, and Type 3.
Type 0 - unrestricted grammar. Type 1 - we cannot convert to an empty string. Type 2 - converts from non terminal to a string of non terminal and terminals. Type 3 grammars must have a single non-terminal on the left-hand side and a right-hand side consisting of a single terminal or single terminal followed by a single non-terminal.
2. A finite automaton is a mathematical model that describes a system that can transition through a finite set of states
   based on a sequence of input symbols. It is a type of automaton, which is a self-operating machine or computational
   device that performs a sequence of predetermined actions based on a set of inputs.

<br/>


## Objectives:
1. Understand what an automaton is and what it can be used for.

2. Continuing the work in the same repository and the same project, the following need to be added:
    a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.

    b. For this you can use the variant from the previous lab.

3. According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

    a. Implement conversion of a finite automaton to a regular grammar.

    b. Determine whether your FA is deterministic or non-deterministic.

    c. Implement some functionality that would convert an NDFA to a DFA.
    
    d. Represent the finite automaton graphically (Optional, and can be considered as a __*bonus point*__):
      
    - You can use external libraries, tools or APIs to generate the figures/diagrams.
        
    - Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.
   

## Implementation description

* Input format:

```python
    # main.py
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
```

* Converting FA to grammar:
```python
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
```

* Converting NFA to DFA

```python
"""finite_automaton.py"""
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
        self.states = new_states
        self.delta = delta

    def get_transitions(self, state) -> List[Transition]:
        delta: List = []
        for temp_state in state:
            for curr_state, char, next_state in self.delta:
                if curr_state == temp_state:
                    delta.append([state, char, next_state])
        return delta

```

After processing the transition for the first state we add it to the visited states and remove it from current states.
After that we check if any potential transitions from temp2 will result in new states that wasn't visited, if it wasn't visited
it is added to current_states.

* Visually representing graphs

```python
    """finite_automaton.py"""
    def graph(self) -> None:
        G = nx.DiGraph()
        for state in self.Q:
            G.add_node(state)

        for current_state, char, next_state in self.delta:
            if next_state != 'X':
              G.add_edge(current_state, next_state, weight=char)
            
        graph = nx.circular_layout(G)
        nx.draw(G, graph, with_labels = True)
        nx.draw_networkx_edge_labels(G, graph)
        plt.show()
```

## Conclusions / Screenshots / Results

[nfa](media/nfa.png)
[dfa](media/dfa.png)


* Conclusion:
During this laboratory work I've managed to impemented NFA to DFA conversion method and I've found myself fixing lots of bugs while doing so, most likely because of the wrong data structure chosen. Other than that I've also implemented a checker to see if an automaton is non-deterministic and a method to represent an automaton graphically which also took quite some time finding the right resources and it still is a bit buggy.

   
