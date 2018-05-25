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

sokoban = Sokoban(puzzle3)

def statistics(resultado, verbose=False):
    '''Metodo concreto para imprimir dados da resolução de um problema Sokoban'''

    # TODO - try except quando path e solution não existem
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
    count = 0
    for index, state in enumerate(path):
        count += 1
        if verbose:
            #time.sleep(0.1)
            print(state, end='\r')

            #print("ola " + str(count) + "\n", end="\r")
    else:
        print('Número de passos:', index)

    print('Números de moves:', number_moves)
    print('Números de pushes:', number_pushes)


#bfs_resultado = breadth_first_search(sokoban)
#ucs_resultado = uniform_cost_search(sokoban)
#astar_resultado = astar_search(sokoban, hung_alg_manh)

#statistics(astar_resultado, True)

inicio = time.time()
astar_resultado = greedy_best_first_graph_search(sokoban, hung_alg_manh)
fim = time.time()
statistics(astar_resultado, True)

print("Tempo de execução", '{0:.2f}'.format(fim-inicio))
#statistics(bfs_resultado)
#statistics(ucs_resultado)