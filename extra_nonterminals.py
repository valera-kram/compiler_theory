#1 - удаление непродуктивных нетерминалов
#2 - удаление недостижимых нетерминалов

class ContextFreeGrammar:
    def __init__(self, **kwargs):
        self.terminal_symbols = kwargs['terminal_symbols']
        self.nonterminal_symbols = kwargs['nonterminal_symbols']
        self.start = kwargs['start']
        self.rules = kwargs['rules']

        self.removing_unproductive_nonterminals()
        self.removing_unreachable_nonterminals()
        self.removing_e_rules()

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


terminal_symbols = ['a', 'b', 'c']
nonterminal_symbols=['S', 'A']
start = 'S'
rules = {'S': ['Ab', 'e', 'a' ], 'A':['Ac', 'Sb', 'e']}

print('Our grammar:')
gr = ContextFreeGrammar(terminal_symbols=terminal_symbols, nonterminal_symbols=nonterminal_symbols, start=start, rules=rules)
print(gr.rules)