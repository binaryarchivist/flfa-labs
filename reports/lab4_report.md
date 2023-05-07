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

Step 1: Identify all non-terminal symbols that can derive epsilon.


In order to do this we simply iterate over non terminal symbols and add the symbol which contains epsilon transition.

```python
def eliminate_epsilon(self):
    eps_symbols = set()
    for symbol in self.vn:
        if 'ε' in self.p[symbol]:
            eps_symbols.add(symbol)
```
Step 2: Generate new productions without eps symbols.


To achieve this we first of all initialize new productions rules as a dictionary

 `new_prods = dict(self.p)`
Then we iterate through all the symbols and associated production rules in `self.p` and in the innermost loop we check whether a nullable symbol is part of the current production rule


a. `if eps_symbol in prod` If a nullable symbol is found in the production rule,


 i. `new_prod = prod.replace(eps_symbol, 'ε')`: Create a new production rule by replacing the nullable symbol with 'ε' (the empty string symbol).


 ii. `if new_prod not in new_prods[symbol]`: Check if the new production rule is not already in the updated rules for the current symbol.


1. `new_prods[symbol].append(new_prod)`: If it's not, append the new production rule to the list of updated rules for the current symbol.


2. `no_new_prod = False`: Set the flag no_new_prod to False to indicate that a new production rule has been added.

```python
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
```

Step 3: Add new productions to handle eps symbol usage in other rules.

Now we have to further process the `new_prods` dictionary.

1. `for symbol, productions in new_prods.items()` This loop iterates over the key-value pairs (symbols and their production rules) in new_prods.
2. `new_prods[symbol] += [production for production in self.p[symbol] if all([eps_symbol not in production for eps_symbol in eps_symbols])]`:
 This line updates the production rules for the current symbol by adding all the original production rules from self.p that do not contain any nullable symbols (eps_symbols). It does this using a list comprehension with a condition that checks if no nullable symbols are present in the production.
3. `for eps_symbol in eps_symbols`: This loop iterates over the nullable symbols.
4. `if eps_symbol in new_prods[symbol]` Inside the loop, it checks if the current nullable symbol is present in the production rules of the current symbol.
5. If the nullable symbol is found, the following operations are performed:<br/>
a. `new_prods[symbol].remove(eps_symbol)`: Remove the nullable symbol from the production rules of the current symbol. <br/>
b. `new_prods[symbol] += [production for production in new_prods[eps_symbol] if production not in new_prods[symbol]]`: Add all production rules associated with the current nullable symbol to the production rules of the current symbol, only if those rules are not already present in the current symbol's production rules. This is done using a list comprehension with a condition that checks if the production is not already in the current symbol's production rules.
6. `new_prods[symbol] = list(set(new_prods[symbol]))`: Finally, remove duplicates from the production rules of the current symbol by converting the list to a set and then back to a list.

```python
for symbol, productions in new_prods.items():
    new_prods[symbol] += [production for production in self.p[symbol]
                            if all([eps_symbol not in production for eps_symbol in eps_symbols])]
    for eps_symbol in eps_symbols:
        if eps_symbol in new_prods[symbol]:
            new_prods[symbol].remove(eps_symbol)
            new_prods[symbol] += [production for production in new_prods[eps_symbol]
                                    if production not in new_prods[symbol]]
    new_prods[symbol] = list(set(new_prods[symbol]))
```
Step 4: Remove epsilon productions.

In the following snippet we simply iterate over symbols and its productions rules and remove the epsilon character.

```python
for symbol, productions in new_prods.items():
    if 'ε' in productions:
        new_prods[symbol].remove('ε')
    new_vals = []
    for prod in productions:
        t = prod.replace('ε', '')
        new_vals.append(t)
    new_prods[symbol] = new_vals
```
Step 5: Remove redundant productions.

In order to avoid duplicate productions we make it a set and assign the new production rules.
```python
for symbol, productions in new_prods.items():
    new_prods[symbol] = list(set(productions))

self.p = new_prods
```

Result:
```
# S ['aB', 'B', 'b', 'bA']
# A ['bAB', 'b', 'S', 'aD', 'AS', 'bB']
# B ['bS', 'a']
# C ['AB', 'B']
# D ['BB']
```

Method `eliminate_renaming` refers to removing rules that have only a single non-terminal on the right-hand side. These rules are also known as "unit rules" or "unit productions." The purpose of this step is to simplify the grammar and make it comply with the CNF rules:


