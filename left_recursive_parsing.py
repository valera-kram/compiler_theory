#Базовый алгоритм парсинга лево-рекурсивным спуском.
#Входные данные:
#grammar - грамматика, ПРИГОДНАЯ для парсинга лево-рекурсивным спуском, и слово.
#Выходные данные:
#Дерево вывода этого слова. Дерево пустое, если слово не пренадлежит грамматике.

class Grammar:
    def __init__(self, **kwargs):
        self.nonterminals = kwargs['nonterminals']
        self.alphabet = kwargs['alphabet']
        self.rules = kwargs['rules']
        self.start = kwargs['start']

#Функция для нахождения дерева вывода 
def getLeftParsing(grammar, word):
    tree = {}

    result = leftRecursiveParsing(grammar, [word, 0], grammar.start, tree)
    if result:
        return tree
    else:
        return {}


#Вспомогательная функция, которая осуществляет лево-рекурсивный парсинг
#pair - список, состоящий из слова и индекса, который указывает на проверяемый символ
def leftRecursiveParsing(grammar, pair, NoTerm, tree):
    listRules = grammar.rules[NoTerm]
    saveIndex = pair[1]
    checkedCharacters = 0
    badRules = 0
    tree[NoTerm] = []

    for rule in listRules:
        for symbol in rule:
            checkedCharacters += 1
            #возврат, если вышли за размер слова
            if pair[1] >= len(pair[0]):
                return False
            if symbol in grammar.nonterminals:  #текущий символ нетерминальный
                tree[NoTerm].append({})
                flag = leftRecursiveParsing(grammar, pair, symbol, tree[NoTerm][len(tree[NoTerm])-1])
                if flag == False:
                    return False
            else:
                # если символ в правиле терминальный и совпадает с символом в слове
                if symbol == pair[0][pair[1]]:
                    tree[NoTerm].append(symbol)
                    pair[1] += 1
                    if(checkedCharacters == len(rule)):
                        return True
                else:
                    # возвращаемся на начальную позицию проверки
                    pair[1] = saveIndex
                    checkedCharacters = 0
                    tree[NoTerm] = []
                    badRules += 1
                    break
    #ни одно правило не подошло
    if badRules == len(listRules):
        return False
    else:
        return True



grammar = Grammar(nonterminals=['S', 'A', 'B'], alphabet=['a', 'b', 'c', 'd', 'e'],
                  rules={'S': ['cbAa'], 'A': ['aBe', 'e'], 'B': ['dd', 'bd']}, start='S')
word = 'cbaddea'
tree = getLeftParsing(grammar, word)


if(len(tree) != 0):
    print("Дерево вывода:")
    print(tree)
else:
    print("Невозможно распознать данное слово этой грамматикой")
