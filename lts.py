#E используется для обозначение спонтанного перехода, используется вместо токена в тройке

#в примере реализована МСП из лекции(з четным числом вхождений а)

import copy

class LTS:
    def __init__(self, **kwargs):
        self.tokens = kwargs['tokens']
        self.states = kwargs['states']
        self.start = kwargs['start']
        self.finish = kwargs['finish']
        self.transitions = kwargs['transitions']

    def getTokens(self):
        return set(self.tokens)

    def getStates(self):
        return set(self.states)

    def accept(self, c):
        W = []
#замыкаем множество W
        closed_states = closure(self, ['start'])
        closed_states.remove('start')
        for state in closed_states:
            W.append((state, 0))

        index = 0
        while len(W)!=0:    
            x = W[0]
            W.remove(x)

            if x[1] == len(c):
                for pair in W:
                    if pair[0] == 'finish' and pair[1] == len(c):
                        return True
#формируем мн-во состояний, на которое расширим наше W                  
            second_states = []
            for transition in self.transitions:
                if x[1] >= len(c): return False
                if transition[0] == x[0] and transition[1] == c[x[1]]:
                    second_states.append(transition[2])
#расширяем W
            for state in second_states:
                W.append((state, x[1]+1))
#замыкаем W
            closed_states = copy.copy(W)
            for pair in W:
                tmp_closed_dict = closure(self, [pair[0]])
                if len(tmp_closed_dict) > 1:
                    for i in range(1, len(tmp_closed_dict)):
                        closed_states.append((tmp_closed_dict[i], pair[1]))
            W = closed_states
        return False
    

#функция для замыкания множества
def closure(lts, input_states):
    transitions = copy.copy(lts.transitions)

    if len(input_states) == 0:
        return input_states
    res_states = input_states
    tmp_states = []
    while(res_states != tmp_states):
        tmp_states = res_states
        second_states = []
        for transition in transitions:
            if transition[1] == 'E' and transition[0] in tmp_states:
                second_states.append(transition[2])
                transitions.remove(transition)
        res_states = tmp_states + second_states
    return res_states

#мн-во переходов системы
T = [('start', 'E', 'even'), ('even', 'a', 'odd'), ('odd', 'a', 'even'), ('even', 'b', 'even'), ('odd', 'b', 'odd'), ('even', 'E', 'finish')]
lts1 = LTS(tokens=('a','b'), states=('start', 'even', 'odd', 'finish'), start='start', finish='finish', transitions=T)

#TRUE
print(lts1.accept('aab'))
print(lts1.accept('aaaa'))
print(lts1.accept('abababa'))

#FALSE
print(lts1.accept('aaa'))
print(lts1.accept('ababba'))