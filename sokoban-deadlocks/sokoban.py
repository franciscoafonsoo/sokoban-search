# coding=utf-8
from utils_main import *
from search import *
from copy import deepcopy
import math


class EstadoSokoban:

    def __init__(self, tabuleiro=None, arrumador=None, caixas=None, alvos=None):
        self.alvos = list() if alvos is None else alvos
        self.caixas = list() if caixas is None else caixas
        self.tabuleiro = list() if tabuleiro is None else tabuleiro
        self.arrumador = tuple() if arrumador is None else arrumador
        #self.deadlocks = self.deadlocks_tabuleiro()

    def pos_deadlock_canto(self, x, y):
        try:

            # canto superior esquerdo
            if self.tabuleiro[x - 1][y] == WALL and self.tabuleiro[x][y - 1] == WALL and self.tabuleiro[x - 1][y - 1] == WALL:
                return True

            # canto superior direito
            if self.tabuleiro[x - 1][y] == WALL and self.tabuleiro[x][y + 1] == WALL and self.tabuleiro[x - 1][y + 1] == WALL:
                return True

            # canto inferior esquerdo
            if self.tabuleiro[x + 1][y] == WALL and self.tabuleiro[x][y - 1] == WALL and self.tabuleiro[x + 1][y - 1] == WALL:
                return True

            # canto inferior direito
            if self.tabuleiro[x + 1][y] == WALL and self.tabuleiro[x][y + 1] == WALL and self.tabuleiro[x + 1][y - 1] == WALL:
                return True
        except IndexError:
            return False

    def pos_deadlock_parede(self, x, y):
        try:
            # parede em cima
            if self.tabuleiro[x - 1][y] == WALL and self.tabuleiro[x - 1][y - 1] == WALL and self.tabuleiro[x - 1][y + 1] == WALL:
                return True

            # parede em baixo
            if self.tabuleiro[x + 1][y] == WALL and self.tabuleiro[x + 1][y - 1] == WALL and self.tabuleiro[x + 1][y + 1] == WALL:
                return True

            # parede à direita
            if self.tabuleiro[x][y + 1] == WALL and self.tabuleiro[x - 1][y + 1] == WALL and self.tabuleiro[x + 1][y + 1] == WALL:
                return True

            # parede à esquerda
            if self.tabuleiro[x][y - 1] == WALL and self.tabuleiro[x - 1][y - 1] == WALL and self.tabuleiro[x + 1][y - 1] == WALL:
                return True
        except IndexError:
            return False

    def em_cruzamento(self, x, y):
        try:
            for i in self.alvos:
                if i[0] == x or i[1] == y:
                    return True
        except IndexError:
            return False

    def deadlocks_tabuleiro(self):
        deadlocks = list()
        for i in range(0, len(self.tabuleiro)):
            for j in range(0, len(self.tabuleiro)):
                if self.pos_deadlock_canto(i, j) and (i, j) not in self.alvos and self.tabuleiro[i][j] != WALL:
                    if (i, j) not in deadlocks:
                        deadlocks.append((i, j))
                if self.pos_deadlock_parede(i, j) and not self.em_cruzamento(i, j) and self.tabuleiro[i][j] != WALL:
                    if (i, j) not in deadlocks:
                        deadlocks.append((i, j))
                pass
        #print(deadlocks)
        return deadlocks

    def pos_livre(self, x, y):
        try:
            return self.tabuleiro[x][y] == FREE or self.tabuleiro[x][y] == TARGET
        except IndexError:
            return False

    def pos_caixa(self, x, y):
        try:
            return self.tabuleiro[x][y] == BOX
        except IndexError:
            return False

    def ver_cima(self, x, y):
        if self.pos_livre(x - 1, y):
            return WALK_UP
        elif self.pos_caixa(x - 1, y):
            if self.pos_livre(x - 2, y):
                return PUSH_UP

    def ver_baixo(self, x, y):
        if self.pos_livre(x + 1, y):
            return WALK_DOWN
        elif self.pos_caixa(x + 1, y):
            if self.pos_livre(x + 2, y):
                return PUSH_DOWN

    def ver_esquerda(self, x, y):
        if self.pos_livre(x, y - 1):
            return WALK_LEFT
        elif self.pos_caixa(x, y - 1):
            if self.pos_livre(x, y - 2):
                return PUSH_LEFT

    def ver_direita(self, x, y):
        if self.pos_livre(x, y + 1):
            return WALK_RIGHT
        elif self.pos_caixa(x, y + 1):
            if self.pos_livre(x, y + 2):
                return PUSH_RIGHT

    def caixas_alvos(self, x, y):
        return (x, y) in self.alvos

    def __str__(self):
        represent = ''
        for line in self.tabuleiro:
            for char in line:
                if char == USHER:
                    represent += USHER_EDIT
                elif char == TARGET:
                    represent += TARGET_EDIT
                elif char == BOX:
                    represent += BOX_EDIT
                elif char == WALL:
                    represent += WALL_EDIT
                elif char == BOX_ON_TARGET:
                    represent += BOX_ON_TARGET_EDIT
                elif char == USHER_ON_TARGET:
                    represent += USHER_ON_TARGET_EDIT
                else:
                    represent += char
            represent += '\n'
        return represent

    def __gt__(self, estado):
        return self.tabuleiro < estado.tabuleiro

    def __eq__(self, estado):
        """Definir em que circunstância os dois estados são considerados iguais.
        Necessário para os algoritmos de procura em grafo.
        """
        return self.tabuleiro == estado.tabuleiro

    def __hash__(self):
        """Necessário para os algoritmos de procura em grafo."""
        return hash((line for line in self.tabuleiro))


