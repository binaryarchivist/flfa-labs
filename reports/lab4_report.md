# Topic: Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Corneliu Nastas

----

## Theory
CNF stands for Chomsky Normal Form, which is a way of representing a context-free grammar (CFG) in a specific form.

In CNF, every production rule has one of two forms:

either a single non-terminal symbol produces two non-terminal symbols,

or a single non-terminal symbol produces a single terminal symbol.

This form makes parsing easier and more efficient, which is why many algorithms and parsers rely on grammars being in CNF. Converting a CFG to CNF involves breaking down longer production rules into smaller ones that fit the required forms.


To convert a Context-Free Grammar (CFG) to Chomsky Normal Form (CNF), we need to follow a set of steps:

1. Remove all ε-productions from the grammar.
2. Remove all unit productions from the grammar.
3. Convert all remaining productions to have either two non-terminals or a non-terminal and a terminal on the right-hand side.
4. If a production has more than two non-terminals on the right-hand side, split it into multiple productions.

After performing these steps, the resulting grammar will be in CNF.



## Objectives:
1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.



## Implementation:
The Context Free Grammar given for Variant 18 is:
```
vn = {'S', 'A', 'B', 'C', 'D'}
vt = {'a', 'b'}
p = {
    'S': ['aB', 'bA', 'B'],
    'A': ['b', 'aD', 'AS', 'bAB', 'ε'],
    'B': ['a', 'bS'],
    'C': ['AB'],
    'D': ['BB']
}
```

The main method is `cfg_to_cnf`  as it implements all the other tasks all together.

Method `eliminate_epsilon` is used to eliminate epsilon transitions as it names suggests.


```python
    def eliminate_epsilon(self):
        # Step 1: Identify all non-terminal symbols that can derive epsilon
        eps_symbols = set()
        for symbol in self.vn:
            if 'ε' in self.p[symbol]:
                eps_symbols.add(symbol)

        # Step 2: Generate new productions without eps symbols
        new_prods = dict(self.p)
        while True:
            no_new_prod = True
            for symbol, prods in self.p.items():
                for prod in prods:
                    for eps_symbol in eps_symbols:
                        if eps_symbol in prod:
                            new_prod = prod.replace(eps_symbol, 'ε')
                            if new_prod not in new_prods[symbol]:
                                new_prods[symbol].append(new_prod)
                                no_new_prod = False
            if no_new_prod:
                break

        # Step 3: Add new productions to handle eps symbol usage in other rules
        for symbol, productions in new_prods.items():
            new_prods[symbol] += [production for production in self.p[symbol]
                                  if all([eps_symbol not in production for eps_symbol in eps_symbols])]
            for eps_symbol in eps_symbols:
                if eps_symbol in new_prods[symbol]:
                    new_prods[symbol].remove(eps_symbol)
                    new_prods[symbol] += [production for production in new_prods[eps_symbol]
                                          if production not in new_prods[symbol]]
            new_prods[symbol] = list(set(new_prods[symbol]))

        # Step 4: Remove epsilon productions
        for symbol, productions in new_prods.items():
            if 'ε' in productions:
                new_prods[symbol].remove('ε')
            new_vals = []
            for prod in productions:
                t = prod.replace('ε', '')
                new_vals.append(t)
            new_prods[symbol] = new_vals

        # Step 5: Remove redundant productions
        for symbol, productions in new_prods.items():
            new_prods[symbol] = list(set(productions))

        self.p = new_prods
```
It first identifies all non-terminal symbols that can derive the empty string (epsilon), generates new productions without epsilon symbols, adds new productions to handle epsilon symbol usage in other rules, removes epsilon productions, and removes redundant productions. The end result is a CNF grammar.

Result:
```
# S ['aB', 'B', 'b', 'bA']
# A ['bAB', 'b', 'S', 'aD', 'AS', 'bB']
# B ['bS', 'a']
# C ['AB', 'B']
# D ['BB']
```

Method `eliminate_renaming` is used at it name suggests for eliminating renamings:

