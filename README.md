# sokoban-search
Problem Solving for the Sokoban game using search algorithms from aima-python.

## Notas sobre implementação

#### initial

Dicionário com: 

- 'board': lista de listas que representa o puzzle:
  - Cada um das listas interiores vão ter os seguintes caracters:    
    - ’#’   – para representar as paredes; 
    -  ’.’   – para representar as posições livres;
    - ’\*’   – para representar as caixas;
    - ’o’   – (um ó minúsculo) para representar os alvos;
    - ’A’   – para representar o arrumador.
    -  ’@’   – para representar uma caixa numa posição alvo.
    - ’B’   – para representar o arrumador em cima de uma posição alvo.
  - 'A': tuplo com posição do arrumador 
  - '\*': tuplo com posição das caixas
  - 'o': tuplo com posição dos alvos

#### goal

a ideia será tentar encontrar um '@', sem nunca encontrar '0' ou '*'.



## aima-python

https://github.com/aimacode/aima-python

## Resorces about Sokoban

http://www.abelmartin.com/rj/sokobanJS/sokoban.html