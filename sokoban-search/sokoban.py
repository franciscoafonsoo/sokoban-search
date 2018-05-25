# coding=utf-8
from copy import deepcopy
from utils_main import *
from search import *
import math

# ficheiro para execução do algoritmo hungáro
from hungarian import Munkres

"""
Implementação do puzzle Sokoban.

Conceitos gerais:

- Deadlock: Um estado do jogo Sokoban em que o problema deixa de ter solução
- Posição: Tuplo com dois valores para representar o espaço cartesiano.
"""

# ______________________________________________________________________________
# Definição de um estado do Problema


class EstadoSokoban:
    """
    Classe para para definir um estado do puzzle Sokoban.
    Os métodos auxiliares vão sendo explicados ao longo do código.

    Atributos:
        - Alvos     : Lista com as posições dos alvos.
        - Caixas    : Lista com as posições das caixas.
        - Tabuleiro : Lista de listas com todos os elementos do puzzle.
        - Arrumador : Posição do Arrumador

    Tabuleiro:
        - Cada um das listas interiores vão ter os seguintes caracters:
        – ’#’   – para representar as paredes;
        – ’.’   – para representar as posições livres;
        – ’*’   – para representar as caixas;
        – ’o’   – (um ó minúsculo) para representar os alvos;
        – ’A’   – para representar o arrumador.
        – ’@’   – para representar uma caixa numa posição alvo.
        – ’B’   – para representar o arrumador em cima de uma posição alvo.
    """

    def __init__(self, tabuleiro=None, arrumador=None, caixas=None, alvos=None):
        self.alvos = list() if alvos is None else alvos
        self.caixas = list() if caixas is None else caixas
        self.tabuleiro = list() if tabuleiro is None else tabuleiro
        self.arrumador = tuple() if arrumador is None else arrumador

    def pos_livre(self, x, y):
        """
        Verifica se uma posição do tabuleiro está livre.

        :param x: Coordenada x
        :param y: Coordenada y
        :return: bool
        """
        try:
            return self.tabuleiro[x][y] == FREE or self.tabuleiro[x][y] == TARGET
        except IndexError:
            return False

    def pos_caixa(self, x, y):
        """
        Verifica se uma posição do tabuleiro é um caixa.

        :param x: Coordenada x
        :param y: Coordenada y
        :return: bool
        """
        try:
            return self.tabuleiro[x][y] == BOX or self.tabuleiro[x][y] == BOX_ON_TARGET
        except IndexError:
            return False

    # _______________________________________
    # Verificações de acções

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
        """
        Representação em str do atributo tabuleiro. Útil para visualizar os vários estados

        :return: str
        """
        represent = ''
        for line in self.tabuleiro:
            for char in line:
                if char == USHER:
                    represent += USHER_EDIT
                elif char == FREE:
                    represent += ' '  
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
        """
        Definir em que circunstância os dois estados são considerados iguais.
        Necessário para os algoritmos de procura em grafo.
        """
        return self.tabuleiro == estado.tabuleiro

    def __hash__(self):
        """Necessário para os algoritmos de procura em grafo."""
        return hash((line for line in self.tabuleiro))

# ______________________________________________________________________________
# Implementação do Problema


