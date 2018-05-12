# coding=utf-8
from search import *


class ProblemaTeoricas_1(Problem):
    grafo = {'I':{'A':2,'B':5},
             'A':{'C':2,'D':4,'I':2},
             'B':{'D':1,'F':5,'I':5},
             'C':{},
             'D':{'C':3,'F':2},
             'F':{}}

    def actions(self, estado):
        sucessores = self.grafo[estado].keys()  # métodos keys() devolve a lista das chaves do dicionário
        accoes = list(map(lambda x: "ir de {} para {}".format(estado, x), sucessores))
        return accoes

    def result(self, estado, accao):
        """Assume-se que uma acção é da forma 'ir de X para Y'
        """
        return accao.split()[-1]

    def path_cost(self, c, state1, action, state2):
        return c + self.grafo[state1][state2]

    def h1(self, no):
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        h = {'I': 7, 'A': 2, 'B': 3, 'C': 1, 'D': 5, 'F': 0}
        return h[no.state]

    def h2(self, no):
        """Uma heurística é uma função de um estado.
        Nesta implementação, é uma função do estado associado ao nó
        (objecto da classe Node) fornecido como argumento.
        """
        h = {'I': 7, 'A': 8, 'B': 11, 'C': 0, 'D': 5, 'F': 0}
        return h[no.state]


prob1 = ProblemaTeoricas_1('I','F')

res_astar = astar_search(prob1,prob1.h2)
print(res_astar.solution(),res_astar.path_cost)

# implementar h2