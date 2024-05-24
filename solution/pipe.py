
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
        self.removed = []
        PipeManiaState.state_id += 1
    
    def emptyRemoved(self):
        self.removed = []
        
    def addRemoved(self, row, col):
        self.removed.append((row, col))

    def __lt__(self, other):
        return self.id < other.id

    


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    grid = [] # Lista de listas de strings
    lastPieceMoved = None
   
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
        self.lastPieceMoved = (row, col)

    def lockPiece(self, row: int, col: int):
        """Bloqueia a peça na posição (row, col)."""
        self.grid[row][col].lock()
        
    def compare(self, other):
        """Compara o tabuleiro com outro tabuleiro passado como argumento."""
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if (self.grid[row][col] != other.grid[row][col]) or (self.grid[row][col].isLocked() != other.grid[row][col].isLocked()):
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
                return conditions["downConnects"] or \
                    ((conditions["upDoesntConnect"] or upPiece.type() == "F") and \
                    (conditions["leftDoesntConnect"] or leftPiece.type() == "F") and \
                    (conditions["rightDoesntConnect"] or rightPiece.type() == "F"))
            elif orientation == "FD":
                return conditions["rightConnects"] or \
                    ((conditions["downDoesntConnect"] or downPiece.type() == "F") and \
                    (conditions["upDoesntConnect"] or upPiece.type() == "F") and \
                    (conditions["leftDoesntConnect"] or leftPiece.type() == "F"))
            elif orientation == "FE":
                return conditions["leftConnects"] or \
                    ((conditions["downDoesntConnect"] or downPiece.type() == "F") and \
                     (conditions["upDoesntConnect"] or upPiece.type() == "F") and \
                     (conditions["rightDoesntConnect"] or rightPiece.type() == "F"))
            elif orientation == "FC":
                return conditions["upConnects"] or \
                    ((conditions["downDoesntConnect"] or downPiece.type() == "F") and \
                     (conditions["leftDoesntConnect"] or leftPiece.type() == "F") and \
                     (conditions["rightDoesntConnect"] or rightPiece.type() == "F"))
            
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
                        (conditions["downDoesntConnect"] and conditions["rightDoesntConnect"]) or \
                        ((conditions["upConnects"] and upPiece.type() == "F") and rightPiece.type() == "F") or \
                        ((conditions["leftConnects"] and leftPiece.type() == "F") and downPiece.type() == "F")
            elif orientation == "VD":
                return (conditions["upConnects"] and conditions["rightConnects"]) or \
                        (conditions["rightConnects"] and conditions["downDoesntConnect"]) or \
                        (conditions["upConnects"] and conditions["leftDoesntConnect"])  or \
                        (conditions["downDoesntConnect"]  and conditions["leftDoesntConnect"]) or \
                        ((conditions["upConnects"] and upPiece.type() == "F") and leftPiece.type() == "F") or \
                        ((conditions["rightConnects"] and rightPiece.type() == "F") and downPiece.type() == "F")
            elif orientation == "VE":
                return (conditions["downConnects"] and conditions["leftConnects"]) or \
                        (conditions["leftConnects"] and conditions["upDoesntConnect"]) or \
                        (conditions["downConnects"] and conditions["rightDoesntConnect"]) or \
                        (conditions["upDoesntConnect"] and conditions["rightDoesntConnect"]) or \
                        ((conditions["downConnects"] and downPiece.type() == "F") and rightPiece.type() == "F") or \
                        ((conditions["leftConnects"] and leftPiece.type() == "F") and upPiece.type() == "F")
            elif orientation == "VB":
                return (conditions["downConnects"] and conditions["rightConnects"]) or \
                        (conditions["rightConnects"] and conditions["upDoesntConnect"] ) or \
                        (conditions["downConnects"] and conditions["leftDoesntConnect"]) or \
                        (conditions["upDoesntConnect"] and conditions["leftDoesntConnect"]) or \
                        ((conditions["downConnects"] and downPiece.type() == "F") and leftPiece.type() == "F") or \
                        ((conditions["rightConnects"] and rightPiece.type() == "F") and upPiece.type() == "F")
    
        return False
    
    
    def ligacaoPossibleActions(self, row: int, col: int, moved=[]):
        piece = self.getPiece(row, col)
        if piece.isLocked() or (row, col) in moved:
            return []
        
        return [(row, col, "LH", False), (row, col, "LV", False)]
    
    def fechoPossibleActions(self, row: int, col: int, moved=[]):
        leftPiece, rightPiece = self.adjacent_horizontal_values(row, col)
        upPiece, downPiece = self.adjacent_vertical_values(row, col)
        piece = self.getPiece(row, col) 
        
        actions = []
        
        if piece.isLocked() or (row, col) in moved:
            return actions  
        
        actions.extend([(row, col, "FB", False), (row, col, "FD", False), (row, col, "FE", False), (row, col, "FC", False)])
        
        if leftPiece != None and ((leftPiece.isLocked() and not piece.connectsWith(leftPiece, "left")) or leftPiece.type() == "F"):
            actions.remove((row, col, "FE", False))
        if rightPiece != None and ((rightPiece.isLocked() and not piece.connectsWith(rightPiece, "right")) or rightPiece.type() == "F"):
            actions.remove((row, col, "FD", False))
        if upPiece != None and ((upPiece.isLocked() and not piece.connectsWith(upPiece, "up")) or upPiece.type() == "F"):
            actions.remove((row, col, "FC", False))
        if downPiece != None and ((downPiece.isLocked() and not piece.connectsWith(downPiece, "down")) or downPiece.type() == "F"):
            actions.remove((row, col, "FB", False))
        
        return actions


    def bifurcationPossibleActions(self, row: int, col: int, moved=[]):
        
        
        leftPiece, rightPiece = self.adjacent_horizontal_values(row, col)
        upPiece, downPiece = self.adjacent_vertical_values(row, col)
        piece = self.getPiece(row, col)
        
        if piece.isLocked() or (row, col) in moved:
            return []
        
        if leftPiece.isLocked() and upPiece.isLocked() and piece.connectsWith(leftPiece, "left") and piece.connectsWith(upPiece, "up"):
            return [(row, col, "BC", False), (row, col, "BE", False)]
        
        if leftPiece.isLocked() and downPiece.isLocked() and piece.connectsWith(leftPiece, "left") and piece.connectsWith(downPiece, "down"):
            return [(row, col, "BB", False), (row, col, "BE", False)]
        
        if rightPiece.isLocked() and downPiece.isLocked() and piece.connectsWith(rightPiece, "right") and piece.connectsWith(downPiece, "down"):
            return [(row, col, "BD", False), (row, col, "BB", False)]
        
        if rightPiece.isLocked() and upPiece.isLocked() and piece.connectsWith(rightPiece, "right") and piece.connectsWith(upPiece, "up"):
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


    def voltaPossibleActions(self, row: int, col: int, moved=[]):
        leftPiece, rightPiece = self.adjacent_horizontal_values(row, col)
        upPiece, downPiece = self.adjacent_vertical_values(row, col)
        piece = self.getPiece(row, col)
        
        if piece.isLocked() or (row, col) in moved:
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
    
    def getMaxConnections(self):
        type = self.orientation[0]
        return { "B": 3, "V": 2, "F": 1, "L": 2 }[type]
    
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
    
    def evaluateConnection(self, piece, direction):
        if self.isConnected(piece, direction):
            return True
        if self.openToNotOpen(piece, direction):
            return False
        if self.notOpenToOpen(piece, direction):
            return False
        if self.notOpenToNotOpen(piece, direction):
            return True

    def openToNotOpen(self, piece, direction):
        return self.orientation in self.openTo[direction] and piece.orientation not in self.connectWith[direction]
    
    def notOpenToOpen(self, piece, direction):
        return self.orientation not in self.openTo[direction] and piece.orientation in self.connectWith[direction]
    
    def notOpenToNotOpen(self, piece, direction):
        return self.orientation not in self.openTo[direction] and piece.orientation not in self.connectWith[direction]
        
    def __str__(self):
        return self.orientation
    
    


