# coding=utf-8
from search import *


class Sokoban(Problem):
    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""

        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


def import_sokoban_file(filename):
    """
    2.3 Leitura de puzzle de ficheiro

    - Le o ficheiro linha a linha, e converte cada linha para uma lista de chars
    - Remove newline char
    - Verifica se cada linha tem o mesmo comprimento

    :return: matrix com as linhas lidas do ficheiro
    """
    matrix = list()
    with open(filename) as file:
        for line in file:
            matrix.append(list(line.rstrip('\n')))

    len_first = len(matrix[0])
    return matrix if all(len(i) == len_first for i in matrix) else False


# importar os 3 ficheiros e testar
puzzle1 = import_sokoban_file('puzzles/puzzle1.txt')
puzzle2 = import_sokoban_file('puzzles/puzzle2.txt')
puzzle3 = import_sokoban_file('puzzles/puzzle3.txt')

Sokoban(puzzle1)
