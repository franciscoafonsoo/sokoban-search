from sokoban import *
import time

def timing(f):

    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print("tempo de execucao", "{0:.2f}".format(time2 - time1))
        return ret

    return wrap


def statistics(resultado, verbose=False):
    """
    Metodo concreto para imprimir dados da resolução de um problema Sokoban

    TODO - try except quando path e solution não existem
    """
    path = resultado.path()
    solucao = resultado.solution()
    number_moves = 0
    number_pushes = 0

    for index, action in enumerate(solucao):
        accao, _ = action.split()
        if accao == "andar":
            number_moves += 1
        else:
            number_pushes += 1

    count = 0
    for index, state in enumerate(path):
        count += 1
        if verbose:
            print(state, end="\r")
    else:
        print("Número de passos:", index)

    print("Números de moves:", number_moves)
    print("Números de pushes:", number_pushes)


def execute(nome, algorithm, problema, heuristic=None):
    print("Execução do algoritmo:", nome)
    if heuristic is not None:
        inicio = time.time()
        resultado = algorithm(problema, heuristic)
        fim = time.time()
        statistics(resultado, True)
    else:
        inicio = time.time()
        resultado = algorithm(problema)
        fim = time.time()
        statistics(resultado, True)

    tempo_execucao = fim - inicio

    m, s = divmod(tempo_execucao, 60)
    h, m = divmod(m, 60)

    print("Tempo de execução: %d:%02d:%02d" % (h, m, s))


puzzle = "puzzle2.txt"
puzzle_estado = import_sokoban_file("puzzles/" + puzzle)

sokoban = Sokoban(puzzle_estado)

execute("greedy - hungarian", greedy_best_first_graph_search, sokoban, hung_alg_manh)


# execute("astar - hungarian", astar_search, sokoban, hung_alg_manh)

# execute("greedy - hungarian + euclidean usher to target", greedy_best_first_graph_search, sokoban, hung_alg_manh_usher_to_target)

# execute("greedy - hungarian + euclidean usher to box", greedy_best_first_graph_search, sokoban, hung_alg_manh_usher_to_box)

# execute("greedy - euclidean usher to target", greedy_best_first_graph_search, sokoban, heur_euclidean_usher_target)
