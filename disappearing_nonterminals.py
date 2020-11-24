#1 - удаление непродуктивных нетерминалов
#2 - удаление недостижимых нетерминалов
#3 - получение исчезающих нетерминалов

class ContextFreeGrammar:
    def __init__(self, **kwargs):
        self.terminal_symbols = kwargs['terminal_symbols']
        self.nonterminal_symbols = kwargs['nonterminal_symbols']
        self.start = kwargs['start']
        self.rules = kwargs['rules']

        self.removing_unproductive_nonterminals()
        self.removing_unreachable_nonterminals()
        # self.removing_e_rules()

#1 - удаление непродуктивных нетерминалов
    def removing_unproductive_nonterminals(self):
        keys = list(self.rules.keys())
        grammar = []
        tmp_grammar = []
        for nonterminal in keys:
            for el in self.rules[nonterminal]:
                if el[0].islower():
                    grammar.append(nonterminal)
                    break
        while grammar != tmp_grammar:
            tmp_grammar = grammar
            for nonterminal in keys:
                for el in self.rules[nonterminal]:
                    if el[0].islower() or el[0] in tmp_grammar:
                        grammar.append(nonterminal)
        for key in keys:
            if key not in grammar:
                self.rules.pop(key)
                self.nonterminal_symbols.remove(key)

#2 - удаление недостижимых нетерминалов            
    def removing_unreachable_nonterminals(self):
        keys = list(self.rules.keys())
        grammar = ['S']
        tmp_grammar = []
        while grammar != tmp_grammar:
            tmp_grammar = grammar
            for nonterminal in tmp_grammar:
                if nonterminal in keys:
                    for el in self.rules[nonterminal]:
                        for sym in list(el):
                            if sym.isupper() and sym not in grammar:
                                grammar.append(sym)
        for key in keys:
            if key not in grammar:
                self.rules.pop(key)
                self.nonterminal_symbols.remove(key)

    def removing_e_rules(self):
        keys = list(self.rules.keys())
        for key in keys:
            for el in self.rules[key]:
                if el == 'e':
                    self.rules[key].remove(el)

#3 - получение исчезающих нетерминалов
def get_disappearing_nonterminals(grammar):
    keys = list(grammar.rules.keys())
    vanishings = []
    for nonterminal in keys:
        for el in grammar.rules[nonterminal]:
            if el == 'e':
                vanishings.append(nonterminal)

    tmp_grammar = []
    while tmp_grammar != vanishings:
        tmp_grammar = vanishings
        for nonterminal in keys:
            for el in grammar.rules[nonterminal]:
                if el.isupper():
                    flag = True
                    for nonterminal_symbol in el.split():
                        if nonterminal_symbol not in vanishings:
                            flag = False
                            break
                    if flag:
                        vanishings.append(nonterminal)
    return vanishings




terminal_symbols = ['a', 'b', 'c']
nonterminal_symbols=['S', 'A']
start = 'S'
rules = { 'S': ['A', 'a' ], 'A':['Ac', 'Sb', 'e', 'B'], 'B':['Ac', 'b'] }

print('Our grammar:')
gr = ContextFreeGrammar(terminal_symbols=terminal_symbols, nonterminal_symbols=nonterminal_symbols, start=start, rules=rules)
print(gr.rules)

print('Disappearing nonterminals:')
print(get_disappearing_nonterminals(gr))