# noinspection PyAbstractClass
class Sokoban(Problem):
    def __init__(self, initial):
        """
        2.1 Formulação

        Representação de um puzzle sokoban vai ser um dict em que:

        - 'board': lista de listas que representa o puzzle:
            - Cada um das listas interiores vão ter os seguintes caracters:
            – ’#’   – para representar as paredes;
            – ’.’   – para representar as posições livres;
            – ’*’   – para representar as caixas;
            – ’o’   – (um ó minúsculo) para representar os alvos;
            – ’A’   – para representar o arrumador.
            – ’@’   – para representar uma caixa numa posição alvo.
            – ’B’   – para representar o arrumador em cima de uma posição alvo.
        - 'A': posição do arrumador, tuplo xy.
        - '*': posição das caixas, tuplo xy.
        - 'o': posição dos alvos, tuplo xy.

        :param initial: dict descrito acima
        """

        super().__init__(initial)

    def actions(self, state):
        """
        comment behavior later
        :param state:
        :return:
        """

        x, y = state.arrumador
        accoes = list()

        if state.ver_baixo(x, y):
            accoes.append(state.ver_baixo(x, y))
        if state.ver_cima(x, y):
            accoes.append(state.ver_cima(x, y))
        if state.ver_direita(x, y):
            accoes.append(state.ver_direita(x, y))
        if state.ver_esquerda(x, y):
            accoes.append(state.ver_esquerda(x, y))

        return accoes

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        alvos = state.alvos
        caixas = deepcopy(state.caixas)
        tabuleiro = deepcopy(state.tabuleiro)
        arrumador = state.arrumador
        x, y = arrumador

        if action is not None:
            accao, direcao = action.split()
        else:
            return state

        if accao == WALK:
            if direcao == DOWN:

                tabuleiro[x + 1][y] = USHER
                arrumador = (x + 1, y)

            elif direcao == UP:

                tabuleiro[x - 1][y] = USHER
                arrumador = (x - 1, y)

            elif direcao == RIGHT:

                tabuleiro[x][y + 1] = USHER
                arrumador = (x, y + 1)

            elif direcao == LEFT:
                tabuleiro[x][y - 1] = USHER
                arrumador = (x, y - 1)

        elif accao == PUSH:

            if direcao == DOWN:

                tabuleiro[x + 1][y] = USHER
                arrumador = (x + 1, y)


                if state.caixas_alvos(x + 2, y):
                    tabuleiro[x + 2][y] = BOX_ON_TARGET
                else:
                    tabuleiro[x + 2][y] = BOX
                caixas.remove((x + 1, y))
                caixas.append((x + 2, y))

            elif direcao == UP:

                tabuleiro[x - 1][y] = USHER
                arrumador = (x - 1, y)
                if state.caixas_alvos(x - 2, y):
                    tabuleiro[x - 2][y] = BOX_ON_TARGET
                else:
                    tabuleiro[x - 2][y] = BOX
                caixas.remove((x - 1, y))
                caixas.append((x - 2, y))

            elif direcao == RIGHT:

                tabuleiro[x][y + 1] = USHER
                arrumador = (x, y + 1)
                if state.caixas_alvos(x, y + 2):
                    tabuleiro[x][y + 2] = BOX_ON_TARGET
                else:
                    tabuleiro[x][y + 2] = BOX
                caixas.remove((x, y + 1))
                caixas.append((x, y + 2))

            elif direcao == LEFT:

                tabuleiro[x][y - 1] = USHER
                arrumador = (x, y - 1)
                if state.caixas_alvos(x, y - 2):
                    tabuleiro[x][y - 2] = BOX_ON_TARGET
                else:
                    tabuleiro[x][y - 2] = BOX
                caixas.remove((x, y - 1))
                caixas.append((x, y - 2))

        if state.caixas_alvos(x, y):
            tabuleiro[x][y] = TARGET
        else:
            tabuleiro[x][y] = FREE

        return EstadoSokoban(tabuleiro, arrumador, caixas, alvos)

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        for x, y in state.alvos:
            if state.tabuleiro[x][y] == USHER:
                return True
            #if state.tabuleiro[x][y] is not BOX_ON_TARGET:
            #    return True
        return False

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        #print(state1)
        #print(state1.deadlocks)

        accao, direcao = action.split()
        if accao == WALK:
            return c + 0.2
        elif accao == PUSH:
            return c + 0.1

    def heur_euclidean_usher_target(self, no):
        """
        Distância euclidiana do arrumador ao alvo mais próximo dele
        :param no:
        :return:
        """
        cost = []
        arrumador = no.state.arrumador
        for i in no.state.alvos:
            cost.append(math.sqrt((i[0] - arrumador[0]) ** 2 + (i[1] - arrumador[1]) ** 2))
        return min(cost)


