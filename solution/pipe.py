
# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 02:
# 99044 Adrian Graur
# 99131 Vasco Roda Félix

import sys
import random
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    grid = [] # Lista de listas de strings
    locked = [] 
    connections = []

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.grid[row][col]
        

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        result = ()
        
        
        if(len(self.grid) - 1 == row):          #last row case
            result += (self.grid[row-1][col],)
            result += (None,)

        elif(row == 0):                         #first row case
            result += (None,)
            result += (self.grid[row+1][col],)

        else:
            result += (self.grid[row-1][col],)
            result += (self.grid[row+1][col],)

        return result

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        result = ()
        
        if(col == 0):
            result += (None,)
            result += (self.grid[row][col+1],)
        
        elif(len(self.grid[row]) - 1 == col):     
            result += (self.grid[row][col-1],)
            result += (None,)

        else:
            result += (self.grid[row][col-1],)
            result += (self.grid[row][col+1],)

        return result


    def getConections(self, row: int, col: int) -> int:
        """Devolve o número de conexões da peça na posição (row, col)."""
        return self.connections[row][col]

    
    def isLocked(self, row: int, col: int) -> bool:
        """Devolve True se a peça na posição (row, col) estiver bloqueada."""
        return self.locked[row][col]
    
    
    
    def updateLocks(self, row: int, col: int):
        """Atualiza o estado de bloqueio das peças adjacentes apoós o bloqueio da peça na posição (row, col)."""
        
        if row == 0 and col == 0:
            if self.grid[row][col] == "VB":
                if self.grid[row+1][col] in ["FC", "VD"]:
                    self.locked[row+1][col] = True
                if self.grid[row][col+1] in ["FE", "VE"]:
                    self.locked[row][col+1] = True
            
            elif self.grid[row][col] == "FD":
                if self.grid[row][col+1] == "VE":
                    self.locked[row][col+1] = True
                    
            elif self.grid[row][col] == "FB":
                if self.grid[row+1][col] == "VD":
                    self.locked[row+1][col] = True
        
        elif row == 0 and col == len(self.grid[row]) - 1:
            if self.grid[row][col] == "VE":
                if self.grid[row+1][col] in ["FC", "VC"]:
                    self.locked[row+1][col] = True
                if self.grid[row][col-1] in ["FD", "VB"]:
                    self.locked[row][col-1] = True
            
            elif self.grid[row][col] == "FE":
                if self.grid[row][col-1] == "VB":
                    self.locked[row][col-1] = True
            
            elif self.grid[row][col] == "FB":
                if self.grid[row+1][col] == "VC":
                    self.locked[row+1][col] = True
        
        elif row == len(self.grid) - 1 and col == 0:
            if self.grid[row][col] == "VD":
                if self.grid[row-1][col] in ["FB", "VB"]:
                    self.locked[row-1][col] = True
                if self.grid[row][col+1] in ["FE", "VC"]:
                    self.locked[row][col+1] = True
            
            elif self.grid[row][col] == "FC":
                if self.grid[row-1][col] == "VB":
                    self.locked[row-1][col] = True
            
            elif self.grid[row][col] == "FD":
                if self.grid[row][col+1] == "VC":
                    self.locked[row][col+1] = True
        
        elif row == len(self.grid) - 1 and col == len(self.grid[row]) - 1:
            if self.grid[row][col] == "VC":
                if self.grid[row-1][col] in ["FB", "VE"]:
                    self.locked[row-1][col] = True
                if self.grid[row][col-1] in ["FD", "VD"]:
                    self.locked[row][col-1] = True

            elif self.grid[row][col] == "FE":
                if self.grid[row][col-1] in ["LH", "VD"]:
                    self.locked[row][col-1] = True
            
            elif self.grid[row][col] == "FC":
                if self.grid[row-1][col] in  ["VE", "LV"]:
                    self.locked[row-1][col] = True
        
        elif row == 0 and col != 0 and col != len(self.grid[row]) - 1:
            if self.grid[row][col] == "LH":
                if self.grid[row][col-1] in ["FD", "BB", "VB"]:
                    self.locked[row][col-1] = True
                if self.grid[row][col+1] in ["FE", "BB", "VE"]:
                    self.locked[row][col+1] = True
            elif self.grid[row][col] == "BB":
                if self.grid[row][col-1] in ["FD", "VB", "BB"]:
                    self.locked[row][col-1] = True
                if self.grid[row][col+1] in ["FE", "BB", "VE"]:
                    self.locked[row][col+1] = True
                if self.grid[row+1][col] == "LV" and row+1 != len(self.grid) - 1:
                    self.locked[row+1][col] = True
                elif self.grid[row-1][col] == "FB":
                    self.locked[row-1][col] = True
            elif self.grid[row][col] == "VB":
                if self.grid[row+1][col] == "LV" and row+1 != len(self.grid) - 1:
                    self.locked[row+1][col] = True
                elif self.grid[row+1][col] == "FB":
                    self.locked[row+1][col] = True
                if self.grid[row][col+1] in ["FE", "BB", "VE"]:
                    self.locked[row][col+1] = True
            elif self.grid[row][col] == "VE":
                if self.grid[row][col-1] in ["FD", "BB", "VB"]:
                    self.locked[row][col-1] = True
                if self.grid[row+1][col] == "LV" and row+1 != len(self.grid) - 1:
                    self.locked[row+1][col] = True
                elif self.grid[row+1][col] == "FC":
                    self.locked[row+1][col] = True
        
        elif row == len(self.grid) - 1 and col != 0 and col != len(self.grid[row]) - 1:
            if self.grid[row][col] == "LH":
                if self.grid[row][col-1] in ["FD", "BC", "VD"]:
                    self.locked[row][col-1] = True
                if self.grid[row][col+1] in ["FE", "BC", "VC"]:
                    self.locked[row][col+1] = True
            elif self.grid[row][col] == "BC":
                if self.grid[row][col-1] in ["FD", "BC", "VD"]:
                    self.locked[row][col-1] = True
                    
                if self.grid[row][col+1] in ["FE", "BC", "VC"]:
                    self.locked[row][col+1] = True
                    
                if self.grid[row-1][col] == "LV" and row-1 != 0:
                    self.locked[row-1][col] = True
                elif self.grid[row-1][col] == "FB":
                    self.locked[row-1][col] = True
            elif self.grid[row][col] == "VC":
                if self.grid[row-1][col] == "LV" and row-1 != 0:
                    self.locked[row-1][col] = True
                elif self.grid[row-1][col] == "FB":
                    self.locked[row-1][col] = True
                if self.grid[row][col-1] in ["FD", "BC", "VD"]:
                    self.locked[row][col+1] = True
            elif self.grid[row][col] == "VD":
                if self.grid[row][col+1] in ["FE", "BE", "VC"]:
                    self.locked[row][col+1] = True
                if self.grid[row-1][col] == "LV" and row-1 != 0:
                    self.locked[row-1][col] = True
                elif self.grid[row-1][col] == "FB":
                    self.locked[row-1][col] = True
            
        elif col == 0 and row != 0 and row != len(self.grid) - 1:
            if self.grid[row][col] == "LV":
                if self.grid[row-1][col] in ["FB", "BD", "VB"]:
                    self.locked[row-1][col] = True
                if self.grid[row+1][col] in ["FC", "BD", "VD"]:
                    self.locked[row+1][col] = True
            elif self.grid[row][col] == "BD":
                if self.grid[row-1][col] in ["FB", "BD", "VB"]:
                    self.locked[row-1][col] = True
                if self.grid[row+1][col] in ["FC", "BD", "VD"]:
                    self.locked[row+1][col] = True
                if self.grid[row][col+1] == "LH" and col+1 != len(self.grid[row]) - 1:
                    self.locked[row][col+1] = True
                elif self.grid[row][col+1] == "FE":
                    self.locked[row][col+1] = True
            elif self.grid[row][col] == "VB":
                if self.grid[row][col+1] == "LH" and col+1 != len(self.grid[row]) - 1:
                    self.locked[row][col+1] = True
                elif self.grid[row][col+1] == "FE":
                    self.locked[row][col+1] = True
                if self.grid[row+1][col] in ["FC", "BD", "VD"]:
                    self.locked[row+1][col] = True
            elif self.grid[row][col] == "VD":
                if self.grid[row][col+1] == "LH" and col+1 != len(self.grid[row]) - 1:
                    self.locked[row][col+1] = True
                elif self.grid[row][col+1] == "FE":
                    self.locked[row][col+1] = True
                if self.grid[row-1][col] in ["FB", "BD", "VB"]:
                    self.locked[row-1][col] = True
        
        elif col == len(self.grid[row]) - 1 and row != 0 and row != len(self.grid) - 1:
            if self.grid[row][col] == "LV":
                if self.grid[row-1][col] in ["FB", "BE", "VE"]:
                    self.locked[row-1][col] = True
                if self.grid[row+1][col] in ["FC", "BE", "VC"]:
                    self.locked[row+1][col] = True
            elif self.grid[row][col] == "BE":
                if self.grid[row-1][col] in ["FB", "BE", "VE"]:
                    self.locked[row-1][col] = True
                if self.grid[row+1][col] in ["FC", "BE", "VC"]:
                    self.locked[row+1][col] = True
                if self.grid[row][col-1] == "LH" and col-1 != 0:
                    self.locked[row][col-1] = True
                elif self.grid[row][col-1] == "FD":
                    self.locked[row][col-1] = True
            elif self.grid[row][col] == "VC":
                if self.grid[row-1][col] in ["FB", "BE", "VE"]:
                    self.locked[row-1][col] = True
                if self.grid[row][col-1] == "LH" and col-1 != 0:
                    self.locked[row][col-1] = True
                elif self.grid[row][col-1] == "FD":
                    self.locked[row][col-1] = True
            elif self.grid[row][col] == "VE":
                if self.grid[row+1][col] in ["FC", "BE", "VC"]:
                    self.locked[row+1][col] = True
                if self.grid[row][col-1] == "LH" and col-1 != 0:
                    self.locked[row][col-1] = True
                elif self.grid[row][col-1] == "FD":
                    self.locked[row][col-1] = True
            
    
    
    
    def updateConncections(self, row: int, col: int):
        """Atualiza o número de conexões da peça na posição (row, col) e das peças adjacentes."""
        piece = self.grid[row][col]
        
        
        connections = 0
        
        up, down, left, right = [], [], [], []
        
        leftPiece, rightPiece = self.adjacent_horizontal_values(row, col)
        upper, lower = self.adjacent_vertical_values(row, col)
        
        if piece == "FC":
            up.extend(["BB", "BE", "BD", "VB", "VE", "LV", "FB"])
        elif piece == "FB":
            down.extend(["BC", "BE", "BD", "VC", "VD", "LV", "FC"])
        elif piece == "FD":
            right.extend(["BB", "BC", "BD", "VB", "VD", "LH", "FD"])
        elif piece == "FE":
            left.extend(["BB", "BC", "BE", "VC", "VE", "LH", "FE"])
        elif piece == "BC":
            up.extend(["BB", "BE", "BD", "VB", "VE", "LV", "FB"])
            left.extend(["BB", "BC", "BD", "VB", "VD", "LH", "FD"])
            right.extend(["BB", "BC", "BE", "VC", "VE", "LH", "FE"])
        elif piece == "BD":
            up.extend(["BB", "BE", "BD", "VB", "VE", "LV", "FB"])
            down.extend(["BC", "BE", "BD", "VC", "VD", "LV", "FC"])
            right.extend(["BB", "BC", "BD", "VB", "VD", "LH", "FD"])
        elif piece == "BE":
            up.extend(["BB", "BE", "BD", "VB", "VE", "LV", "FB"])
            down.extend(["BC", "BE", "BD", "VC", "VD", "LV", "FC"])
            left.extend(["BB", "BC", "BE", "VC", "VE", "LH", "FE"])
        elif piece == "BB":
            left.extend(["BB", "BC", "BD", "VB", "VD", "LH", "FD"])
            right.extend(["BB", "BC", "BE", "VC", "VE", "LH", "FE"])
            down.extend(["BC", "BE", "BD", "VC", "VD", "LV", "FC"])
        elif piece == "VC":
            up.extend(["BB", "BE", "BD", "VB", "VE", "LV", "FB"])
            left.extend(["BB", "BC", "BD", "VB", "VD", "LH", "FD"])
        elif piece == "VB":
            down.extend(["BC", "BE", "BD", "VC", "VD", "LV", "FC"])
            right.extend(["BB", "BC", "BE", "VC", "VE", "LH", "FE"])
        elif piece == "VE":
            down.extend(["BC", "BE", "BD", "VC", "VD", "LV", "FC"])
            left.extend(["BB", "BC", "BE", "VC", "VE", "LH", "FE"])
        elif piece == "VD":
            up.extend(["BB", "BE", "BD", "VB", "VE", "LV", "FB"])
            right.extend(["BB", "BC", "BD", "VB", "VD", "LH", "FD"])
        elif piece == "LH":
            left.extend(["BB", "BC", "BD", "VB", "VD", "LH", "FD"])
            right.extend(["BB", "BC", "BE", "VC", "VE", "LH", "FE"])
        elif piece == "LV":
            up.extend(["BB", "BE", "BD", "VB", "VE", "LV", "FB"])
            down.extend(["BC", "BE", "BD", "VC", "VD", "LV", "FC"])
            
        if upper in up:
            connections += 1
        
        if lower in down:
            connections += 1
        
        if leftPiece in left:
            connections += 1
        
        if rightPiece in right:
            connections += 1
            
        self.connections[row][col] = connections


    @staticmethod
    def parse_instance():
        """Lê a instância do problema do standard input (stdin)
        e retorna uma instância da classe Board."""

        board = Board()

        lines = stdin.readlines()
        for line in lines:
            line = line.strip()
            
            row = []
            lock = []
            conn = []
            
            for piece in line.split():
                row.append(piece)
                lock.append(False)
                conn.append(0)
            
            board.grid.append(row)
            board.locked.append(lock)
            board.connections.append(conn)
            
            
        for i in range(len(board.grid)):
            for j in range(len(board.grid[i])):
                board.updateConncections(i, j)
            

        return board

    def change_piece_orientation(self, row: int, col: int, orientation: str):
        """Muda a orientação da peça na posição (row, col) para a
        orientação passada como argumento."""
        self.grid[row][col] = orientation
        self.updateConncections(row, col)

    
    def copy(self):
        """Retorna uma cópia do tabuleiro."""
        board = Board()
        board.grid = [row.copy() for row in self.grid]
        board.locked = [row.copy() for row in self.locked]
        board.connections = [row.copy() for row in self.connections]
        return board
    
    
    def compare(self, other):
        """Compara o tabuleiro com outro tabuleiro passado como argumento."""
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != other.grid[i][j]:
                    return False
        return True
    
    def print(self):
        """Imprime o tabuleiro."""
        for row in self.grid:
            print(" ".join(row))
        print("\n")



