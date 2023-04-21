from math import inf as infinity
from random import choice
import platform
import time
from os import system

"""
An implementation of Minimax AI Algorithm in Tic Tac Toe, using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)
"""

HUMANO = -1
COMPUTADOR = +1
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def evaluate(estado):
    """
    Función de evaluación del estado de finalización del juego.
     : parametro: estado, estado actual del tablero
     : devuelve: +1 si COMPUTADOR gana; -1 si el HUMANO gana; 0 en caso de empate
    """
    if wins(estado, COMPUTADOR):
        score = +1
    elif wins(estado, HUMANO):
        score = -1
    else:
        score = 0

    return score

def wins(estado, player):
    """Compara celda por celda"""
    count = 0
    for i in range(3):
        if estado[i][0] == estado[i][1] == player:
            count += 1
        if estado[i][1] == estado[i][2] == player:
            count += 1
        if estado[0][i] == estado[1][i] == player:
            count += 1
        if estado[1][i] == estado[2][i] == player:
            count += 1
    return count


def empty_cells(estado):
    """
    Cada celda vacía se agregará a la lista de celdas
    :parametro estado, estado de tablero actual
    :devuelve, una lista de las celdas vacias
    """
    cells = []

    for x, fila in enumerate(estado):
        for y, cell in enumerate(fila):
            if cell == 0:
                cells.append([x, y])
    return cells

def valid_move(x, y):
    """
    Un movimiento es válido si la celda elegida está vacía
    :parametro x, coordenada X
    :parametro y, coordenada Y
    :devuelve: True si la posicion del tablero[x][y] esta vacia
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

def set_move(x, y, player):
    """
    Establece un movimiento en el tablero, si las coordenadas son validas
    :parametro x, coordenada X
    :parametro y, coordenada Y
    :parametro player, jugador actual
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(estado, depth, player):
    """
    Funcion IA que elige la mejor movida
    AI function that choice the best move
    :parametro estado, estado actual en el tablero
    :param depth, indice del nodo en el arbol (0 <= depth < 9), pero nunca nueve.
    :param player, un HUMANO o un COMPUTADOR
    :devuelve, una lista con [la mejor fila, la mejor columna, el mejor score]
    """
    if player == COMPUTADOR:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 1:
        score = evaluate(estado)
        return [-1, -1, score]

    for cell in empty_cells(estado):
        x, y = cell[0], cell[1]
        estado[x][y] = player
        score = minimax(estado, depth - 1, -player)
        estado[x][y] = 0
        score[0], score[1] = x, y

        if player == COMPUTADOR:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(estado, c_choice, h_choice):
    """
    Print the board on console
    :param estado: current estado of the board
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for fila in estado:
        for cell in fila:
            symbol = chars[cell]
            print(f'| {symbol} |', end = '')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    """
    Esta funcion llama a la funcion minimax si la profundidad es < 9,
    caso contrario esta elige una coordenada aleatoria.
    :param c_choice: COMPUTADOR elije X o O
    :param h_choice: HUMANO elije X o O
    :return:
    """
    depth = len(empty_cells(board))
    """Cambiar el valor de depth, esto tambien para que quede
    un espacio en blanco"""
    if depth == 0:
        return

    clean()
    print(f'Juega COMPUTADOR [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMPUTADOR)
        x, y = move[0], move[1]

    set_move(x, y, COMPUTADOR)
    time.sleep(1)

def HUMANO_turn(c_choice, h_choice):
    """
    El HUMANO juega eligiendo una movida valida.
    :param c_choice: COMPUTADORuter's choice X or O
    :param h_choice: HUMANO's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0:
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'turno HUMANO [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use los numeros (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMANO)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    """
    Main function that calls all functions
    """
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if HUMANO is the first

    # HUMANO chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting COMPUTADORuter's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # HUMANO may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    #Para que quede una celda vacia cambiamos el valor comparado conlas celdas vacias
    while len(empty_cells(board)) > 1:
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        HUMANO_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)
    # Game over message
    countH = wins(board, HUMANO)
    countC = wins(board, COMPUTADOR)
    if countH > countC:
        clean()
        print(f'HUMANO turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print(f'HUMANO [{h_choice}] = ', countH)
        print(f'COMPUTADORA [{c_choice}] = ', countC)
        print('YOU WIN!')
    elif countC > countH:
        clean()
        print(f'COMPUTADOR turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print(f'HUMANO [{h_choice}] = ', countH)
        print(f'COMPUTADORA [{c_choice}] = ', countC)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print(f'HUMANO [{h_choice}] = ', countH)
        print(f'COMPUTADORA [{c_choice}] = ', countC)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