# noinspection PyAbstractClass
class Sokoban(Problem):
    def __init__(self, initial):
        """
        2.1 Formulação

        :param initial: estado inicial do puzzle do tipo EstadoSokoban()
        """

        super().__init__(initial)
        self.estado_inicial = initial
        self.tabuleiro_inicial = initial.tabuleiro
        self.deadlocks = self.deadlocks_tabuleiro()

    # _______________________________________
    # Detecção de Deadlocks simples

    def pos_deadlock_canto(self, x, y):
        try:
            # canto superior esquerdo
            if self.tabuleiro_inicial[x - 1][y] == WALL and \
                    self.tabuleiro_inicial[x][y - 1] == WALL and \
                    self.tabuleiro_inicial[x - 1][y - 1] == WALL:
                return True

            # canto superior direito
            if self.tabuleiro_inicial[x - 1][y] == WALL and \
                    self.tabuleiro_inicial[x][y + 1] == WALL \
                    and self.tabuleiro_inicial[x - 1][y + 1] == WALL:
                return True

            # canto inferior esquerdo
            if self.tabuleiro_inicial[x + 1][y] == WALL and \
                    self.tabuleiro_inicial[x][y - 1] == WALL and \
                    self.tabuleiro_inicial[x + 1][y - 1] == WALL:
                return True

            # canto inferior direito
            if self.tabuleiro_inicial[x + 1][y] == WALL and \
                    self.tabuleiro_inicial[x][y + 1] == WALL and \
                    self.tabuleiro_inicial[x + 1][y - 1] == WALL:
                return True
        except IndexError:
            return False

    def deadlock_parede(self, deadlocks_cantos):
        try:
            auxiliar = list()
            auxiliar_boolean = list()
            deadlocks_paredes = list()

            for canto1 in deadlocks_cantos:
                for canto2 in deadlocks_cantos:
                    if canto1 != canto2:
                        canto1_x = canto1[0]
                        canto1_y = canto1[1]

                        canto2_x = canto2[0]
                        canto2_y = canto2[1]

                        if canto1_x == canto2_x:
                            auxiliar = list()
                            auxiliar_boolean = list()
                            for i in range(canto1_y, canto2_y):

                                if self.tabuleiro_inicial[canto1_x + 1][i] == WALL and \
                                        self.tabuleiro_inicial[canto1_x][i] != WALL:
                                    auxiliar.append((canto1_x, i))
                                    auxiliar_boolean.append(True)

                                elif self.tabuleiro_inicial[canto1_x - 1][i] == WALL and \
                                        self.tabuleiro_inicial[canto1_x][i] != WALL:
                                    auxiliar.append((canto1_x, i))
                                    auxiliar_boolean.append(True)

                                else:
                                    auxiliar_boolean.append(False)

                        elif canto1_y == canto2_y:

                            auxiliar = list()
                            auxiliar_boolean = list()

                            for i in range(canto1_x, canto2_x):
                                if self.tabuleiro_inicial[i][canto1_y + 1] == WALL and \
                                        self.tabuleiro_inicial[i][canto1_y] != WALL:
                                    auxiliar.append((i, canto1_y))
                                    auxiliar_boolean.append(True)

                                elif self.tabuleiro_inicial[i][canto1_y - 1] == WALL and \
                                        self.tabuleiro_inicial[i][canto1_y] != WALL:
                                    auxiliar.append((i, canto1_y))
                                    auxiliar_boolean.append(True)

                                else:
                                    auxiliar_boolean.append(False)

                    if False not in auxiliar_boolean:
                        for i in auxiliar:
                            deadlocks_paredes.append(i)
            return deadlocks_paredes
        except IndexError:
            return False

    def em_cruzamento_com_alvo(self, x, y):
        try:
            for i in self.estado_inicial.alvos:
                if i[0] == x or i[1] == y:
                    return True
        except IndexError:
            return False

    def deadlocks_tabuleiro(self):

        deadlocks = list()
        for i, lista in enumerate(self.tabuleiro_inicial):
            for j in range(0, len(lista)):

                if self.pos_deadlock_canto(i, j) and (i, j) not in self.estado_inicial.alvos and \
                        self.tabuleiro_inicial[i][j] != WALL:

                    if (i, j) not in deadlocks:
                        deadlocks.append((i, j))

        deadlocks_paredes = self.deadlock_parede(deadlocks)

        if not deadlocks_paredes:
            for i in deadlocks_paredes:
                if i not in deadlocks:
                    deadlocks.append(i)
        return deadlocks

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
        # posição do arrumador e da caixa no fim da acção
        new_x_usher, new_y_usher, new_x_box, new_y_box = 0, 0, 0, 0

        # variaveis necessarias para determinar o resultado de uma acção
        alvos = state.alvos
        caixas = deepcopy(state.caixas)
        tabuleiro = deepcopy(state.tabuleiro)
        arrumador = state.arrumador
        x, y = arrumador

        if action is not None:
            accao, direcao = action.split()
        else:
            return state

        # determinar em que direcção é que vamos mover o arrumador (e caixa)
        if direcao == DOWN:
            new_x_usher = x + 1
            new_y_usher = y
        elif direcao == UP:
            new_x_usher = x - 1
            new_y_usher = y
        elif direcao == RIGHT:
            new_x_usher = x
            new_y_usher = y + 1
        elif direcao == LEFT:
            new_x_usher = x
            new_y_usher = y - 1

        if accao == PUSH:
            if direcao == DOWN:
                new_x_box = x + 2
                new_y_box = y
            elif direcao == UP:
                new_x_box = x - 2
                new_y_box = y
            elif direcao == RIGHT:
                new_x_box = x
                new_y_box = y + 2
            elif direcao == LEFT:
                new_x_box = x
                new_y_box = y - 2

        # verificar deadlocks antes de executar a accao EMPURRAR
        if (new_x_box, new_y_box) not in self.deadlocks:
            if accao == PUSH:
                if state.caixas_alvos(new_x_box, new_y_box):
                    tabuleiro[new_x_box][new_y_box] = BOX_ON_TARGET
                else:
                    tabuleiro[new_x_box][new_y_box] = BOX
                caixas.remove((new_x_usher, new_y_usher))
                caixas.append((new_x_box, new_y_box))

            # ANDAR (SE FOR TARGET, USHER_ON_TARGET)
            if tabuleiro[new_x_usher][new_y_usher] == TARGET:
                tabuleiro[new_x_usher][new_y_usher] = USHER_ON_TARGET
            else:
                tabuleiro[new_x_usher][new_y_usher] = USHER
            arrumador = (new_x_usher, new_y_usher)

            # SE ARRUMADOR SAIR DO TARGET, INSERIR TARGET OUTRA VEZ
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
            if state.tabuleiro[x][y] is not BOX_ON_TARGET:
                return False
        return True

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        accao, direcao = action.split()
        if accao == WALK:
            return c + 1
        elif accao == PUSH:
            return c + 1