class PipeMania(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        initial = PipeManiaState(board)
        super().__init__(initial)
        self.visited = []
        

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        actions = []
        
        print("Expanding state: ", state.id, "\n")
        board.print()

        if self.isVisited(board):
            return actions
        
        self.visited.append(board.copy())
        print("Adding board to visited:\n")
        board.print()
        
        print("Locks:", board.locked, "\n")

        for i in range(len(board.grid)):
            for j in range(len(board.grid[i])):
                
                if board.isLocked(i, j):
                    continue
                
                piece = board.get_value(i, j)

                if i == 0 and j == 0:
                    if piece.startswith("F"):
                        right = board.adjacent_horizontal_values(i, j)[1]
                        down = board.adjacent_vertical_values(i, j)[1]
                        
                        # Se uma peça adjecente está locked, só há uma ação possível
                        action = self.checkIfLockedFecho(board, i, j)
                        if action is not None and piece != action[2]:
                            actions.append(action)
                            continue
                        
                        if not right.startswith("F"):
                            actions.append((i, j, "FD"))
                        if not down.startswith("F"):
                            actions.append((i, j, "FB"))
                    elif piece.startswith("V"):
                        actions.append((i, j, "VB"))
            
                elif i == 0 and j == len(board.grid[i]) - 1:
                    if piece.startswith("F"):
                        left = board.adjacent_horizontal_values(i, j)[0]
                        down = board.adjacent_vertical_values(i, j)[1]
                        
                        # Se uma peça adjecente está locked, só há uma ação possível
                        action = self.checkIfLockedFecho(board, i, j)
                        if action is not None and piece != action[2]:
                            actions.append(action)
                            continue
                        
                        if not left.startswith("F"):
                            actions.append((i, j, "FE"))
                        if not down.startswith("F"):
                            actions.append((i, j, "FB"))
                    elif piece.startswith("V"):
                        actions.append((i, j, "VE"))

                elif i == len(board.grid) - 1 and j == 0:
                    if piece.startswith("F"):
                        right = board.adjacent_horizontal_values(i, j)[1]
                        up = board.adjacent_vertical_values(i, j)[0]
                        
                        # Se uma peça adjecente está locked, só há uma ação possível
                        action = self.checkIfLockedFecho(board, i, j)
                        if action is not None and piece != action[2]:
                            actions.append(action)
                            continue
                        
                        if not right.startswith("F"):
                            actions.append((i, j, "FD"))
                        if not up.startswith("F"):
                            actions.append((i, j, "FC"))
                    elif piece.startswith("V"):
                        actions.append((i, j, "VD"))
            
                elif i == len(board.grid) - 1 and j == len(board.grid[i]) - 1:
                    if piece.startswith("F"):
                        left = board.adjacent_horizontal_values(i, j)[0]
                        up = board.adjacent_vertical_values(i, j)[0]
                        
                        # Se uma peça adjecente está locked, só há uma ação possível
                        action = self.checkIfLockedFecho(board, i, j)
                        if action is not None and piece != action[2]:
                            actions.append(action)
                            continue
                        
                        
                        if not left.startswith("F"):
                            actions.append((i, j, "FE"))
                        if not up.startswith("F"):
                            actions.append((i, j, "FC"))
                    elif piece.startswith("V"):
                        actions.append((i, j, "VC"))

                elif i == 0 and j != 0 and j != len(board.grid[i]) - 1:
                    if piece.startswith("B"):
                        actions.append((i, j, "BB"))
                    elif piece.startswith("L"):
                        actions.append((i, j, "LH"))
                    elif piece.startswith("V"):
                        actions.extend([(i, j, "VB"), (i, j, "VE")])
                    elif piece.startswith("F"):
                        left = board.adjacent_horizontal_values(i, j)[0]
                        right = board.adjacent_horizontal_values(i, j)[1]
                        down = board.adjacent_vertical_values(i, j)[1]
                        
                        # Se uma peça adjecente está locked, só há uma ação possível
                        action = self.checkIfLockedFecho(board, i, j)
                        if action is not None and piece != action[2]:
                            actions.append(action)
                            continue
                        
                        if not left.startswith("F"):
                            actions.append((i, j, "FE"))
                        if not right.startswith("F"):
                            actions.append((i, j, "FD"))
                        if not down.startswith("F"):
                            actions.append((i, j, "FB"))
                
                elif i == len(board.grid) - 1 and j != 0 and j != len(board.grid[i]) - 1:
                    if piece.startswith("B"):
                        actions.append((i, j, "BC"))
                    elif piece.startswith("L"):
                        actions.append((i, j, "LH"))
                    elif piece.startswith("V"):
                        actions.extend([(i, j, "VC"), (i, j, "VD")])
                    elif piece.startswith("F"):
                        left = board.adjacent_horizontal_values(i, j)[0]
                        right = board.adjacent_horizontal_values(i, j)[1]
                        up = board.adjacent_vertical_values(i, j)[0]
                        
                        # Se uma peça adjecente está locked, só há uma ação possível
                        action = self.checkIfLockedFecho(board, i, j)
                        if action is not None and piece != action[2]:
                            actions.append(action)
                            continue
                        
                        if not left.startswith("F"):
                            actions.append((i, j, "FE"))
                        if not right.startswith("F"):
                            actions.append((i, j, "FD"))
                        if not up.startswith("F"):
                            actions.append((i, j, "FC"))

                elif j == 0 and i != 0 and i != len(board.grid) - 1:
                    if piece.startswith("B"):
                        actions.append((i, j, "BD"))
                    elif piece.startswith("L"):
                        actions.append((i, j, "LV"))
                    elif piece.startswith("V"):
                        actions.extend([(i, j, "VB"), (i, j, "VD")])
                    elif piece.startswith("F"):
                        up = board.adjacent_vertical_values(i, j)[0]
                        right = board.adjacent_horizontal_values(i, j)[1]
                        down = board.adjacent_vertical_values(i, j)[1]
                        
                        # Se uma peça adjecente está locked, só há uma ação possível
                        action = self.checkIfLockedFecho(board, i, j)
                        if action is not None and piece != action[2]:
                            actions.append(action)
                            continue
                        
                        if not up.startswith("F"):
                            actions.append((i, j, "FC"))
                        if not right.startswith("F"):
                            actions.append((i, j, "FD"))
                        if not down.startswith("F"):
                            actions.append((i, j, "FB"))    

                elif j == len(board.grid[i]) - 1 and i != 0 and i != len(board.grid) - 1:
                    if piece.startswith("B"):
                        actions.append((i, j, "BE"))
                    elif piece.startswith("L"):
                        actions.append((i, j, "LV"))
                    elif piece.startswith("V"):
                        actions.extend([(i, j, "VC"), (i, j, "VE")])
                    elif piece.startswith("F"):
                        up = board.adjacent_vertical_values(i, j)[0]
                        left = board.adjacent_horizontal_values(i, j)[0]
                        down = board.adjacent_vertical_values(i, j)[1]
                        
                        # Se uma peça adjecente está locked, só há uma ação possível
                        action = self.checkIfLockedFecho(board, i, j)
                        if action is not None and piece != action[2]:
                            actions.append(action)
                            continue
                        
                        if not up.startswith("F"):
                            actions.append((i, j, "FC"))
                        if not left.startswith("F"):
                            actions.append((i, j, "FE"))
                        if not down.startswith("F"):
                            actions.append((i, j, "FB"))

                else:
                    if piece.startswith("B"):
                        ac = self.checkIfLockedBifurcacao(board, i, j)
                        if ac is not None:
                            actions.append(ac)
                        else:
                            left = board.adjacent_horizontal_values(i, j)[0]
                            right = board.adjacent_horizontal_values(i, j)[1]
                            up = board.adjacent_vertical_values(i, j)[0]
                            down = board.adjacent_vertical_values(i, j)[1]
                            
                            if not (board.isLocked(i-1, j) and up in ["FC", "FE", "FD", "BC", "VC", "VD", "LH"]):
                                actions.append((i, j, "BC"))
                            if not (board.isLocked(i+1, j) and down in ["FB", "FE", "FD", "BB", "VB", "VE", "LH"]):
                                actions.append((i, j, "BB"))
                            if not (board.isLocked(i, j-1) and left in ["FC", "FB", "FE", "BE", "VE", "VC", "LV"]):
                                actions.append((i, j, "BE"))
                            if not (board.isLocked(i, j+1) and right in ["FC", "FB", "FD", "BD", "VB", "VD", "LV"]):
                                actions.append((i, j, "BD"))
                                
                    elif piece.startswith("L"):
                        actions.extend([(i, j, "LH"), (i, j, "LV")])
                    elif piece.startswith("V"):
                        actions.extend([(i, j, "VB"), (i, j, "VC"), (i, j, "VD"), (i, j, "VE")])
                    elif piece.startswith("F"):
                        up = board.adjacent_vertical_values(i, j)[0]
                        left = board.adjacent_horizontal_values(i, j)[0]
                        right = board.adjacent_horizontal_values(i, j)[1]
                        down = board.adjacent_vertical_values(i, j)[1]
                        
                        # Se uma peça adjecente está locked, só há uma ação possível
                        action = self.checkIfLockedFecho(board, i, j)
                        if action is not None and piece != action[2]:
                            actions.append(action)
                            continue
                        
                        if not up.startswith("F"):
                            actions.append((i, j, "FC"))
                        if not left.startswith("F"):
                            actions.append((i, j, "FE"))
                        if not right.startswith("F"):
                            actions.append((i, j, "FD"))
                        if not down.startswith("F"):
                            actions.append((i, j, "FB"))       

                # Remove a ação de colocar a peça na posição atual caso seja adicionada.
                if (i, j, piece) in actions:
                    actions.remove((i, j, piece))

        actionsToRemove = []
        
        for action in actions:
            copy = state.board.copy()
            copy.change_piece_orientation(action[0], action[1], action[2])
            
            for b in self.visited:
                if copy.compare(b):
                    actionsToRemove.append(action)
                    break
                    
        
        for action in actionsToRemove:
            actions.remove(action)
    
        
        random.shuffle(actions) 
        print("Actions:", actions, "\n")   
        return actions



    def checkIfLockedBifurcacao(self, board, row, col):
        """Restringe as ações possíveis para peças do tipo "B" bifurcação."""
        
        up = ["BB", "BE", "BD", "VB", "VE", "LV", "FD"]   # Peças que encaixam com peça com abertura virada pra cima
        left = ["BB", "BC", "BD", "VB", "VD", "LH", "FD"] # Peças que encaixam com peça com abertura virada pra esquerda
        right = ["BB", "BC", "BE", "VC", "VE", "LH" "FE"] # Peças que encaixam com peça com abertura virada pra direita
        down = ["BC", "BE", "BD", "VC", "VD", "LV", "FC"] # Peças que encaixam com peça com abertura virada pra baixo
        
        up_piece = board.adjacent_vertical_values(row, col)[0]
        down_piece = board.adjacent_vertical_values(row, col)[1]
        left_piece = board.adjacent_horizontal_values(row, col)[0]
        right_piece = board.adjacent_horizontal_values(row, col)[1]
        
        if board.isLocked(row+1, col) and board.isLocked(row, col+1) and board.isLocked(row, col-1):
            if down_piece in down and left_piece in left and right_piece in right:
                return (row, col, "BB")
        elif board.isLocked(row-1, col) and board.isLocked(row, col+1) and board.isLocked(row, col-1):
            if up_piece in up and left_piece in left and right_piece in right:
                return (row, col, "BC")
        elif board.isLocked(row+1, col) and board.isLocked(row-1, col) and board.isLocked(row, col-1):
            if down_piece in down and up_piece in up and left_piece in left:
                return (row, col, "BE")
        elif board.isLocked(row+1, col) and board.isLocked(row-1, col) and board.isLocked(row, col+1):
            if down_piece in down and up_piece in up and right_piece in right:
                return (row, col, "BD")
        
        return None
            
            


    def checkIfLockedFecho(self, board, row, col):
        """Restringe as ações possíveis para peças do tipo "F" fecho."""
        
        up = ["BB", "BE", "BD", "VB", "VE", "LV"]   # Peças que encaixam com peça com abertura virada pra cima
        left = ["BB", "BC", "BD", "VB", "VD", "LH"] # Peças que encaixam com peça com abertura virada pra esquerda
        right = ["BB", "BC", "BE", "VC", "VE", "LH"] # Peças que encaixam com peça com abertura virada pra direita
        down = ["BC", "BE", "BD", "VC", "VD", "LV"] # Peças que encaixam com peça com abertura virada pra baixo
        
        
        if row == 0 and col == 0:
           if board.isLocked(row+1, col) and board.get_value(row+1, col) in down:
               return (row, col, "FB")
           elif board.isLocked(row, col+1) and board.get_value(row, col+1) in right:
               return (row, col, "FD")

        elif row == 0 and col == len(board.grid[row]) - 1:
            if board.isLocked(row+1, col) and board.get_value(row+1, col) in down:
                return (row, col, "FB")
            elif board.isLocked(row, col-1) and board.get_value(row, col-1) in left:
                return (row, col, "FE")
        
        elif row == len(board.grid) - 1 and col == 0:
            if board.isLocked(row-1, col) and board.get_value(row-1, col) in up:
                return (row, col, "FC")
            elif board.isLocked(row, col+1) and board.get_value(row, col+1) in right:
                return (row, col, "FD")
        
        elif row == len(board.grid) - 1 and col == len(board.grid[row]) - 1:
            if board.isLocked(row-1, col) and board.get_value(row-1, col) in up:
                return (row, col, "FC")
            elif board.isLocked(row, col-1) and board.get_value(row, col-1) in left:
                return (row, col, "FE")
        
        elif row == 0 and col != 0 and col != len(board.grid[row]) - 1:
            if board.isLocked(row+1, col) and board.get_value(row+1, col) in down:
                return (row, col, "FB")
            elif board.isLocked(row, col-1) and board.get_value(row, col-1) in left:
                return (row, col, "FE")
            elif board.isLocked(row, col+1) and board.get_value(row, col+1) in right:
                return (row, col, "FD")
        
        elif row == len(board.grid) - 1 and col != 0 and col != len(board.grid[row]) - 1:
            if board.isLocked(row-1, col) and board.get_value(row-1, col) in up:
                return (row, col, "FC")
            elif board.isLocked(row, col-1) and board.get_value(row, col-1) in left:
                return (row, col, "FE")
            elif board.isLocked(row, col+1) and board.get_value(row, col+1) in right:
                return (row, col, "FD")
        
        elif col == 0 and row != 0 and row != len(board.grid) - 1:
            if board.isLocked(row-1, col) and board.get_value(row-1, col) in up:
                return (row, col, "FC")
            elif board.isLocked(row+1, col) and board.get_value(row+1, col) in down:
                return (row, col, "FB")
            elif board.isLocked(row, col+1) and board.get_value(row, col+1) in right:
                return (row, col, "FD")
            
        elif col == len(board.grid[row]) - 1 and row != 0 and row != len(board.grid) - 1:
            if board.isLocked(row-1, col) and board.get_value(row-1, col) in up:
                return (row, col, "FC")
            elif board.isLocked(row+1, col) and board.get_value(row+1, col) in down:
                return (row, col, "FB")
            elif board.isLocked(row, col-1) and board.get_value(row, col-1) in left:
                return (row, col, "FE")
        
        return None




    def isVisited(self, board):
        
        for b in self.visited:
            if board.compare(b):
                return True
        
        return False



    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        board = state.board.copy()
        row, col, orientation = action
        
        board.change_piece_orientation(row, col, orientation)
 
        
        # Dá lock às peças dos cantos e arestas e às adjecentes
        if row == 0 and col == 0:
            if orientation == "VB":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "FD":
                if board.get_value(row+1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FB":
                if board.get_value(row, col+1).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            
            
        
        elif row == 0 and col == len(board.grid[row]) - 1:
            if orientation == "VE":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "FE":
                if board.get_value(row+1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FB":
                if board.get_value(row, col-1).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
                
        
        elif row == len(board.grid) - 1 and col == 0:
            if orientation == "VD":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "FC":
                if board.get_value(row, col+1).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FD":
                if board.get_value(row-1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
                
        
        elif row == len(board.grid) - 1 and col == len(board.grid[row]) - 1:
            if orientation == "VC":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "FC":
                if board.get_value(row, col-1).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FE":
                if board.get_value(row-1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)                
                
        elif row == 0 and col != 0 and col != len(board.grid[row]) - 1:
            if orientation == "LH":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "BB":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "VB":
                if board.isLocked(row, col+1) and board.get_value(row, col+1) in ["FE", "LH", "BB", "VE"]:
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "VE":
                if board.isLocked(row, col-1) and board.get_value(row, col-1) in ["FD", "LH", "BB", "VB"]:
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FD":
                if board.get_value(row, col-1).startswith("F") and board.get_value(row+1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FE":
                if board.get_value(row, col+1).startswith("F") and board.get_value(row+1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FB":
                if board.get_value(row, col+1).startswith("F") and board.get_value(row, col-1).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            
        
        elif row == len(board.grid) - 1 and col != 0 and col != len(board.grid[row]) - 1:
            if orientation == "LH":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "BC":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "VC":
                if board.isLocked(row, col-1) and board.get_value(row, col-1) in ["FD", "LH", "BC", "VD"]:
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "VD":
                if board.isLocked(row, col+1) and board.get_value(row, col+1) in ["FE", "LH", "BC", "VC"]:
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FD":
                if board.get_value(row, col-1).startswith("F") and board.get_value(row-1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FE":
                if board.get_value(row, col+1).startswith("F") and board.get_value(row-1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FC":
                if board.get_value(row, col+1).startswith("F") and board.get_value(row, col-1).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            
            
                
        elif col == 0 and row != 0 and row != len(board.grid) - 1:
            if orientation == "LV":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "BD":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "VB":
                if board.isLocked(row+1, col) and board.get_value(row+1, col) in ["FC", "BD", "VD", "LV"]:
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "VD":
                if board.isLocked(row-1, col) and board.get_value(row-1, col) in ["FB", "BD", "VB", "LV"]:
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FC":
                if board.get_value(row+1, col).startswith("F") and board.get_value(row, col+1).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FB":
                if board.get_value(row, col+1).startswith("F") and board.get_value(row-1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FD":
                if board.get_value(row+1, col).startswith("F") and board.get_value(row-1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
        
        elif col == len(board.grid[row]) - 1 and row != 0 and row != len(board.grid) - 1:
            if orientation == "LV":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "BE":
                board.locked[row][col] = True
                board.updateLocks(row, col)
            elif orientation == "VC":
                if board.isLocked(row-1, col) and board.get_value(row-1, col) in ["FB", "BE", "VE", "LV"]:
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "VE":
                if board.isLocked(row+1, col) and board.get_value(row+1, col) in ["FC", "BE", "VC", "LV"]:
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FC":
                if board.get_value(row+1, col).startswith("F") and board.get_value(row, col-1).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FE":
                if board.get_value(row+1, col).startswith("F") and board.get_value(row-1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
            elif orientation == "FB":
                if board.get_value(row, col-1).startswith("F") and board.get_value(row-1, col).startswith("F"):
                    board.locked[row][col] = True
                    board.updateLocks(row, col)
        
        
        
        # Dá lock às peças que não estão nos cantos nem nas arestas e às adjecentes
        if orientation == "FB":
            down = board.adjacent_vertical_values(row, col)[1]
            if down in ["BC", "BE", "BD", "VC", "VD", "LV"]:
                if board.isLocked(row+1, col):
                    board.locked[row][col] = True
                   
        
        elif orientation == "FC":
            up = board.adjacent_vertical_values(row, col)[0]
            if up in ["BB", "BE", "BD", "VB", "VE", "LV"]:
                if board.isLocked(row-1, col):
                    board.locked[row][col] = True
                    
        
        elif orientation == "FD":
            right = board.adjacent_horizontal_values(row, col)[1]
            if right in ["BB", "BC", "BE", "VC", "VE", "LH"]:
                if board.isLocked(row, col+1):
                    board.locked[row][col] = True
                    
                    
        elif orientation == "FE":
            left = board.adjacent_horizontal_values(row, col)[0]
            if left in ["BB", "BC", "BD", "VB", "VD", "LH"]:
                if board.isLocked(row, col-1):
                    board.locked[row][col] = True
                    
                    
        elif orientation == "BC":
            left = board.adjacent_horizontal_values(row, col)[0]
            right = board.adjacent_horizontal_values(row, col)[1]
            up = board.adjacent_vertical_values(row, col)[0]
            if left in ["BB", "BC", "BD", "VB", "VD", "LH", "FD"] and right in ["BB", "BC", "BE", "VC", "VE", "LH", "FE"] and up in ["BB", "BE", "BD", "VB", "VE", "LV", "FB"]:
                if board.isLocked(row, col-1) and board.isLocked(row, col+1) and board.isLocked(row-1, col):
                    board.locked[row][col] = True
        
        elif orientation == "BD":
            up = board.adjacent_vertical_values(row, col)[0]
            down = board.adjacent_vertical_values(row, col)[1]
            right = board.adjacent_horizontal_values(row, col)[1]
            if up in ["BB", "BE", "BD", "VB", "VE", "LV", "FB"] and down in ["BC", "BE", "BD", "VC", "VD", "LV", "FC"] and right in ["BB", "BC", "BE", "VC", "VE", "LH", "FE"]:
                if board.isLocked(row-1, col) and board.isLocked(row+1, col) and board.isLocked(row, col+1):
                    board.locked[row][col] = True
                    
        elif orientation == "BE":
            up = board.adjacent_vertical_values(row, col)[0]
            down = board.adjacent_vertical_values(row, col)[1]
            left = board.adjacent_horizontal_values(row, col)[0]
            if up in ["BB", "BE", "BD", "VB", "VE", "LV", "FB"] and down in ["BC", "BE", "BD", "VC", "VD", "LV", "FC"] and left in ["BB", "BC", "BD", "VB", "VD", "LH", "FD"]:
                if board.isLocked(row-1, col) and board.isLocked(row+1, col) and board.isLocked(row, col-1):
                    board.locked[row][col] = True
        
        elif orientation == "BB":
            left = board.adjacent_horizontal_values(row, col)[0]
            right = board.adjacent_horizontal_values(row, col)[1]
            down = board.adjacent_vertical_values(row, col)[1]
            if left in ["BB", "BC", "BD", "VB", "VD", "LH", "FD"] and right in ["BB", "BC", "BE", "VC", "VE", "LH", "FE"] and down in ["BC", "BE", "BD", "VC", "VD", "LV", "FC"]:
                if board.isLocked(row, col-1) and board.isLocked(row, col+1) and board.isLocked(row+1, col):
                    board.locked[row][col] = True
            
        elif orientation == "VC":
            up = board.adjacent_vertical_values(row, col)[0]
            left = board.adjacent_horizontal_values(row, col)[0]
            if up in ["BB", "BE", "BD", "VB", "VE", "LV", "FB"] and left in ["BB", "BC", "BD", "VB", "VD", "LH", "FD"]:
                if board.isLocked(row-1, col) and board.isLocked(row, col-1):
                    board.locked[row][col] = True   
                      
        
        elif orientation == "VB":
            down = board.adjacent_vertical_values(row, col)[1]
            right = board.adjacent_horizontal_values(row, col)[1]
            if down in ["BC", "BE", "BD", "VC", "VD", "LV", "FC"] and right in ["BB", "BC", "BE", "VC", "VE", "LH", "FE"]:
                if board.isLocked(row+1, col) and board.isLocked(row, col+1):
                    board.locked[row][col] = True
                   
                    
        elif orientation == "VE":
            down = board.adjacent_vertical_values(row, col)[1]
            left = board.adjacent_horizontal_values(row, col)[0]
            if down in ["BC", "BE", "BD", "VC", "VD", "LV", "FC"] and left in ["BB", "BC", "BD", "VB", "VD", "LH", "FD"]:
                if board.isLocked(row+1, col) and board.isLocked(row, col-1):
                    board.locked[row][col] = True
                   
                    
        elif orientation == "VD":
            up = board.adjacent_vertical_values(row, col)[0]
            right = board.adjacent_horizontal_values(row, col)[1]
            if up in ["BB", "BE", "BD", "VB", "VE", "LV", "FB"] and right in ["BB", "BC", "BE", "VC", "VE", "LH", "FE"]:
                if board.isLocked(row-1, col) and board.isLocked(row, col+1):
                    board.locked[row][col] = True
                  
        
        elif orientation == "LH":
            left = board.adjacent_horizontal_values(row, col)[0]
            right = board.adjacent_horizontal_values(row, col)[1]
            if left in ["BB", "BC", "BD", "VB", "VD", "LH", "FD"] and board.isLocked(row, col-1):
                board.locked[row][col] = True

            
            elif right in ["BB", "BC", "BE", "VC", "VE", "LH", "FE"] and board.isLocked(row, col+1):
                board.locked[row][col] = True
                
                    
        elif orientation == "LV":
            up = board.adjacent_vertical_values(row, col)[0]
            down = board.adjacent_vertical_values(row, col)[1]
            if up in ["BB", "BE", "BD", "VB", "VE", "LV", "FB"] and down in ["BC", "BE", "BD", "VC", "VD", "LV", "FC"]:
                if board.isLocked(row-1, col) and board.isLocked(row+1, col):
                    board.locked[row][col] = True
    
            
           

        return PipeManiaState(board)

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        board = state.board

        up = ["BB", "BE", "BD", "VB", "VE", "LV", "FB"]         # Peças que encaixam com peça com abertura virada pra cima
        down = ["BC", "BE", "BD", "VC", "VD", "LV", "FC"]       # Peças que encaixam com peça com abertura virada pra baixo
        left = ["BB", "BC", "BD", "VB", "VD", "LH", "FD"]       # Peças que encaixam com peça com abertura virada pra esquerda
        right = ["BB", "BC", "BE", "VC", "VE", "LH", "FE"]      # Peças que encaixam com peça com abertura virada pra direita


        # Verificar se todas as peças encaixam com as peças adjacentes
        for i in range(len(board.grid)):
            for j in range(len(board.grid[i])):
                piece = board.get_value(i, j)
                if piece == "FC":
                    upper = board.adjacent_vertical_values(i, j)[0]
                    if upper not in up:
                        return False
                    
                elif piece == "FB":
                    lower = board.adjacent_vertical_values(i, j)[1]
                    if lower not in down:
                        return False
                
                elif piece == "FD":
                    rightPiece = board.adjacent_horizontal_values(i, j)[1]
                    if rightPiece not in right:
                        return False
                
                elif piece == "FE":
                    leftPiece = board.adjacent_horizontal_values(i, j)[0]
                    if leftPiece not in left:
                        return False
                
                elif piece == "BC":
                    upper = board.adjacent_vertical_values(i, j)[0]
                    leftPiece = board.adjacent_horizontal_values(i, j)[0]
                    rightPiece = board.adjacent_horizontal_values(i, j)[1]
                    if upper not in up or leftPiece not in left or rightPiece not in right:
                        return False
                
                elif piece == "BD":
                    upper = board.adjacent_vertical_values(i, j)[0]
                    lower = board.adjacent_vertical_values(i, j)[1]
                    rightPiece = board.adjacent_horizontal_values(i, j)[1]
                    if upper not in up or lower not in down or rightPiece not in right:
                        return False
                
                elif piece == "BE":
                    upper = board.adjacent_vertical_values(i, j)[0]
                    lower = board.adjacent_vertical_values(i, j)[1]
                    leftPiece = board.adjacent_horizontal_values(i, j)[0]
                    if upper not in up or lower not in down or leftPiece not in left:
                        return False
                
                elif piece == "BB":
                    leftPiece = board.adjacent_horizontal_values(i, j)[0]
                    rightPiece = board.adjacent_horizontal_values(i, j)[1]
                    lower = board.adjacent_vertical_values(i, j)[1]
                    if leftPiece not in left or rightPiece not in right or lower not in down:
                        return False
                    
                elif piece == "VC":
                    upper = board.adjacent_vertical_values(i, j)[0]
                    leftPiece = board.adjacent_horizontal_values(i, j)[0]
                    if upper not in up or leftPiece not in left:
                        return False
                    
                elif piece == "VB":
                    lower = board.adjacent_vertical_values(i, j)[1]
                    rightPiece = board.adjacent_horizontal_values(i, j)[1]
                    if lower not in down or rightPiece not in right:
                        return False
                    
                elif piece == "VE":
                    lower = board.adjacent_vertical_values(i, j)[1]
                    leftPiece = board.adjacent_horizontal_values(i, j)[0]
                    if lower not in down or leftPiece not in left:
                        return False
                
                elif piece == "VD":
                    upper = board.adjacent_vertical_values(i, j)[0]
                    rightPiece = board.adjacent_horizontal_values(i, j)[1]
                    if upper not in up or rightPiece not in right:
                        return False
                
                elif piece == "LH":
                    leftPiece = board.adjacent_horizontal_values(i, j)[0]
                    rightPiece = board.adjacent_horizontal_values(i, j)[1]
                    if leftPiece not in left or rightPiece not in right:
                        return False
                
                elif piece == "LV":
                    upper = board.adjacent_vertical_values(i, j)[0]
                    lower = board.adjacent_vertical_values(i, j)[1]
                    if upper not in up or lower not in down:
                        return False
                
        # Se todas as peças encaixam, então o tabuleiro está resolvido
        return True


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


'''
Pieces that match:

    Cima: "BB", "BE", "BD", "VB", "VE", "LV", "FB";
    Baixo: "BC", "BE", "BD", "VC", "VD", "LV", "FC";
    Esquerda: "BB", "BC", "BD", "VB", "VD", "LH", "FD";
    Direita: "BB", "BC", "BE", "VC", "VE", "LH", "FE";

    - "FC" Cima;
    - "FB" Baixo;
    - "FD" Direita;
    - "FE" Esquerda;
    - "BC" Cima, Esquerda, Direita;
    - "BD" Cima, Baixo, Direita;
    - "BE" Cima, Baixo, Esquerda;
    - "BB" Esquerda, Direita, Baixo;
    - "VC" Cima, Esquerda;
    - "VB" Baixo, Direita;
    - "VE" Esquerda, Baixo;
    - "VD" Cima, Direita;
    - "LH" Esquerda, Direita;
    - "LV" Cima, Baixo;

'''






if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.



    # Teste da classe Board e goal test
    board = Board.parse_instance()
    problem = PipeMania(board)
    
    goal_node = depth_first_tree_search(problem)

    print("Is goal?", problem.goal_test(goal_node.state), "\n")
    print("Solution:\n")
    goal_node.state.board.print()
    

    pass