Step 1: Create a dictionary of all renaming productions
```python
renaming_dict = {}
for var in self.vn:
    renaming_dict[var] = [var]
```
Step2: Update production rules for each non terminal symbol until there were made changes.

1. `for var in self.vn` Iterate through non terminal symbols 
2. `new_renaming = []` Initialize an empty list to store the updated production rules for the current non-terminal symbol
3. `for prod in self.p[var]` Iterates through production rules of current non terminal symbol
4. `if len(prod) == 1 and prod[0] in self.vn` Check if current production rule is a renaming.
5. `new_renaming.extend(renaming_dict[prod[0]])` Instead of adding the renaming itself, extend `new_renaming`  with the production rules of the non-terminal symbol on the right-hand side of the renaming.
6. `new_renaming.append(prod)` If it isn't a renaming add it without any modifications.
7. After processing all production rules for the current non-terminal symbol we check if the updated production rules in `new_renaming` are different from original and thus make necessary changes.

```python
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
```

Step3: Remove all renaming productions
1. Iterate through non terminal symbols
2. Initialize a `new_productions` list
3. Check if a production is a renaming skip it.
4. After all the processing update the current production rules.
```python
for var in self.vn:
    new_productions = []
    for prod in self.p[var]:
        if len(prod) == 1 and prod[0] in self.vn:
            continue  # skip renaming productions
        else:
            new_productions.append(prod)
    self.p[var] = new_productions
```
Result:
```
# S ['bA', 'aB', 'b']
# A ['AS', 'b', 'aD', 'bAB', 'bB']
# B ['a', 'bS']
# C ['AB']
# D ['BB']
```


Method `eliminate_inaccessible` refers to the process of removing all non-terminal symbols and associated production rules that cannot be reached from the start symbol. 

```python
accessible = set([self.start_symbol])
```
Step 1: 
`accessible = set([self.start_symbol])` Marks the start symbol as accessible


Step 2: Find all accessible nonterminal symbols
In this snippet we basically iterate through the production rules and check for each its symbol and if its symbol is in non terminal symbols then it is accessible.
```python
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
```
Step 3: Remove inaccessible productions and symbols
```python
        self.p = {nt: [p for p in prod if all(
            s in accessible or s in self.vt for s in p)] for nt, prod in self.p.items() if nt in accessible}
        self.vn = accessible
```
Summary:


This code snippet is used to eliminate any nonterminal symbols that are not accessible from the start symbol. Firstly, the start symbol is marked as accessible, and then all nonterminal symbols that are accessible from the start symbol are identified using a loop. In each iteration of the loop, all nonterminal symbols that have productions containing only accessible nonterminal and terminal symbols are added to the set of accessible nonterminal symbols. This process continues until no new nonterminal symbols are added to the set. Finally, the productions that contain only accessible symbols are kept, and the inaccessible nonterminal symbols are removed. This ensures that the grammar only contains symbols that can be derived from the start symbol.


Result:

```
S ['aB', 'bA', 'b']
A ['b', 'AS', 'aD', 'bAB', 'bB']
B ['bS', 'a']
D ['BB']
```

Method `eliminate_non_productive_rules` refers to the process of removing non-productive non-terminal symbols and their associated production rules.

Step 1: Find productive symbols

Iterate through all non-terminal symbols and their production rules, If a non-terminal symbol has a production rule that contains only terminal symbols or symbols already in the `productive_symbols` set, we add the non-terminal symbol to the `productive_symbols` set.
```python
def eliminate_non_productive_rules(self):
    # find productive symbols
    productive = set()
    for symbol in self.vn:
        for production in self.p[symbol]:
            if all([s in productive.union(self.vt) for s in production]):
                productive.add(symbol)
                break
```

Step 2: Removing non-productive productions

Iterate through production rules and initialize each time a `new_productions` list
Check if symbol is in the `productive` set defined earlier iterate for each production and
`if all([s in productive.union(self.vt) for s in production])` check if all symbols in the current production rule are either in the `productive` set or in the terminal symbols set, if its true add it to `new_productions` and after processing all production rules for the current non-terminal symbol add the non-terminal symbol and its updated production rules to the `new_P` dictionary and update the production rules and non terminal symbols accordingly.

```python
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
Summary:


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

## Conclusion:
During this laboratory work I've managed to understand more deeply how to convert CFG to CNF and its necessary steps and writing this all down in code took more significant time since there are lots of caveats that are pretty annoying to deal with.

## References:
[1] [Chomsky Normal Form Wiki](https://en.wikipedia.org/wiki/Chomsky_normal_form)
 