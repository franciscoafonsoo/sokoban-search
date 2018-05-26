from sokoban import *
import time

# ______________________________________________________________________________
# Puzzles para testes

puzzle1 = import_sokoban_file("puzzles/puzzle1.txt")
puzzle1_2 = import_sokoban_file("puzzles/puzzle1_2.txt")
puzzle2 = import_sokoban_file("puzzles/puzzle2.txt")
puzzle2_1 = import_sokoban_file("puzzles/puzzle2_1.txt")
puzzle3 = import_sokoban_file("puzzles/puzzle3.txt")
puzzle3_1 = import_sokoban_file("puzzles/puzzle3_1.txt")
puzzle3_2 = import_sokoban_file("puzzles/puzzle3_2.txt")
puzzle4 = import_sokoban_file("puzzles/puzzle4.txt")
puzzle5 = import_sokoban_file("puzzles/puzzle5.txt")


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
        statistics(resultado, False)
    else:
        inicio = time.time()
        resultado = algorithm(problema)
        fim = time.time()
        statistics(resultado, False)

    tempo_execucao = fim - inicio
    if tempo_execucao > 60:
        tempo_execucao = tempo_execucao / 60

    print("Tempo de execução:", "{0:.2f}".format(tempo_execucao))


sokoban = Sokoban(puzzle2)

execute("greedy - hungarian", greedy_best_first_graph_search, sokoban, hung_alg_manh)


# execute("astar - hungarian", astar_search, sokoban, hung_alg_manh)

# execute("greedy - hungarian + euclidean usher to target", greedy_best_first_graph_search, sokoban, hung_alg_manh_usher_to_target)

# execute("greedy - hungarian + euclidean usher to box", greedy_best_first_graph_search, sokoban, hung_alg_manh_usher_to_box)

# execute("greedy - euclidean usher to target", greedy_best_first_graph_search, sokoban, heur_euclidean_usher_target)
