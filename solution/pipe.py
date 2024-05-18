
# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 02:
# 99044 Adrian Graur
# 99131 Vasco Roda Félix

import sys
import random
import copy
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

    def __init__(self, board, moved=[]):
        self.board = board
        self.id = PipeManiaState.state_id
        self.moved = moved
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    grid = [] # Lista de listas de strings
   
    def getPiece(self, row: int, col: int):
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

    def updateConnections(self, row: int, col: int):
        """Atualiza o número de conexões da peça na posição (row, col) e das peças adjacentes."""
        
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[row]):
            return
        
        connections = 0
        piece = self.grid[row][col]
        
        leftPiece, rightPiece = self.adjacent_horizontal_values(row, col)
        upPiece, downPiece = self.adjacent_vertical_values(row, col)
        
        if leftPiece != None and piece.isConnected(leftPiece, "left"):
            connections += 1
        if rightPiece != None and piece.isConnected(rightPiece, "right"):
            connections += 1
        if upPiece != None and piece.isConnected(upPiece, "up"):
            connections += 1
        if downPiece != None and piece.isConnected(downPiece, "down"):
            connections += 1
        
        piece.updateConnections(connections)
        

    @staticmethod
    def parse_instance():
        """Lê a instância do problema do standard input (stdin)
        e retorna uma instância da classe Board."""

        board = Board()

        lines = stdin.readlines()
        for line in lines:
            line = line.strip()
            
            row = []
            
            for piece in line.split():
                row.append(Piece(piece))
               
            
            board.grid.append(row)

        for row in range(len(board.grid)):
            for col in range(len(board.grid[row])):
                if board.checkIfLocks(row, col, board.grid[row][col].orientation):
                    board.grid[row][col].lock()
        
        for row in range(len(board.grid)):
            for col in range(len(board.grid[row])):
                board.updateConnections(row, col)
                
        
        return board

    def change_piece_orientation(self, row: int, col: int, orientation: str):
        """Muda a orientação da peça na posição (row, col) para a
        orientação passada como argumento."""
        self.grid[row][col].setOrientation(orientation)

    def lockPiece(self, row: int, col: int):
        """Bloqueia a peça na posição (row, col)."""
        self.grid[row][col].lock()
        
    def compare(self, other):
        """Compara o tabuleiro com outro tabuleiro passado como argumento."""
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] != other.grid[row][col]:
                    return False
        
        return True
        
    def copy(self):
        """Retorna uma cópia do tabuleiro."""
        board = Board() 
        board.grid = copy.deepcopy(self.grid)
        return board
    
    def __str__(self) -> str:
        string = ""
        for r, row in enumerate(self.grid):
            for p, piece in enumerate(row):
                string += piece.orientation + ("\t" if p != len(row) - 1 else "")
            string += ("\n" if r != len(self.grid) - 1 else "")
        
        return string

    def checkIfLocks(self, row: int, col: int, orientation: str):
        """Verifica se a peça na posição (row, col) pode ser bloqueada"""
        leftPiece, rightPiece = self.adjacent_horizontal_values(row, col)
        upPiece, downPiece = self.adjacent_vertical_values(row, col)

        piece = Piece(orientation)
        
        zones = {
            "leftUpperCorner": row == 0 and col == 0,
            "rightUpperCorner": row == 0 and col == len(self.grid[row]) - 1,
            "leftLowerCorner": row == len(self.grid) - 1 and col == 0,
            "rightLowerCorner": row == len(self.grid) - 1 and col == len(self.grid[row]) - 1,
            "upperEdge": row == 0 and col != 0 and col != len(self.grid[row]) - 1,
            "lowerEdge": row == len(self.grid) - 1 and col != 0 and col != len(self.grid[row]) - 1,
            "leftEdge": col == 0 and row != 0 and row != len(self.grid) - 1,
            "rightEdge": col == len(self.grid[row]) - 1 and row != 0 and row != len(self.grid) - 1,
        }
        
        upC , downC, leftC, rightC, upDC, downDC, leftDC, rightDC = False, False, False, False, False, False, False, False
        if leftPiece != None:
            leftC = leftPiece.isLocked() and piece.connectsWith(leftPiece, "left")
            leftDC = leftPiece.isLocked() and not piece.connectsWith(leftPiece, "left")
        if rightPiece != None:
            rightC = rightPiece.isLocked() and piece.connectsWith(rightPiece, "right")
            rightDC = rightPiece.isLocked() and not piece.connectsWith(rightPiece, "right")
        if upPiece != None:
            upC = upPiece.isLocked() and piece.connectsWith(upPiece, "up")
            upDC = upPiece.isLocked() and not piece.connectsWith(upPiece, "up")
        if downPiece != None:
            downC = downPiece.isLocked() and piece.connectsWith(downPiece, "down")
            downDC = downPiece.isLocked() and not piece.connectsWith(downPiece, "down")
        
        conditions = {
            "upConnects": upC,
            "downConnects": downC,
            "leftConnects": leftC,
            "rightConnects": rightC,
            "upDoesntConnect": upDC,
            "downDoesntConnect": downDC,
            "leftDoesntConnect": leftDC,
            "rightDoesntConnect": rightDC
        }
        
        if zones["leftUpperCorner"]:
            if orientation == "VB":
                return True
            
            elif orientation == "FD":
                return conditions["downDoesntConnect"] or conditions["rightConnects"]
            
            elif orientation == "FB":
                return conditions["downConnects"] or conditions["rightDoesntConnect"]
                
        elif zones["rightUpperCorner"]:
            if orientation == "VE":
                return True
            
            elif orientation == "FE":
                return conditions["downDoesntConnect"] or conditions["leftConnects"]  
            
            elif orientation == "FB":
                return conditions["downConnects"] or conditions["leftDoesntConnect"]
                        
        elif zones["leftLowerCorner"]:
            if orientation == "VD":
                return True
            
            elif orientation == "FD":
                return conditions["upDoesntConnect"] or conditions["rightConnects"]
            
            elif orientation == "FC":
                return conditions["upConnects"] or conditions["rightDoesntConnect"]
                        
        elif zones["rightLowerCorner"]:
            if orientation == "VC":
                return True
            
            elif orientation == "FE":
                return conditions["upDoesntConnect"] or conditions["leftConnects"]
            
            elif orientation == "FC":
                return conditions["upConnects"] or conditions["leftDoesntConnect"]
        
        elif zones["upperEdge"]:
            if orientation == "FB":
                return conditions["downConnects"] or (conditions["leftDoesntConnect"] and conditions["rightDoesntConnect"])
            
            elif orientation == "FD":
                return conditions["rightConnects"] or (conditions["downDoesntConnect"] and conditions["leftDoesntConnect"])
            
            elif orientation == "FE":
                return conditions["leftConnects"] or (conditions["downDoesntConnect"] and conditions["rightDoesntConnect"])
            
            elif orientation == "BB":
                return True
            
            elif orientation == "LH":
                return True
            
            elif orientation == "VE":
                return conditions["leftConnects"] or conditions["rightDoesntConnect"]
            
            elif orientation == "VB":
                return conditions["rightConnects"] or conditions["leftDoesntConnect"]
        
        elif zones["lowerEdge"]:
            if orientation == "FC":
                return conditions["upConnects"] or (conditions["leftDoesntConnect"] and conditions["rightDoesntConnect"])
                        
            elif orientation == "FD":
                return conditions["rightConnects"] or (conditions["upDoesntConnect"] and conditions["leftDoesntConnect"])
                        
            elif orientation == "FE":
                return conditions["leftConnects"] or (conditions["upDoesntConnect"] and conditions["rightDoesntConnect"])
            
            elif orientation == "BC":
                return True
            
            elif orientation == "LH":
                return True
            
            elif orientation == "VC":
                return conditions["leftConnects"] or conditions["rightDoesntConnect"]
            
            elif orientation == "VD":
                return conditions["rightConnects"] or conditions["leftDoesntConnect"]
        
        elif zones["leftEdge"]:
            if orientation == "FD":
                return conditions["rightConnects"] or (conditions["upDoesntConnect"] and conditions["downDoesntConnect"])
                        
            elif orientation == "FB":
                return conditions["downConnects"] or (conditions["upDoesntConnect"] and conditions["rightDoesntConnect"])
                        
            elif orientation == "FC":
                return conditions["upConnects"] or (conditions["downDoesntConnect"] and conditions["rightDoesntConnect"])
            
            elif orientation == "BD":
                return True
            
            elif orientation == "LV":
                return True
            
            elif orientation == "VB":
                return conditions["downConnects"] or conditions["upDoesntConnect"]
            
            elif orientation == "VD":
                return conditions["upConnects"] or conditions["downDoesntConnect"]
        
        elif zones["rightEdge"]:
            if orientation == "FE":
                return conditions["leftConnects"] or (conditions["upDoesntConnect"] and conditions["downDoesntConnect"])
                        
            elif orientation == "FB":
                return conditions["downConnects"] or (conditions["upDoesntConnect"] and conditions["leftDoesntConnect"])
                        
            elif orientation == "FC":
                return conditions["upConnects"] or (conditions["downDoesntConnect"] and conditions["leftDoesntConnect"])
            
            elif orientation == "BE":
                return True
            
            elif orientation == "LV":
                return True
            
            elif orientation == "VC":
                return conditions["upConnects"] or conditions["downDoesntConnect"]
            
            elif orientation == "VE":
                return conditions["downConnects"] or conditions["upDoesntConnect"]
        
        else:
            if orientation == "FB":
                return conditions["downConnects"] or (conditions["upDoesntConnect"] and conditions["leftDoesntConnect"] and conditions["rightDoesntConnect"])
            elif orientation == "FD":
                return conditions["rightConnects"] or (conditions["downDoesntConnect"] and conditions["upDoesntConnect"] and conditions["leftDoesntConnect"])
            elif orientation == "FE":
                return conditions["leftConnects"] or (conditions["downDoesntConnect"] and conditions["upDoesntConnect"] and conditions["rightDoesntConnect"])
            elif orientation == "FC":
                return conditions["upConnects"] or (conditions["downDoesntConnect"] and conditions["leftDoesntConnect"] and conditions["rightDoesntConnect"])
            
            elif orientation == "LH":
                return (conditions["leftConnects"] or conditions["rightConnects"]) or (conditions["upDoesntConnect"] or conditions["downDoesntConnect"])
            elif orientation == "LV":
                return (conditions["upConnects"] or conditions["downConnects"]) or (conditions["leftDoesntConnect"] or conditions["rightDoesntConnect"]) 
            
            elif orientation == "BB":
                return conditions["upDoesntConnect"] or (conditions["leftConnects"] and conditions["rightConnects"] and conditions["downConnects"]) 
                         
            elif orientation == "BC":
                return conditions["downDoesntConnect"] or (conditions["leftConnects"] and conditions["rightConnects"] and conditions["upConnects"]) 
                                         
            elif orientation == "BE":
                return conditions["rightDoesntConnect"] or (conditions["leftConnects"] and conditions["upConnects"] and conditions["downConnects"]) 
                            
            elif orientation == "BD":
                return conditions["leftDoesntConnect"] or (conditions["rightConnects"] and conditions["upConnects"] and conditions["downConnects"]) 


            elif orientation == "VC":
                return (conditions["upConnects"] and conditions["leftConnects"]) or \
                       (conditions["leftConnects"] and conditions["downDoesntConnect"]) or \
                       (conditions["upConnects"] and conditions["rightDoesntConnect"]) or \
                       (conditions["downDoesntConnect"] and conditions["rightDoesntConnect"])
            elif orientation == "VD":
                return (conditions["upConnects"] and conditions["rightConnects"]) or \
                       (conditions["rightConnects"] and conditions["downDoesntConnect"]) or \
                       (conditions["upConnects"] and conditions["leftDoesntConnect"])  or \
                       (conditions["downDoesntConnect"]  and conditions["leftDoesntConnect"])
            elif orientation == "VE":
                return (conditions["downConnects"] and conditions["leftConnects"]) or \
                       (conditions["leftConnects"] and conditions["upDoesntConnect"]) or \
                       (conditions["downConnects"] and conditions["rightDoesntConnect"]) or \
                       (conditions["upDoesntConnect"] and conditions["rightDoesntConnect"])
            elif orientation == "VB":
                return (conditions["downConnects"] and conditions["rightConnects"]) or \
                       (conditions["rightConnects"] and conditions["upDoesntConnect"] ) or \
                       (conditions["downConnects"] and conditions["leftDoesntConnect"]) or \
                       (conditions["upDoesntConnect"] and conditions["leftDoesntConnect"])
    
        return False
    
    
    def ligacaoPossibleActions(self, row: int, col: int):
        piece = self.getPiece(row, col)
        if piece.isLocked():
            return []
        
        return [(row, col, "LH", False), (row, col, "LV", False)]
    
    def fechoPossibleActions(self, row: int, col: int):
        leftPiece, rightPiece = self.adjacent_horizontal_values(row, col)
        upPiece, downPiece = self.adjacent_vertical_values(row, col)
        piece = self.getPiece(row, col) 
        
        actions = []
        
        if piece.isLocked():
            return actions  
        
        actions.extend([(row, col, "FB", False), (row, col, "FD", False), (row, col, "FE", False), (row, col, "FC", False)])
        
        if leftPiece != None and leftPiece.isLocked() and not piece.connectsWith(leftPiece, "left"):
            actions.remove((row, col, "FE", False))
        if rightPiece != None and rightPiece.isLocked() and not piece.connectsWith(rightPiece, "right"):
            actions.remove((row, col, "FD", False))
        if upPiece != None and upPiece.isLocked() and not piece.connectsWith(upPiece, "up"):
            actions.remove((row, col, "FC", False))
        if downPiece != None and downPiece.isLocked() and not piece.connectsWith(downPiece, "down"):
            actions.remove((row, col, "FB", False))
        
        return actions


    def bifurcationPossibleActions(self, row: int, col: int):
        
        
        leftPiece, rightPiece = self.adjacent_horizontal_values(row, col)
        upPiece, downPiece = self.adjacent_vertical_values(row, col)
        piece = self.getPiece(row, col)
        
        if piece.isLocked():
            return []
        
        if leftPiece.isLocked() and upPiece.isLocked and piece.connectsWith(leftPiece, "left") and piece.connectsWith(upPiece, "up"):
            return [(row, col, "BC", False), (row, col, "BE", False)]
        
        if leftPiece.isLocked() and downPiece.isLocked and piece.connectsWith(leftPiece, "left") and piece.connectsWith(downPiece, "down"):
            return [(row, col, "BB", False), (row, col, "BE", False)]
        
        if rightPiece.isLocked() and downPiece.isLocked and piece.connectsWith(rightPiece, "right") and piece.connectsWith(downPiece, "down"):
            return [(row, col, "BD", False), (row, col, "BB", False)]
        
        if rightPiece.isLocked() and upPiece.isLocked and piece.connectsWith(rightPiece, "right") and piece.connectsWith(upPiece, "up"):
            return [(row, col, "BD", False), (row, col, "BC", False)]

        if leftPiece != None and leftPiece.isLocked() and piece.connectsWith(leftPiece, "left"):
            
            return [(row, col, "BB", False), (row, col, "BC", False), (row, col, "BE", False)]
        if rightPiece != None and rightPiece.isLocked() and piece.connectsWith(rightPiece, "right"):
            
            return [(row, col, "BB", False), (row, col, "BD", False), (row, col, "BC", False)]
        if upPiece != None and upPiece.isLocked() and piece.connectsWith(upPiece, "up"):
            
            return [(row, col, "BC", False), (row, col, "BE", False), (row, col, "BD", False)]
        if downPiece != None and downPiece.isLocked() and piece.connectsWith(downPiece, "down"):
            
            return [(row, col, "BB", False), (row, col, "BE", False), (row, col, "BD", False)]

        return [(row, col, "BB", False), (row, col, "BC", False), (row, col, "BE", False), (row, col, "BD", False)]


    def voltaPossibleActions(self, row: int, col: int):
        leftPiece, rightPiece = self.adjacent_horizontal_values(row, col)
        upPiece, downPiece = self.adjacent_vertical_values(row, col)
        piece = self.getPiece(row, col)
        
        if piece.isLocked():
            return []

        if leftPiece != None and rightPiece != None:
            if (leftPiece.isLocked() and piece.connectsWith(leftPiece, "left")) or \
                (rightPiece.isLocked() and not piece.connectsWith(rightPiece, "right")):
                return [(row, col, "VE", False), (row, col, "VC", False)]
        
            if (rightPiece.isLocked() and piece.connectsWith(rightPiece, "right")) or \
                (leftPiece.isLocked() and not piece.connectsWith(leftPiece, "left")):
                return [(row, col, "VD", False), (row, col, "VB", False)]
        
        if upPiece != None and downPiece != None:
            if (upPiece.isLocked() and piece.connectsWith(upPiece, "up")) or \
                (downPiece.isLocked() and not piece.connectsWith(downPiece, "down")):
                return [(row, col, "VC", False), (row, col, "VD", False)]
            
            if (downPiece.isLocked() and piece.connectsWith(downPiece, "down")) or \
                (upPiece.isLocked() and not piece.connectsWith(upPiece, "up")):
                return [(row, col, "VE", False), (row, col, "VB", False)]
        
        return [(row, col, "VB", False), (row, col, "VD", False), (row, col, "VE", False), (row, col, "VC", False)]
   
    
    
