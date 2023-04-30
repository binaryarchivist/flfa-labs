import pprint
from grammar_impl import Grammar


'''
V18
1) Eliminate epsilon productions
2) Eliminate any renaming
3) Eliminate inaccessible symbols
4) Eliminate non-productive symbols
5) Obtain Chomsky Normal Form
---
G = { V_n, V_t, P, S }
V_n = { S, A, B, C, D }
V_t = { a, b }
P = {
1. S -> aB
2. S -> bA
3. S -> B
4. A -> b
5. A -> aD
6. A -> AS
7. A -> bAB
8. A -> ε
9. B -> a
10. B -> bS
11. C -> AB
12. D -> BB
}
'''

vn = {'S', 'A', 'B', 'C', 'D'}
vt = {'a', 'b'}
p = {
    'S': ['aB', 'bA', 'B'],
    'A': ['b', 'aD', 'AS', 'bAB', 'ε'],
    'B': ['a', 'bS'],
    'C': ['AB'],
    'D': ['BB']
}
start_symbol = 'S'

grammar = Grammar(vn, vt, p, start_symbol)
for k,v in grammar.p.items():
    print(k,v)
print('---')
grammar.eliminate_epsilon()
# S ['aB', 'B', 'b', 'bA']
# A ['bAB', 'b', 'S', 'aD', 'AS', 'bB']
# B ['bS', 'a']
# C ['AB', 'B']
# D ['BB']
for k,v in grammar.p.items():
    print(k,v)
print('---')
grammar.eliminate_renaming()
# S ['bA', 'aB', 'b']
# A ['AS', 'b', 'aD', 'bAB', 'bB']
# B ['a', 'bS']
# C ['AB']
# D ['BB']

for k,v in grammar.p.items():
    print(k,v)
print('---')

# grammar.eliminate_inaccessible()
# for k,v in grammar.p.items():
#     print(k,v)
# print('---')



grammar.eliminate_non_productive_rules()
print(grammar.vn)

