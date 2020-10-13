#стартовое состояние МСП -- 'start'
#финишное состояние МСП -- 'finish'
#спонтанный переход -- (stateA, 'E', stateB)

class ReX:
    def __init__(self, **kwargs):
        self.tree = {}

        if len(kwargs) == 0:
            self.tree[0] = 'E'
        elif 'token' in kwargs:
            self.tree[0] = kwargs['token']
        elif 'operation' in kwargs and 'expressions' in kwargs:
            if kwargs['operation'] == '*':
                if len(kwargs['expressions']) != 1:
                    print('Incorrect number of expressions')
                elif 0 in kwargs['expressions'][0].tree and kwargs['expressions'][0].tree[0] == 'E':
                    print("Incorrect operation '*' for E")
                else:
                    self.tree['*'] = kwargs['expressions'][0].tree
            elif kwargs['operation'] in ('|', ','):
                if len(kwargs['expressions']) != 2:
                    print('Incorrect number of expressions for ', kwargs['operation'])
                else:
                    self.tree[kwargs['operation']] = { 'left': kwargs['expressions'][0].tree, 'right': kwargs['expressions'][1].tree }
        else:
            print('Incorrect input data')
    
    def __str__(self):
        createStringFromTree(self.tree)
        return summary

def createStringFromTree(tree) -> str:
    global summary

    if 0 in tree:
        if tree[0] == 'E':
            summary += ''
        else:
            summary += tree[0]
    elif ',' in tree:
        summary += '('
        createStringFromTree(tree[',']['left'])
        summary += ','
        createStringFromTree(tree[',']['right'])
        summary += ')'
    elif '|' in tree:
        summary += '('
        createStringFromTree(tree['|']['left'])
        summary += '|'
        createStringFromTree(tree['|']['right'])
        summary += ')'
    elif '*' in tree:
        createStringFromTree(tree['*'])
        summary += '*'

class LTS:
    def __init__(self, **kwargs):
        self.tokens = kwargs['tokens']
        self.states = kwargs['states']
        self.start = kwargs['start']
        self.finish = kwargs['finish']
        self.transitions = kwargs['transitions']