class Piece:
    
    openTo = {
        "up": ["BC", "BE", "BD", "VC", "VD", "LV", "FC"],
        "down": ["BB", "BE", "BD", "VB", "VE", "LV", "FB"],
        "left": ["BB", "BC", "BE", "VC", "VE", "LH", "FE"],
        "right": ["BB", "BC", "BD", "VD", "VB", "LH", "FD"]
    }
        
    connectWith = {
        "up": openTo["down"],
        "down": openTo["up"],
        "left": openTo["right"],
        "right": openTo["left"]        
    }
        
    
    def __init__(self, orientation, connections=0, locked=False):
        self.orientation = orientation
        self.connections = connections
        self.locked = locked
        
    def setOrientation(self, orientation):
        self.orientation = orientation
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return self.orientation == value
        elif isinstance(value, Piece):
            return self.orientation == value.orientation
        return False
    
    def getOrientation(self):
        return self.orientation
    
    def lock(self):
        self.locked = True
    
    def isLocked(self):
        return self.locked
    
    def getConnections(self):
        return self.connections
    
    
    def updateConnections(self, value: int):
        self.connections = value
    
    def isAllConnected(self):
        numberOfConnections = { "B": 3, "V": 2, "F": 1, "L": 2 }
        type = self.orientation[0]
        return self.connections == numberOfConnections[type]
    
    def sameType(self, piece):
        return self.orientation[0] == piece.orientation[0]
    
    def type(self):
        return self.orientation[0]
    
    def isConnected(self, piece, direction):
        if self.orientation.startswith("F") and piece.orientation.startswith("F"):
            return False

        
        if self.orientation not in self.openTo[direction]:
            return False
        else:
            return piece.orientation in self.connectWith[direction]
        
    def connectsWith(self, piece, direction):
        if self.orientation.startswith("F") and piece.orientation.startswith("F"):
            return False
        
        return piece.orientation in self.connectWith[direction]
        
    def __str__(self):
        return self.orientation
    
    


