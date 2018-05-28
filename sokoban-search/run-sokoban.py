from sokoban import *
import time
import sys
from multiprocessing import Process

# ______________________________________________________________________________
# Estatísticas e Função de execução


def statistics(resultado, caminho=False):
    """ Metodo concreto para imprimir dados da resolução de um problema Sokoban """
    try:
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

        for index, state in enumerate(path):
            if caminho:
                print(state, sep=" ", end="", flush=True)
        else:
            print("Número de passos:", index)

        print("Números de moves:", number_moves)
        print("Números de pushes:", number_pushes)

    except:
        print("\nNão existe solução/Parametros mal introduzidos")

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor



def execute(nome, algorithm, problema, heuristic=None):
    print("Execução do algoritmo:", nome)

    def wheel():
        spinner = spinning_cursor()
        while True:
            sys.stdout.write(spinner.__next__())
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

    if heuristic is not None:
        print("É só esperar...")
        t = Process(target=wheel)
        t.start()

        inicio = time.time()
        resultado = algorithm(problema, heuristic)
        fim = time.time()

        if (t.is_alive()):
            t.terminate()
        statistics(resultado, True)
    else:
        print("É só esperar...")
        t = Process(target=wheel)
        t.start()

        inicio = time.time()
        resultado = algorithm(problema)
        fim = time.time()

        if (t.is_alive()):
            t.terminate()
        statistics(resultado, True)

    tempo_execucao = fim - inicio

    ms = tempo_execucao % 1
    ms = ms * 1000
    m, s = divmod(tempo_execucao, 60)
    h, m = divmod(m, 60)

    print("Tempo de execução: %d:%02d:%02d:%03d " % (h, m, s, ms))


# ______________________________________________________________________________
# Carregar puzzles e correr algoritmos

puzzle = "puzzle3.txt"
puzzle_estado = import_sokoban_file("puzzles/" + puzzle)

sokoban = Sokoban(puzzle_estado)

execute("greedy - hungarian", greedy_best_first_graph_search, sokoban, hung_alg_manh)


# execute("astar - hungarian", astar_search, sokoban, hung_alg_manh)

# execute("greedy - hungarian + euclidean usher to target", greedy_best_first_graph_search, sokoban, hung_alg_manh_usher_to_target)

# execute("greedy - hungarian + euclidean usher to box", greedy_best_first_graph_search, sokoban, hung_alg_manh_usher_to_box)

# execute("greedy - euclidean usher to target", greedy_best_first_graph_search, sokoban, heur_euclidean_usher_target)
