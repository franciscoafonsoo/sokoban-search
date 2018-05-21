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
        self.deadlocks = self.deadlocks_tabuleiro()
 
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
 
commit:5c596d
Deteção de cantos, e de linhas "mortas".

E não permite que as caixas sejam empurradas para lá.