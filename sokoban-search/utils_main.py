# coding=utf-8

"""
#####################################
#
#	COLORS & FORMATTING
#
#####################################
"""
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

"""
#####################################
#
#	CONSTANTS
#
#####################################
"""
#Ações
WALK_UP = 'andar cima'
PUSH_UP = 'empurrar cima'
WALK_DOWN = 'andar baixo'
PUSH_DOWN = 'empurrar baixo'
WALK_LEFT = 'andar esquerda'
PUSH_LEFT = 'empurrar esquerda'
WALK_RIGHT = 'andar direita'
PUSH_RIGHT = 'empurrar direita'
WALK = 'andar'
PUSH = 'empurrar'
UP = "cima"
DOWN = "baixo"
LEFT = "esquerda"
RIGHT = "direita"

#Caracteres - board

WALL = "#"
FREE = "."
BOX = "*"
TARGET = "o"
USHER = "A"
BOX_ON_TARGET = "@"
USHER_ON_TARGET = "B"