class PipeMania(Problem):



    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        initial = PipeManiaState(board)
        super().__init__(initial)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        actions = []
        lock_actions = []
        board = state.board

        def countLockedAround(row, col):
            leftPiece, rightPiece = board.adjacent_horizontal_values(row, col)
            upPiece, downPiece = board.adjacent_vertical_values(row, col)
            
            count = 0
            if leftPiece != None:
                if leftPiece.isLocked():
                    count += 1
                else:
                    l, u, d = board.adjacent_horizontal_values(row, col-1)[0], board.adjacent_vertical_values(row, col-1)[0], board.adjacent_vertical_values(row, col-1)[1]
                    if l != None and l.isLocked():
                        count += 0.5
                    if u != None and u.isLocked():
                        count += 0.5
                    if d != None and d.isLocked():
                        count += 0.5

            if rightPiece != None:
                if rightPiece.isLocked():
                    count += 1
                else:
                    r, u, d = board.adjacent_horizontal_values(row, col+1)[1], board.adjacent_vertical_values(row, col+1)[0], board.adjacent_vertical_values(row, col+1)[1]
                    if r != None and r.isLocked():
                        count += 0.5
                    if u != None and u.isLocked():
                        count += 0.5
                    if d != None and d.isLocked():
                        count += 0.5
                        
            if upPiece != None:
                if upPiece.isLocked():
                    count += 1
                else:
                    u, l, r = board.adjacent_vertical_values(row-1, col)[0], board.adjacent_horizontal_values(row-1, col)[0], board.adjacent_horizontal_values(row-1, col)[1]
                    if u != None and u.isLocked():
                        count += 0.5
                    if l != None and l.isLocked():
                        count += 0.5
                    if r != None and r.isLocked():
                        count += 0.5
            
            if downPiece != None:
                if downPiece.isLocked():
                    count += 1
                else:
                    d, l, r = board.adjacent_vertical_values(row+1, col)[1], board.adjacent_horizontal_values(row+1, col)[0], board.adjacent_horizontal_values(row+1, col)[1]
                    if d != None and d.isLocked():
                        count += 0.5
                    if l != None and l.isLocked():
                        count += 0.5
                    if r != None and r.isLocked():
                        count += 0.5
            
            return count

        def countConnectionsAround(row, col, orientation):
            leftPiece, rightPiece = board.adjacent_horizontal_values(row, col)
            upPiece, downPiece = board.adjacent_vertical_values(row, col)
            count = 0
            
            if leftPiece != None:
                if Piece(orientation).isConnected(leftPiece, "left"):
                    count += 1
                    l, u, d = board.adjacent_horizontal_values(row, col-1)[0], board.adjacent_vertical_values(row, col-1)[0], board.adjacent_vertical_values(row, col-1)[1]
                    if l != None and leftPiece.isConnected(l, "left") and l.isLocked():
                        count += 0.5
                    if u != None and leftPiece.isConnected(u, "up") and u.isLocked():
                        count += 0.5
                    if d != None and leftPiece.isConnected(d, "down") and d.isLocked():
                        count += 0.5
            if rightPiece != None:
                if Piece(orientation).isConnected(rightPiece, "right"):
                    count += 1
                    r, u, d = board.adjacent_horizontal_values(row, col+1)[1], board.adjacent_vertical_values(row, col+1)[0], board.adjacent_vertical_values(row, col+1)[1]
                    if r != None and rightPiece.isConnected(r, "right") and r.isLocked():
                        count += 0.5
                    if u != None and rightPiece.isConnected(u, "up") and u.isLocked():
                        count += 0.5
                    if d != None and rightPiece.isConnected(d, "down") and d.isLocked():
                        count += 0.5
            if upPiece != None:
                if Piece(orientation).isConnected(upPiece, "up"):
                    count += 1
                    u, l, r = board.adjacent_vertical_values(row-1, col)[0], board.adjacent_horizontal_values(row-1, col)[0], board.adjacent_horizontal_values(row-1, col)[1]
                    if u != None and upPiece.isConnected(u, "up") and u.isLocked():
                        count += 0.5
                    if l != None and upPiece.isConnected(l, "left") and l.isLocked():
                        count += 0.5
                    if r != None and upPiece.isConnected(r, "right") and r.isLocked():
                        count += 0.5
            if downPiece != None:
                if Piece(orientation).isConnected(downPiece, "down"):
                    count += 1
                    d, l, r = board.adjacent_vertical_values(row+1, col)[1], board.adjacent_horizontal_values(row+1, col)[0], board.adjacent_horizontal_values(row+1, col)[1]
                    if d != None and downPiece.isConnected(d, "down") and d.isLocked():
                        count += 0.5
                    if l != None and downPiece.isConnected(l, "left") and l.isLocked():
                        count += 0.5
                    if r != None and downPiece.isConnected(r, "right") and r.isLocked():
                        count += 0.5
            
            return count
        
      
        # FIRST STEP: Check for actions that are imediate and lock the piece, return all of them so that they can be all applied at the same time
        # This makes the algorithm much faster 
        la = []
        for row in range(len(state.board.grid)):
            for col in range(len(state.board.grid[row])):
                
                piece = board.getPiece(row, col)
                
                # Lock pieces that might have not been locked yet
                if board.checkIfLocks(row, col, piece.getOrientation()):
                    board.lockPiece(row, col)
                
                # If the piece is locked, we can't do anything with it
                if piece.isLocked():
                    continue
                
                # Check for locked pieces if the piece is a fecho
                if piece.type() == "F":
                    if board.checkIfLocks(row, col, "FB"):
                        la.append((row, col, "FB", True))
                        continue
                    elif board.checkIfLocks(row, col, "FD"):
                        la.append((row, col, "FD", True))
                        continue
                    elif board.checkIfLocks(row, col, "FE"):
                        la.append((row, col, "FE", True))
                        continue
                    elif board.checkIfLocks(row, col, "FC"):
                        la.append((row, col, "FC", True))
                        continue
            
                # Check for locked pieces if the piece is a ligacao
                elif piece.type() == "L":
                    if board.checkIfLocks(row, col, "LV"):
                        la.append((row, col, "LV", True))
                        continue
                    elif board.checkIfLocks(row, col, "LH"):
                        la.append((row, col, "LH", True))
                        continue
                
                # Check for locked pieces if the piece is a bifurcation
                elif piece.type() == "B":
                    if board.checkIfLocks(row, col, "BB"):
                        la.append((row, col, "BB", True))
                        continue
                    elif board.checkIfLocks(row, col, "BC"):
                        la.append((row, col, "BC", True))
                        continue
                    elif board.checkIfLocks(row, col, "BD"):
                        la.append((row, col, "BD", True))
                        continue
                    elif board.checkIfLocks(row, col, "BE"):
                        la.append((row, col, "BE", True))
                        continue
                    
                # Check for locked pieces if the piece is a volta
                elif piece.type() == "V":
                    if board.checkIfLocks(row, col, "VB"):
                        la.append((row, col, "VB", True))
                        continue
                    elif board.checkIfLocks(row, col, "VC"):
                        la.append((row, col, "VC", True))
                        continue
                    elif board.checkIfLocks(row, col, "VD"):
                        la.append((row, col, "VD", True))
                        continue
                    elif board.checkIfLocks(row, col, "VE"):
                        la.append((row, col, "VE", True))
                        continue
                        
                # Remove the action if it is the same as the current  piece
                if (row, col, piece, True) in la:
                    la.remove((row, col, piece, True))
                
        # If there are locked pieces, return all locked pieces
        if la != []:
            actions.append([la])
            return actions
        
        # If there are no locked pieces, we can proceed to the next step
        # Check for possible actions      
        if la == []:
         
            finalLocked = []
            
            for row in range(len(state.board.grid)):
                for col in range(len(state.board.grid[row])):
                    piece = board.getPiece(row, col)
                    leftPiece, rightPiece = board.adjacent_horizontal_values(row, col)
                    upPiece, downPiece = board.adjacent_vertical_values(row, col)
                    
                    if piece.isLocked():
                        continue
                        
                    if state.moved != [] and (row, col) == state.moved[-1]:
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
                    
                    notConnects = {
                        "up": False,
                        "down": False,
                        "left": False,
                        "right": False
                    }
                    
                    if leftPiece != None:
                        possibleActions = functions[leftPiece.type()](row, col-1)
                        if possibleActions != [] and all([piece.connectsWith(Piece(orien[2]), "left") for orien in possibleActions]):
                            connects["left"] = True
                        elif possibleActions != []:
                            aux = []
                            for action in possibleActions:
                                if not piece.connectsWith(Piece(action[2]), "left"):
                                    aux.append(True)
                                else:
                                    aux.append(False)
                            if all(aux):
                                notConnects["left"] = True
                    if rightPiece != None:
                        possibleActions = functions[rightPiece.type()](row, col+1)
                        if possibleActions != [] and all([piece.connectsWith(Piece(orien[2]), "right") for orien in possibleActions]):
                            connects["right"] = True
                        elif possibleActions != []:
                            aux = []
                            for action in possibleActions:
                                if not piece.connectsWith(Piece(action[2]), "right"):
                                    aux.append(True)
                                else:
                                    aux.append(False)
                            if all(aux):
                                notConnects["right"] = True
                        
                    if upPiece != None:
                        possibleActions = functions[upPiece.type()](row-1, col)
                        if possibleActions != [] and all([piece.connectsWith(Piece(orien[2]), "up") for orien in possibleActions]):
                            connects["up"] = True
                        elif possibleActions != []:
                            aux = []
                            for action in possibleActions:
                                if not piece.connectsWith(Piece(action[2]), "up"):
                                    aux.append(True)
                                else:
                                    aux.append(False)
                            if all(aux):
                                notConnects["up"] = True
                    if downPiece != None:
                        possibleActions = functions[downPiece.type()](row+1, col)
                        if possibleActions != [] and all([piece.connectsWith(Piece(orien[2]), "down") for orien in possibleActions]):
                            connects["down"] = True
                        elif possibleActions != []:
                            aux = []
                            for action in possibleActions:
                                if not piece.connectsWith(Piece(action[2]), "down"):
                                    aux.append(True)
                                else:
                                    aux.append(False)
                            if all(aux):
                                notConnects["down"] = True
                        
                    if piece.type() == "F":
                        if connects["up"]:
                            actions.append((row, col, "FC", True))
                            continue
                        if connects["down"]:
                            actions.append((row, col, "FB", True))
                            continue
                        if connects["left"]:
                            actions.append((row, col, "FE", True))
                            continue
                        if connects["right"]:
                            actions.append((row, col, "FD", True))
                            continue
                        
                        actions.extend(board.fechoPossibleActions(row, col, state.moved))
                    
                    elif piece.type() == "L":
                        if connects["up"] or connects["down"] or notConnects["left"] or notConnects["right"]:
                            lock_actions.append((row, col, "LV", True))
                            continue
                        if connects["left"] or connects["right"] or notConnects["up"] or notConnects["down"]:
                            lock_actions.append((row, col, "LH", True))
                            continue

                        
                        actions.extend(board.ligacaoPossibleActions(row, col, state.moved))
                    
                    elif piece.type() == "B":
                        if (connects["up"] and connects["left"] and connects["right"]) or notConnects["down"]:
                            lock_actions.append((row, col, "BC", True))
                            continue
                        if (connects["down"] and connects["left"] and connects["right"]) or notConnects["up"]:
                            lock_actions.append((row, col, "BB", True))
                            continue
                        if (connects["right"] and connects["up"] and connects["down"]) or notConnects["left"]:
                            lock_actions.append((row, col, "BD", True))
                            continue
                        if (connects["left"] and connects["up"] and connects["down"]) or notConnects["right"]:
                            lock_actions.append((row, col, "BE", True))
                            continue
                        
                        actions.extend(board.bifurcationPossibleActions(row, col, state.moved))
                    
                    elif piece.type() == "V":
                        if (connects["up"] and connects["left"]) or \
                            (connects["left"] and notConnects["down"]) or \
                            (connects["up"] and notConnects["right"]) or \
                            (notConnects["down"] and notConnects["right"]):
                            lock_actions.append((row, col, "VC", True))
                            continue
                        if (connects["up"] and connects["right"]) or \
                            (connects["right"] and notConnects["down"]) or \
                            (connects["up"] and notConnects["left"]) or \
                            (notConnects["down"] and notConnects["left"]):
                            lock_actions.append((row, col, "VD", True))
                            continue
                        if (connects["down"] and connects["left"]) or \
                            (connects["left"] and notConnects["up"]) or \
                            (connects["down"] and notConnects["right"]) or \
                            (notConnects["up"] and notConnects["right"]):
                            lock_actions.append((row, col, "VE", True))
                            continue
                        if (connects["down"] and connects["right"]) or \
                            (connects["right"] and notConnects["up"]) or \
                            (connects["down"] and notConnects["left"]) or \
                            (notConnects["up"] and notConnects["left"]):
                            lock_actions.append((row, col, "VB", True))
                            continue
                        actions.extend(board.voltaPossibleActions(row, col, state.moved))
                    
                  
                    if (row, col, piece, True) in actions:
                        actions.remove((row, col, piece, True))

                # If there are locked pieces, return all the locked pieces so that they are all applied to the same state for more efficiency
                if lock_actions != []:
                    finalLocked.append([lock_actions])
                    return finalLocked
                
        
            if actions != []:
                # Sort actions by the number of locked pieces around the piece
                actions.sort(key=lambda x: countLockedAround(x[0], x[1]))
                ac = []
                state.emptyRemoved()    # Empty the list of removed pieces from the previous state
                
                # Remove actions that are not possible to connect to the adjacent pieces so that useless actions are not taken
                actions = [action for action in actions if self.removeAction(state, action[0], action[1], action[2])]
                
                # If a position where actions were removed, there is no meaning in continuing the search in that branch
                # Return an empty list of actions so that the search goes back to the previous state
                for row, col in state.removed:
                    leftPiece, rightPiece = board.adjacent_horizontal_values(row, col)
                    upPiece, downPiece = board.adjacent_vertical_values(row, col)
                    if ((leftPiece == None or leftPiece.isLocked()) or (row, col-1) in self.checkAdjacents(state, row, col)[1]) and \
                        ((rightPiece == None or rightPiece.isLocked()) or (row, col+1) in self.checkAdjacents(state, row, col)[1]) and \
                        ((upPiece == None or upPiece.isLocked()) or (row-1, col) in self.checkAdjacents(state, row, col)[1]) and \
                        ((downPiece == None or downPiece.isLocked()) or (row+1, col) in self.checkAdjacents(state, row, col)[1]):
                        
                        inActions = False
                        for action in actions:
                            if row == action[0] and col == action[1]:
                                inActions = True
                                break
                        
                        if not inActions:
                            return []


                adjacentActions = []
                
                # Filter actions for actions that are adjacent to the last piece moved so that the search is more efficient
                if state.moved != []:
                    adjacentActions = [action for action in actions if self.isAdjacent(action[0], action[1], state.moved[-1][0], state.moved[-1][1])]
                
                # Add only the actions of one position so that the search is more efficient
                # This doesn't create useless branches in the search tree
                if adjacentActions != []:    
                    row, col = adjacentActions[-1][0], adjacentActions[-1][1]
                    for action in adjacentActions:
                        if row == action[0] and col == action[1]:
                            ac.append(action)
                
                elif actions != []:
                    row, col = actions[-1][0], actions[-1][1]
                    for action in actions:
                        if row == action[0] and col == action[1]:
                            ac.append(action)
                
                
                # Sort the actions by the number of connections around the piece
                ac.sort(key=lambda x: countConnectionsAround(x[0], x[1], x[2]))
                return ac

        # Return empty actions
        return actions 
    
    
    def isAdjacent(self, r1, c1, r2, c2):
        """Returns if two pieces are adjacent."""
        return (abs(r1 - r2) == 1 and c1 == c2) or (abs(c1 - c2) == 1 and r1 == r2)
    
    def checkAdjacents(self, state, row, col):
        """Check all adjecent pieces to the piece in the position (row, col) and returns if they are adjecent and a list of the adjecent pieces."""
        adjacent = []
        areAdjecent = False
        if state.moved != []:
            for r, c in state.moved:
                if self.isAdjacent(row, col, r, c):
                    areAdjecent = True
                    adjacent.append((r, c))
        
        return (areAdjecent, adjacent)
    
    
    def removeAction(self, state, row: int, col: int, orientation: str):
        """Removes a piece from the available actions if it is not possible to connect it to the adjacent pieces
        that were previously moved in the current branch of the tree."""
        board = state.board

        directions = {
            (0, 1): "right",
            (0, -1): "left",
            (1, 0): "down",
            (-1, 0): "up"
        }
        
        adjacent = self.checkAdjacents(state, row, col)
        
        if adjacent[0]:
            conns = []
            for r, c in adjacent[1]:
                conns.append(Piece(orientation).evaluateConnection(board.getPiece(r, c), directions[(r-row, c-col)]))
            if all(conns):
                return True
            state.addRemoved(row, col)
            return False
        
        return True
                
    
    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        board = state.board.copy()
        acList = []
        
        # Verifica se recebeu uma ação que não dá lock ou uma lista de ações imeadiatas 
        if isinstance(action[0], list):
            acList = action[0]
        else:
            acList.append(action)
            
        for move in acList:
            row, col, orientation, isLocked = move


            # Add to moved list if it is not locked so that a piece is not moved twice
            moved = copy.deepcopy(state.moved)
            if not isLocked:
                moved.append((row, col))

            # Apply the action to the board
            board.change_piece_orientation(row, col, orientation)
            leftPiece, rightPiece = board.adjacent_horizontal_values(row, col)
            upPiece, downPiece = board.adjacent_vertical_values(row, col)
            
            # Update connections of the adjecent pieces
            board.updateConnections(row, col)
            board.updateConnections(row+1, col)
            board.updateConnections(row-1, col)
            board.updateConnections(row, col+1)
            board.updateConnections(row, col-1)
            
            # If piece is set to be locked, lock it and lock the adjecent pieces if they are locked
            if isLocked:
                board.lockPiece(row, col)
                if upPiece != None and board.checkIfLocks(row-1, col, upPiece.getOrientation()):
                    board.lockPiece(row-1, col)
                if downPiece != None and board.checkIfLocks(row+1, col, downPiece.getOrientation()):
                    board.lockPiece(row+1, col)
                if leftPiece != None and board.checkIfLocks(row, col-1, leftPiece.getOrientation()):
                    board.lockPiece(row, col-1)
                if rightPiece != None and board.checkIfLocks(row, col+1, rightPiece.getOrientation()):
                    board.lockPiece(row, col+1)

        
        return PipeManiaState(board, moved)

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        visitedPos = []
        
        # Sides to where a piece can connect so that dfs can follow all paths
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
        
        
        # Check if all pieces have all connections
        for row in range(len(state.board.grid)):
            r = []
            for col in range(len(state.board.grid[row])):
                r.append(False)
                piece = state.board.getPiece(row, col)
                if not piece.isAllConnected():
                    return False
            visitedPos.append(r)
           
           
        def in_bounds(x, y):
            return x >= 0 and x < len(state.board.grid) and y >= 0 and y < len(state.board.grid[x])
            
            
        # If all pieces are connected, check if there is an island in the board
        stack = [(0, 0)]        
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
                
        # If there is an island, return False
        # If there is no island, return True and goal is reached
        return all(all(row) for row in visitedPos)


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        state = node.state
        heuristicScore = 0    
        
        # Sides to where a piece can connect so that dfs can follow all paths
        openings = {
            "FC": [(-1, 0)],                        # Up
            "FD": [(0, 1)],                         # Right
            "FE": [(0, -1)],                        # Left              
            "FB": [(1, 0)],                         # Down
            "VC": [(-1, 0), (0, -1)],               # Up, Left
            "VD": [(0, 1), (-1, 0)],                # Right, Up
            "VE": [(0, -1), (1, 0)],                # Left, Down
            "VB": [(1, 0), (0, 1)],                 # Down, Right
            "BB": [(1, 0), (0, 1), (0, -1)],        # Down, Right, Left
            "BC": [(0, 1), (0, -1), (-1, 0)],       # Right, Left, Up
            "BD": [(0, 1), (-1, 0), (1, 0)],        # Right, Up, Down
            "BE": [(0, -1), (1, 0), (-1, 0)],       # Left, Down, Up
            "LV": [(-1, 0), (1, 0)],                # Up, Down
            "LH": [(0, -1), (0, 1)],	            # Left, Right
        }
        
        # Check if a coordinate is inside the board
        def in_bounds(x, y):
            return x >= 0 and x < len(state.board.grid) and y >= 0 and y < len(state.board.grid[x])   
        
        # Checks if there is an island in the board starting from the given position
        def checkIslands(row, col):
            visitedPos = []
            
            stack = [(row, col)]
            while stack:
                x, y = stack.pop()
                if not state.board.getPiece(x, y).isAllConnected():
                    return False
                visitedPos.append((x, y))    
                
                for xap, yap in openings[state.board.getPiece(x, y).getOrientation()]:
                    nx, ny = x + xap, y + yap
                    if in_bounds(nx, ny) and (nx, ny) not in visitedPos:
                        stack.append((nx, ny))
                
            if len(visitedPos) != (len(state.board.grid[0]) * len(state.board.grid)):
                return True
            
        for row in range(len(state.board.grid)):
            for col in range(len(state.board.grid[row])):
                piece = state.board.getPiece(row, col)
                
                if piece.isLocked():
                    continue
                
                heuristicScore += piece.getConnections() 
                heuristicScore -= (piece.getMaxConnections() - piece.getConnections()) * 0.2
                
                if not piece.isAllConnected():
                    heuristicScore -= 0.2

                if checkIslands(row, col):
                    heuristicScore -= 1000
  
        return - heuristicScore
        

if __name__ == "__main__":

    board = Board.parse_instance()
    problem = PipeMania(board)

    goal_node = depth_first_tree_search(problem)

    print(goal_node.state.board)
    

    pass