```python
        # Create a dictionary of all renaming productions
        renaming_dict = {}
        for var in self.vn:
            renaming_dict[var] = [var]

        while True:
            updated = False
            for var in self.vn:
                new_renaming = []
                for prod in self.p[var]:
                    if len(prod) == 1 and prod[0] in self.vn:
                        new_renaming.extend(renaming_dict[prod[0]])
                    else:
                        new_renaming.append(prod)

                if set(new_renaming) != set(self.p[var]):
                    updated = True
                    self.p[var] = new_renaming

            if not updated:
                break

        # Remove all renaming productions
        for var in self.vn:
            new_productions = []
            for prod in self.p[var]:
                if len(prod) == 1 and prod[0] in self.vn:
                    continue  # skip renaming productions
                else:
                    new_productions.append(prod)
            self.p[var] = new_productions
```

It creates a dictionary of all the renaming productions and then iteratively removes them. It also updates the existing productions based on the renaming productions, until no further updates are possible. Finally, it removes all the renaming productions from the context-free grammar.

Result:
```
# S ['bA', 'aB', 'b']
# A ['AS', 'b', 'aD', 'bAB', 'bB']
# B ['a', 'bS']
# C ['AB']
# D ['BB']
```


Method `eliminate_inaccessible` is used at its name suggests for eliminating inaccessible symbols

```python
        # Mark the start symbol as accessible
        accessible = set([self.start_symbol])

        # Find all accessible nonterminal symbols
        while True:
            prev_accessible = set(accessible)
            for nt, prod in self.p.items():
                if nt in accessible:
                    for p in prod:
                        for symbol in p:
                            if symbol in self.vn:
                                accessible.add(symbol)
            if prev_accessible == accessible:
                break

        # Remove inaccessible productions and symbols
        self.p = {nt: [p for p in prod if all(
            s in accessible or s in self.vt for s in p)] for nt, prod in self.p.items() if nt in accessible}
        self.vn = accessible
```
This code snippet is used to eliminate any nonterminal symbols that are not accessible from the start symbol. Firstly, the start symbol is marked as accessible, and then all nonterminal symbols that are accessible from the start symbol are identified using a loop. In each iteration of the loop, all nonterminal symbols that have productions containing only accessible nonterminal and terminal symbols are added to the set of accessible nonterminal symbols. This process continues until no new nonterminal symbols are added to the set. Finally, the productions that contain only accessible symbols are kept, and the inaccessible nonterminal symbols are removed. This ensures that the grammar only contains symbols that can be derived from the start symbol.


Result:

```
S ['aB', 'bA', 'b']
A ['b', 'AS', 'aD', 'bAB', 'bB']
B ['bS', 'a']
D ['BB']
```

Method `eliminate_non_productive_rules` is used at its name suggests.
```python
    def eliminate_non_productive_rules(self):
        # find productive symbols
        productive = set()
        for symbol in self.vn:
            for production in self.p[symbol]:
                if all([s in productive.union(self.vt) for s in production]):
                    productive.add(symbol)
                    break

        # remove non-productive productions
        new_P = {}
        for symbol, productions in self.p.items():
            new_productions = []
            if symbol in productive:
                for production in productions:
                    if all([s in productive.union(self.vt) for s in production]):
                        new_productions.append(production)
                if new_productions:
                    new_P[symbol] = new_productions
            else:
                new_P[symbol] = []

        # update grammar
        self.p = new_P
        self.vn = productive
```

It removes all non-productive rules and symbols from the grammar.
It works as follows:

Marks the start symbol as productive.

Finds all productive nonterminal symbols.

Removes unproductive productions and symbols from the grammar.

Result:

```
S ['aB', 'bA', 'b']
A ['b', 'AS', 'aD', 'bAB', 'bB']
B ['bS', 'a']
D ['BB']
```



## References:
[1] [Chomsky Normal Form Wiki](https://en.wikipedia.org/wiki/Chomsky_normal_form)
 