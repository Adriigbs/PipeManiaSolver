# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
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

    @staticmethod
    def parse_instance():
        """Lê a instância do problema do standard input (stdin)
        e retorna uma instância da classe Board."""

        board = Board()

        lines = stdin.readlines()
        for line in lines:
            line = line.strip()
            board.grid.append(line.split())

        return board

    def change_piece_orientation(self, row: int, col: int, orientation: str):
        """Muda a orientação da peça na posição (row, col) para a
        orientação passada como argumento."""
        self.grid[row][col] = orientation



class PipeMania(Problem):

    

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        initial = PipeManiaState(board)
        super().__init__(initial)
        

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        actions = []

        for i in range(len(board.grid)):
            for j in range(len(board.grid[i])):
                piece = board.get_value(i, j)

                if i == 0 and j == 0:
                    if piece.startswith("F"):
                        actions.extend([(i, j, "FB"), (i, j, "FD")])
                    elif piece.startswith("V"):
                        actions.append((i, j, "VB"))
            
                elif i == 0 and j == len(board.grid[i]) - 1:
                    if piece.startswith("F"):
                        actions.extend([(i, j, "FB"), (i, j, "FE")])
                    elif piece.startswith("V"):
                        actions.append((i, j, "VE"))

                elif i == len(board.grid) - 1 and j == 0:
                    if piece.startswith("F"):
                        actions.extend([(i, j, "FC"), (i, j, "FD")])
                    elif piece.startswith("V"):
                        actions.append((i, j, "VD"))
            
                elif i == len(board.grid) - 1 and j == len(board.grid[i]) - 1:
                    if piece.startswith("F"):
                        actions.extend([(i, j, "FC"), (i, j, "FE")])
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
                        actions.extend([(i, j, "FB"), (i, j, "FD"), (i, j, "FE")])
                
                elif i == len(board.grid) - 1 and j != 0 and j != len(board.grid[i]) - 1:
                    if piece.startswith("B"):
                        actions.append((i, j, "BC"))
                    elif piece.startswith("L"):
                        actions.append((i, j, "LH"))
                    elif piece.startswith("V"):
                        actions.extend([(i, j, "VC"), (i, j, "VD")])
                    elif piece.startswith("F"):
                        actions.extend([(i, j, "FC"), (i, j, "FD"), (i, j, "FE")])

                elif j == 0 and i != 0 and i != len(board.grid) - 1:
                    if piece.startswith("B"):
                        actions.append((i, j, "BD"))
                    elif piece.startswith("L"):
                        actions.append((i, j, "LV"))
                    elif piece.startswith("V"):
                        actions.extend([(i, j, "VB"), (i, j, "VD")])
                    elif piece.startswith("F"):
                        actions.extend([(i, j, "FC"), (i, j, "FB"), (i, j, "FD")])         

                elif j == len(board.grid[i]) - 1 and i != 0 and i != len(board.grid) - 1:
                    if piece.startswith("B"):
                        actions.append((i, j, "BE"))
                    elif piece.startswith("L"):
                        actions.append((i, j, "LV"))
                    elif piece.startswith("V"):
                        actions.extend([(i, j, "VC"), (i, j, "VE")])
                    elif piece.startswith("F"):
                        actions.extend([(i, j, "FC"), (i, j, "FB"), (i, j, "FE")])           

        #TODO Restantes casos, talvez uma maneira de guardar no estado se uma peça está na posição final ou não.

        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

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


    pass
