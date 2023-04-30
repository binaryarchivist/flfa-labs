import random
from typing import List, Tuple
import pprint


# p = {
#     'S': ['aB', 'bA', 'B'],
#     'A': ['b', 'aD', 'AS', 'bAB', 'ε'],
#     'B': ['a', 'bS'],
#     'C': ['AB'],
#     'D': ['BB']
# }

class Grammar:
    def __init__(self, vn, vt, p, start_symbol) -> None:
        self.vn = vn
        self.vt = vt
        self.p = p
        self.start_symbol = start_symbol

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

    def eliminate_renaming(self):
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

    def eliminate_inaccessible(self):
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

    def eliminate_non_productive_rules(self):
            return 't'


    def is_terminal(self, string: str) -> bool:
        return string in self.vt

    def is_non_terminal(self, string: str) -> bool:
        return string in self.vn

    def get_rule(self, index: int) -> str:
        return self.p[index][1] + self.p[index][2]
