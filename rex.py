# E используется для пустого слова
# 0 используется для обозначения операции, которой нет (проще говоря для листа дерева)

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

def createStringFromTree(tree):
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

reg_expr = ReX() 
summary = ''
print('Empty expression: ', reg_expr)

reg_expr2 = ReX(token='a')
summary = ''
print('Expression with one token: ', reg_expr2)

reg_expr3 = ReX(operation='*', expressions=[reg_expr2])
summary = ''
print("Expression with '*':", reg_expr3)

reg_expr4 = ReX(operation='|', expressions=[ReX(token='a'), ReX(token='b')])
summary = ''
print('Expression with alternation: ', reg_expr4)

reg_expr5 = ReX(operation=',', expressions=[reg_expr4, ReX(token='c')])
summary = ''
print('Expression with alternation and concatenation: ', reg_expr5)

reg_expr6 = ReX(operation='*', expressions=[reg_expr5])
summary = ''
print("Expression with alternation, concatenation and '*': ", reg_expr6)

#Incorrect cases
ReX(operaion='*')
ReX(operation='*', expresssions=[ReX(token='a'), ReX(token='b')])
ReX(operation='|', expresssions=[ReX(token='a')])