# Парсинг лево-рекурсивным спуском с помощью FIRST и FOLLOWS
# На вход поступает грамматика, ПРИГОДНАЯ для парсинга лево-рекурсивным спуском.

class Grammar:
    def __init__(self, **kwargs):
        self.nonterminals = kwargs['nonterminals']
        self.alphabet = kwargs['alphabet']
        self.rules = kwargs['rules']
        self.start = kwargs['start']


# Построение функции FIRST для данного символа
def getFIRST(grammar, noNerm, result):
    listRules = grammar.rules[noNerm]
    for rule in listRules:
        if rule[0] in grammar.alphabet:
            if rule[0] in result:
                continue
            else:
                result.append(rule[0])
        else:
            getFIRST(grammar, rule[0], result)


# Построение для данной строки функции FIRST
def FIRST(grammar, input_str):
    resultList = []
    if len(input_str) == 0:
        return resultList
    if input_str[0] in grammar.alphabet:
        resultList.append(input_str[0])
    else:
        getFIRST(grammar, input_str[0], resultList)
    return resultList

# Построение для данного нетерминала функции FOLLOW
def FOLLOW(grammar, noNerm):
    resList = []
    for key in grammar.nonterminals:
        for rule in grammar.rules[key]:
            # для каждого нетерминала и правила, в правой части которого стоит данный нетерминал,
            # ищем первый терминал, который следует за данным нетерминалом
            if noNerm in list(rule):
                resList.extend(FIRST(grammar, rule[(rule.index(noNerm)+1):]))
    return list(set(resList))


# Построение дерева вывода для данного слова и грамматики
def getLeftParsing(grammar, word):
    tree = {}

    result = parsingFIRSTandFOLLOW(grammar, [word, 0], grammar.start, tree, 0)
    if result == 1:
        return tree
    else:
        return {}


# Рекурсивная проверка принадлежности слова данной граматике.
# Если принаджежит, то построение дерева вывода.
# pair - пара, стостоящая из слова и числа-индекса, которое указывает на проверяемый символ
# check - шаг разбора
def parsingFIRSTandFOLLOW(grammar, pair, noTerm, tree, check):
    tree[noTerm] = []
    count = 0

    for rule in grammar.rules[noTerm]:
        if pair[1] >= len(pair[0]):
            return 0
        if pair[0][pair[1]] in FIRST(grammar, rule):
            count += 1
            for symbol in rule:
                if symbol in grammar.alphabet:
                    # проверяемый символ совпадает с терминалом в правиле
                    if symbol == pair[0][pair[1]]:
                        tree[noTerm].append(pair[0][pair[1]])
                        pair[1] += 1
                    else:
                        return 0
                else:  # символ в правиле -  нетерминал
                    tree[noTerm].append(symbol)

                    res = parsingFIRSTandFOLLOW(
                        grammar, pair, symbol, tree, check+1)
                    if res == 0:
                        return 0
                    # если символ не находится в множестве FIRST данного нетерминала, возвращаем ошибку
                    if pair[0][pair[1]] not in FOLLOW(grammar, symbol):
                        return 0
    if count == 0:
        return 0  # ни один символ не подошёл
    if (check == 0) and (pair[1] != len(pair[0])):
        return 0
    return 1


grammar = Grammar(nonterminals=['S', 'A', 'B'], alphabet=['a', 'b', 'c', 'd', 'e'],
                  rules={'S': ['cbAa'], 'A': ['aBe', 'e'], 'B': ['dd', 'bd']}, start='S')
word = 'cbaddea'
tree = getLeftParsing(grammar, word)

if(len(tree) != 0):
    print("Дерево вывода:")
    print(tree)
else:
    print("Невозможно распознать данное слово этой грамматикой")