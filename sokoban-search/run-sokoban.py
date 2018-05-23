from sokoban import *
import time

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('tempo de execucao', '{0:.2f}'.format(time2-time1))
        return ret
    return wrap


sokoban = Sokoban(puzzle2)

@timing
def statistics(resultado, verbose=False):
    '''Metodo concreto para imprimir dados da resolução de um problema Sokoban'''
    path = resultado.path()
    solucao = resultado.solution()
    number_moves = 0
    number_pushes = 0

    for index, action in enumerate(solucao):
        accao, _ = action.split()
        if accao == 'andar':
            number_moves += 1
        else:
            number_pushes += 1

    for index, state in enumerate(path):
        if verbose:
            print(state)
    else:
        print('Número de passos:', index)

    print('Números de moves:', number_moves)
    print('Números de pushes:', number_pushes)


bfs_resultado = breadth_first_search(sokoban)
ucs_resultado = uniform_cost_search(sokoban)
astar_resultado = astar_search(sokoban, hung_alg_manh)

statistics(astar_resultado, True)
statistics(bfs_resultado)
statistics(ucs_resultado)