class PipeMania(Problem):



    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        initial = PipeManiaState(board)
        self.visited = []
        super().__init__(initial)

    
    def isVisited(self, board: Board):
        for visited in self.visited:
            if visited.compare(board):
                return True
        return False

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        actions = []
        board = state.board
        
        if self.isVisited(board):
            print("State already visited\n")
            return actions
        
        self.visited.append(board)
        
        print("Expanding state: ", state.id, "\n")
        print(board)
        
        st = ""
        for row in range(len(state.board.grid)):
            for col in range(len(state.board.grid[row])):
                st += f"{state.board.grid[row][col].isLocked()}" + " "
            st += "\n"
        print(st)
        
        def distance_from_border(row, col):
            return min(row, col, len(board.grid) - 1 - row, len(board.grid[0]) - 1 - col)

        
        for row in range(len(state.board.grid)):
            for col in range(len(state.board.grid[row])):
                
                piece = board.getPiece(row, col)
                
                if board.checkIfLocks(row, col, piece.getOrientation()):
                    board.lockPiece(row, col)
                
                if piece.isLocked():
                    continue
                
                if piece.type() == "F":
                    if board.checkIfLocks(row, col, "FB"):
                        actions.append((row, col, "FB", True))
                        break
                    elif board.checkIfLocks(row, col, "FD"):
                        actions.append((row, col, "FD", True))
                        break
                    elif board.checkIfLocks(row, col, "FE"):
                        actions.append((row, col, "FE", True))
                        break
                    elif board.checkIfLocks(row, col, "FC"):
                        actions.append((row, col, "FC", True))
                        break
            
                elif piece.type() == "L":
                    if board.checkIfLocks(row, col, "LV"):
                        actions.append((row, col, "LV", True))
                        break   
                    elif board.checkIfLocks(row, col, "LH"):
                        actions.append((row, col, "LH", True))
                        break   
                    
                
                elif piece.type() == "B":
                    if board.checkIfLocks(row, col, "BB"):
                        actions.append((row, col, "BB", True))
                        break
                    elif board.checkIfLocks(row, col, "BC"):
                        actions.append((row, col, "BC", True))
                        break
                    elif board.checkIfLocks(row, col, "BD"):
                        actions.append((row, col, "BD", True))
                        break
                    elif board.checkIfLocks(row, col, "BE"):
                        actions.append((row, col, "BE", True))
                        break   
                    
                    
                elif piece.type() == "V":
                    if board.checkIfLocks(row, col, "VB"):
                        actions.append((row, col, "VB", True))
                        break
                    elif board.checkIfLocks(row, col, "VC"):
                        actions.append((row, col, "VC", True))
                        break
                    elif board.checkIfLocks(row, col, "VD"):
                        actions.append((row, col, "VD", True))
                        break
                    elif board.checkIfLocks(row, col, "VE"):
                        actions.append((row, col, "VE", True))
                        break
                        
                
                if (row, col, piece, False) in actions:
                    actions.remove((row, col, piece, False))
                if (row, col, piece, True) in actions:
                    actions.remove((row, col, piece, True))
                
            if actions != []:
                break
                    
        if actions == []:
            for row in range(len(state.board.grid)):
                for col in range(len(state.board.grid[row])):
                    piece = board.getPiece(row, col)
                    leftPiece, rightPiece = board.adjacent_horizontal_values(row, col)
                    upPiece, downPiece = board.adjacent_vertical_values(row, col)
                    
                    if (row, col) in state.moved:
                        continue
                    
                    if piece.isLocked():
                        continue
                    
                    functions = {
                        "F": board.fechoPossibleActions,
                        "L": board.ligacaoPossibleActions,
                        "B": board.bifurcationPossibleActions,
                        "V": board.voltaPossibleActions
                    }
                    
                    connects = {
                        "up": False,
                        "down": False,
                        "left": False,
                        "right": False
                    }
                    
                    if leftPiece != None:
                        possibleActions = functions[leftPiece.type()](row, col-1)
                        if possibleActions != [] and all([piece.connectsWith(Piece(orien[2]), "left") for orien in possibleActions]):
                            connects["left"] = True
                    if rightPiece != None:
                        possibleActions = functions[rightPiece.type()](row, col+1)
                        if possibleActions != [] and all([piece.connectsWith(Piece(orien[2]), "right") for orien in possibleActions]):
                            connects["right"] = True
                    if upPiece != None:
                        possibleActions = functions[upPiece.type()](row-1, col)
                        if possibleActions != [] and all([piece.connectsWith(Piece(orien[2]), "up") for orien in possibleActions]):
                            connects["up"] = True
                    if downPiece != None:
                        possibleActions = functions[downPiece.type()](row+1, col)
                        if possibleActions != [] and all([piece.connectsWith(Piece(orien[2]), "down") for orien in possibleActions]):
                            connects["down"] = True
                        
                    
                    
                    if piece.type() == "F":
                        if connects["up"]:
                            actions.append((row, col, "FC", True))
                            break
                        if connects["down"]:
                            actions.append((row, col, "FB", True))
                            break
                        if connects["left"]:
                            actions.append((row, col, "FE", True))
                            break
                        if connects["right"]:
                            actions.append((row, col, "FD", True))
                            break
                        
                        actions.extend(board.fechoPossibleActions(row, col))
                    
                    elif piece.type() == "L":
                        actions.extend(board.ligacaoPossibleActions(row, col))
                    
                    elif piece.type() == "B":
                        actions.extend(board.bifurcationPossibleActions(row, col))
                    
                    elif piece.type() == "V":
                        actions.extend(board.voltaPossibleActions(row, col))
                    
                    if (row, col, piece, False) in actions:
                        actions.remove((row, col, piece, False))
                    if (row, col, piece, True) in actions:
                        actions.remove((row, col, piece, True))
                
                if len(actions) == 1 and actions[0][3]:
                    break
       
        print("Actions: ", actions, "\n")
        return actions    
    


    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        board = state.board.copy()
        
        row, col, orientation, isLocked = action
        
        
        moved = copy.deepcopy(state.moved)
        moved.append((row, col))

        
        board.change_piece_orientation(row, col, orientation)
        board.updateConnections(row, col)
        board.updateConnections(row+1, col)
        board.updateConnections(row-1, col)
        board.updateConnections(row, col+1)
        board.updateConnections(row, col-1)
        if isLocked:
            board.lockPiece(row, col)
        
        
    
        
        return PipeManiaState(board, moved)


    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        visitedPos = []
        
        openings = {
            "FC": [(-1, 0)],
            "FD": [(0, 1)],
            "FE": [(0, -1)],
            "FB": [(1, 0)],
            "VC": [(-1, 0), (0, -1)],
            "VD": [(0, 1), (-1, 0)],
            "VE": [(0, -1), (1, 0)],
            "VB": [(1, 0), (0, 1)],
            "BB": [(1, 0), (0, 1), (0, -1)],
            "BC": [(0, 1), (0, -1), (-1, 0)],
            "BD": [(0, 1), (-1, 0), (1, 0)],
            "BE": [(0, -1), (1, 0), (-1, 0)],
            "LV": [(-1, 0), (1, 0)],
            "LH": [(0, -1), (0, 1)],	
        }
        
        for row in range(len(state.board.grid)):
            r = []
            for col in range(len(state.board.grid[row])):
                r.append(False)
                piece = state.board.getPiece(row, col)
                if not piece.isAllConnected():
                    return False
            visitedPos.append(r)
            
        stack = [(0, 0)]
        
        def in_bounds(x, y):
            return x >= 0 and x < len(state.board.grid) and y >= 0 and y < len(state.board.grid[x])
        
        while stack:
            x, y = stack.pop()
            if visitedPos[x][y]:
                continue
            visitedPos[x][y] = True
            
            piece = state.board.getPiece(x, y)   
            for xap, yap in openings[piece.getOrientation()]:
                nx, ny = x + xap, y + yap
                if in_bounds(nx, ny) and not visitedPos[nx][ny]:
                    stack.append((nx, ny))
                
        
        return all(all(row) for row in visitedPos)


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        state = node.state
        heuristic_value = 0
        for row in state.board.grid:
            for piece in row:
                heuristic_value += max(0, 2 - piece.connections)
        return heuristic_value

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
    print(goal_node.state.board)
    

    pass