# ______________________________________________________________________________
# Heuristicas


def heur_euclidean_usher_target(nodo):
    """
    Distância euclidiana do arrumador ao alvo mais próximo dele
    :param nodo:
    :return:
    """
    cost = []
    arrumador = nodo.state.arrumador
    for i in nodo.state.alvos:
        cost.append(math.sqrt((i[0] - arrumador[0]) ** 2 + (i[1] - arrumador[1]) ** 2))
    return min(cost)


def heur_euclidean_usher_box(nodo):
    """
    Distância euclidiana do arrumador ao alvo mais próximo dele
    :param nodo:
    :return:
    """
    cost = []
    arrumador = nodo.state.arrumador
    for i in nodo.state.caixas:
        cost.append(math.sqrt((i[0] - arrumador[0]) ** 2 + (i[1] - arrumador[1]) ** 2))
    return min(cost)


def hung_alg_manh_usher_to_target(nodo):
    """
    Algoritmo hungaro, em que o custo de cada caixa a um alvo é a distância de manhattan.
    
    Explicação no relatório.
    """
    m = Munkres()
        
    caixas = nodo.state.caixas
    alvos = nodo.state.alvos
    custo = list()
    mhd = 0

    for index, c in enumerate(caixas):
        custo.append(list())
        for a in alvos:
            custo[index].append(abs(c[0] - a[0]) + abs(c[1] - a[1]))
    indexes = m.compute(custo)
    for row, column in indexes:
        value = custo[row][column]
        mhd += value
    return mhd + heur_euclidean_usher_target(nodo)


def hung_alg_manh_usher_to_box(nodo):
    """
    Algoritmo hungaro, em que o custo de cada caixa a um alvo é a distância de manhattan.

    Explicação no relatório.
    """
    m = Munkres()

    caixas = nodo.state.caixas
    alvos = nodo.state.alvos
    custo = list()
    mhd = 0

    for index, c in enumerate(caixas):
        custo.append(list())
        for a in alvos:
            custo[index].append(abs(c[0] - a[0]) + abs(c[1] - a[1]))
    indexes = m.compute(custo)
    for row, column in indexes:
        value = custo[row][column]
        mhd += value
    return mhd + heur_euclidean_usher_box(nodo)


def hung_alg_manh(nodo):
    """
    Algoritmo hungaro, em que o custo de cada caixa a um alvo é a distância de manhattan.

    Explicação no relatório.
    """
    m = Munkres()

    caixas = nodo.state.caixas
    alvos = nodo.state.alvos
    custo = list()
    mhd = 0

    for index, c in enumerate(caixas):
        custo.append(list())
        for a in alvos:
            custo[index].append(abs(c[0] - a[0]) + abs(c[1] - a[1]))
    indexes = m.compute(custo)
    for row, column in indexes:
        value = custo[row][column]
        mhd += value
    return mhd


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
