from sys import stdin




class State:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = State.state_id
        State.state_id += 1


    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id
    

class Board:
    """ Representação interna de uma grelha de PipeMania. """

    grid = [] # Lista de listas de strings

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
        

    # TODO: outros metodos da classe

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



'''
class PipeMania(Problem):
    def __init__(self, initial_state: Board, goal_state: Board):
        """ O construtor especifica o estado inicial. """
        # TODO
        pass


    def actions(self, state: State):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass


    def result(self, state: State, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # TODO
        pass


    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
'''



# Teste da classe Board
board = Board.parse_instance()

print(board.adjacent_vertical_values(0, 0))
print(board.adjacent_horizontal_values(0, 0))
print(board.adjacent_vertical_values(1, 1))
print(board.adjacent_horizontal_values(1, 1))