#вспомогательная функция для построения МСП
def help_for_lts(**kwargs) -> LTS:
    #используется для получения уникального номера для построения нового состояния
    global counter

    operation = kwargs['operation']
    value = kwargs['value']
    
    #мы имеем лист дерева и создаем стартовую МСП 
    if operation == 'null':
        lts = LTS(tokens=[], states=['start', 'finish'], start='start', finish='finish', transitions=[])
        #МСП с 1 спонтанным переходом
        if value[0] == 'E':
            lts.transitions.append(('start', 'E', 'finish'))
        #МСП с 1 переходом и токеном
        else:
            lts.tokens.append(value[0])
            lts.transitions.append(('start', value[0], 'finish'))
        return lts
    elif operation == '*':
        if 0 in value:
            temp_lts = help_for_lts(operation='null', value=value)
        else:
            next_operation = list(value.keys())[0]
            temp_lts = help_for_lts(operation=next_operation, value=value[next_operation])
            
        #имея МСП на предыдущем шаге, строим МСП для операции *
        old_start = ('state'+ str(counter))
        counter+=1
        old_finish = ('state'+ str(counter))
        counter+=1

        temp_lts.states+= [old_start, old_finish]

        new_transitions = []
        for el in temp_lts.transitions:
            if el[0] == 'start' and el[2] == 'finish':
                new_transitions.append((old_start, el[1], old_finish))
            elif el[0] == 'start':
                new_transitions.append((old_start, el[1], el[2]))
            elif el[2] == 'finish':
                new_transitions.append((el[0], el[1], old_finish))
            else:
                new_transitions.append((el[0], el[1], el[2]))

        new_transitions.append(('start', 'E', old_start))
        new_transitions.append((old_finish, 'E', 'finish'))
        new_transitions.append((old_start, 'E', old_finish))
        new_transitions.append((old_finish, 'E', old_start))

        temp_lts.transitions = new_transitions
        return temp_lts
    elif operation in ['|', ',']:
        if 0 in value['left']:
            left_lts = help_for_lts(operation='null', value=value['left'])
        else:
            next_operation = list(value['left'].keys())[0]
            left_lts = help_for_lts(operation=next_operation, value=value['left'][next_operation])
        if 0 in value['right']:
            right_lts = help_for_lts(operation='null', value=value['right'])
        else:
            next_operation = list(value['right'].keys())[0]
            right_lts = help_for_lts(operation=next_operation, value=value['right'][next_operation])
        
        #имея МСП на предыдущем шаге, строим МСП для операции ,
        if operation == ',':
            old_left_finish = ('state'+ str(counter))
            counter+=1
            old_right_start = ('state'+ str(counter))
            counter+=1

            left_lts.states += [old_left_finish, old_right_start]
            left_lts.states += right_lts.states
            left_lts.states.remove('start')
            left_lts.states.remove('finish')

            left_lts.tokens += right_lts.tokens

            new_transitions = []
            for el in left_lts.transitions:
                if el[2] == 'finish':
                    new_transitions.append((el[0], el[1], old_left_finish))
                else:
                    new_transitions.append((el[0], el[1], el[2]))
            for el in right_lts.transitions:
                if el[0] == 'start':
                    new_transitions.append((old_right_start, el[1], el[2]))
                else:
                    new_transitions.append((el[2], el[1], el[2]))
            
            new_transitions.append((old_left_finish, 'E', old_right_start))
            left_lts.transitions = new_transitions

            return left_lts

        #имея МСП на предыдущем шаге, строим МСП для операции |
        elif operation == '|':
            old_left_start = ('state'+ str(counter))
            counter+=1
            old_left_finish = ('state'+ str(counter))
            counter+=1
            old_right_start = ('state'+ str(counter))
            counter+=1
            old_right_finish = ('state'+ str(counter))
            counter+=1

            left_lts.states += [old_left_start, old_left_finish, old_right_start, old_right_finish]
            left_lts.states += right_lts.states
            
            left_lts.states.remove('start')
            left_lts.states.remove('finish')

            left_lts.tokens += right_lts.tokens

            new_transitions = []
            for el in left_lts.transitions:
                if el[0] == 'start' and el[2] == 'finish':
                    new_transitions.append((old_left_start, el[1], old_left_finish))
                elif el[0] == 'start':
                    new_transitions.append((old_left_start, el[1], el[2]))
                elif el[2] == 'finish':
                    new_transitions.append((el[0], el[1], old_left_finish))
                else:
                    new_transitions.append((el[0], el[1], el[2]))
            for el in right_lts.transitions:
                if el[0] == 'start' and el[2] == 'finish':
                    new_transitions.append((old_right_start, el[1], old_right_finish))
                elif el[0] == 'start':
                    new_transitions.append((old_right_start, el[1], el[2]))
                elif el[2] == 'finish':
                    new_transitions.append((el[0], el[1], old_right_finish))
                else:
                    new_transitions.append((el[0], el[1], el[2]))
            
            new_transitions.append(('start', 'E', old_left_start))
            new_transitions.append(('start', 'E', old_right_start))
            new_transitions.append((old_left_finish, 'E', 'finish'))
            new_transitions.append((old_right_finish, 'E', 'finish'))

            left_lts.transitions = new_transitions

            return left_lts


#основная функция для построения МСП из объекта ReX
def ReX2LTS(rex) -> LTS:
    if 0 in rex.tree: 
        return help_for_lts(operation='null', value=rex.tree)
    else:
        next_operation = list(rex.tree.keys())[0]
        return help_for_lts(operation=next_operation, value=rex.tree[next_operation])


counter = 0
summary = ''
rex = ReX(token='a') 
print('Expr: ', rex)
lts = ReX2LTS(rex)
print(lts.transitions)

summary = ''
counter = 0
rex2 = ReX(operation='|',  expressions=[ReX(token='a'), ReX(token='b')])
print('Expr: ', rex2)
lts = ReX2LTS(rex2)
print(lts.transitions)

summary = ''
counter = 0
rex3 = ReX(operation=',', expressions=[rex2, ReX(token='c')])
print('Expr: ', rex3)
lts = ReX2LTS(rex3)
print(lts.transitions)

summary = ''
counter = 0
rex4 = ReX(operation='*', expressions=[rex3])
print('Expr: ', rex4)
lts = ReX2LTS(rex4)
print(lts.transitions)