# Laboratory Work no.1 V.18

### Course: Formal Languages & Finite Automata
### Author: Corneliu Nastas

----

## Theory
0. The most important part of this laboratory work is to understand how grammar and finite automata works, also it is important to mention that both of them are closely related and work pretty much the same in one way or another.
1. Grammar: <br/>
    <b>VN</b> set of non-terminal symbols<br/>
    <b>VT</b> set of terminal symbols<br/>
    <b>P</b> set of production rules<br/>
    In my case it is a <b>type 3 right linear grammar</b>
    <br/>
    <hr/>
2. A finite automaton is a mathematical model that describes a system that can transition through a finite set of states based on a sequence of input symbols. It is a type of automaton, which is a self-operating machine or computational device that performs a sequence of predetermined actions based on a set of inputs.

<br/>
Because the way I've implemented Finite automaton it isn't necessary to do any conversion from Grammar, we can simply pass to the constructor the production rules and generate a Finite Automaton instance.


## Objectives:

1. Understand what a language is and what it needs to have in order to be considered a formal one.

2. Provide the initial setup for the evolving project that you will work on during this semester. I said project because usually at lab works, I encourage/impose students to treat all the labs like stages of development of a whole project. Basically you need to do the following:

    a. Create a local && remote repository of a VCS hosting service (let us all use Github to avoid unnecessary headaches);

    b. Choose a programming language, and my suggestion would be to choose one that supports all the main paradigms;

    c. Create a separate folder where you will be keeping the report. This semester I wish I won't see reports alongside source code files, fingers crossed;

3. According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:

    a. Implement a type/class for your grammar;

    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

    c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;
    
    d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;


   

## Implementation description

* Input format (grammar):
```python
    # main.py
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
```
* Input format (finite automation):
```python
    """ finite_automaton.py """
    # Finite automaton constructor
    def __init__(self, tran: List[Tuple[str, str, str]]):
        self.transitions: List[Tuple[str, str, str]] = tran
        self.start_state: str = 'S'
        self.accept_states: set = {'X'}
    
    # Grammar to_finite_automaton method
    def to_finite_automaton(self) -> FiniteAutomaton:
        return FiniteAutomaton(self._p)
```
Transitions can be accepted in the same form of the production rules then start_state  and accept_states is predefined.

* Generating strings:
```python
    """grammar.py"""
    def generate_string(self, string: str) -> str:
        flag: bool = True

        while flag:
            flag = False
            for i in range(len(string)):
                if self.is_non_terminal(string[i]):
                    choices: List[int] = self.get_indices(string[i])
                    rule_index: int = random.choice(choices)
                    r: str = self.get_rule(rule_index)

                    string = string[:i] + r + string[i + 1:]
                    flag = True

        return string[:-1]
```
This algorithm simply iterates through the string and if its a non terminal string gets possible next rules, gets one randomly and updates the string respectively. At the end we output the string except last character (terminal symbol 'X')

* Util functions used (Grammar):
```python
    """grammar.py"""
    # Here we get the indeces of possible choices
    def get_indices(self, string: str) -> List[int]:
        result: List[int] = []
        for tran in self._p:
            if string == tran[0]:
                result.append(self._p.index(tran))
        return result

    # Validation function
    def is_terminal(self, string: str) -> bool:
        return string in self._vt

    # Validation function
    def is_non_terminal(self, string: str) -> bool:
        return string in self._vn

    # Get the next terminal and non terminal character
    def get_rule(self, index: int) -> str:
        return self._p[index][1] + self._p[index][2]
```

* Converting to Finite Automaton:
```python
    """grammar.py"""
    def to_finite_automaton(self) -> FiniteAutomaton:
        return FiniteAutomaton(self._p)
```

* Checking if a string belongs to automaton
```python
    """finite_automaton.py"""

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
```
In this algorithm we iterate through each character in the string and check from possible transitions if there is any possible transition, important to mention that there's also an early break in case there isn't any transitions. If the last transition is 'X' which I've marked as last possible state then it should belong to the given rules.

## Conclusions / Screenshots / Results
* Test cases (all strings generated by the Grammar class should be valid):
```python
"""main.py"""
    gram: Grammar = Grammar(vn, vt, p)
    fa: FiniteAutomaton = gram.to_finite_automaton()

    print("Generated by grammar class: \n")
    for _ in range(1, 50):
        s = gram.generate_string("S")
        print("string: ", s, " fa:", fa.accepts(s))

    print("\n\nFalse cases: \n")
    false_cases: List[str] = ['ab', 'abbaaaa', 'aa', 'ababababababb', 'abaaaa', 'baaaaaaa']
    for s in false_cases:
        print(s, ':', fa.accepts(s))
```

* Results:
[Test case results](media/test_cases.png)

* Lab1 implementation commit: https://github.com/binaryarchivist/flfa-labs/tree/e1f0b7683eeb6f86418a63a87ba1f812b982f295

* Conclusion:
During this laboratory work I've implemented two classes Grammar and FiniteAutomaton. 
Grammar class generating a string according to the production rules and terminal/non-terminal symbols given to it.
To prove that they are generated correctly FiniteAutomaton is validating them, which proved successful. It was a learning experience to implement the functionality of these two, important to note that it might have been harder to implement a Non Deterministic Finite Automata because we would have to introduce epsilon transitions and some move functions...