def import_sokoban_file(filename):
    """
    2.3 Leitura de puzzle de ficheiro

    - Le o ficheiro linha a linha, e converte cada linha para uma lista de chars
    - Procura arrumador, caixas e alvos para indexar a sua posição
    - Remove newline char
    - Verifica se cada linha tem o mesmo comprimento

    :return: dict com as linhas lidas do ficheiro + posições de arrumador, caixas e alvos
    """
    estado = EstadoSokoban()

    with open(filename) as file:
        for line in file:
            estado.tabuleiro.append(list(line.rstrip('\n')))

            for index, value in enumerate(line):
                if value is USHER:
                    estado.arrumador = (len(estado.tabuleiro) - 1, index)
                elif value is BOX:
                    estado.caixas.append((len(estado.tabuleiro) - 1, index))
                elif value is TARGET:
                    estado.alvos.append((len(estado.tabuleiro) - 1, index))
                elif value is BOX_ON_TARGET:
                    estado.caixas.append((len(estado.tabuleiro) - 1, index))
                    estado.alvos.append((len(estado.tabuleiro) - 1, index))
                elif value is USHER_ON_TARGET:
                    estado.arrumador = (len(estado.tabuleiro) - 1, index)
                    estado.alvos.append((len(estado.tabuleiro) - 1, index))

    len_first = len(estado.tabuleiro[0])
    return estado if all(len(i) == len_first for i in estado.tabuleiro) else False


# importar os 3 ficheiros e testar
puzzle1 = import_sokoban_file('puzzles/puzzle1.txt')
puzzle1_2 = import_sokoban_file('puzzles/puzzle1_2.txt')
puzzle2 = import_sokoban_file('puzzles/puzzle2.txt')
puzzle2_1 = import_sokoban_file('puzzles/puzzle2_1.txt')
puzzle3 = import_sokoban_file('puzzles/puzzle3.txt')

a = Sokoban(puzzle1)

resultado = uniform_cost_search(a)
print(resultado.state)

# res_gbfs = greedy_best_first_graph_search(a,a.heur_euclidean_usher_target)

# print(res_gbfs.solution(),res_gbfs.path_cost)

# print("resultado final\n" + str(res_gbfs.state))

# res_astar = astar_search(a,a.heur_euclidean_usher_target)

# print(res_astar.solution(),res_astar.path_cost)

# print(res_astar.state)