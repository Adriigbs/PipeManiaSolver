import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from pipe import *
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
from pipe import PipeMania, Board


files = {
            "2x2": "test-01.txt",
            "2x2 Version 2": "test-02.txt",
            "2x2 Version 3": "test-03.txt",
            "3x3": "test-04.txt",
            "3x3 Version 2": "test-05.txt",
            "3x3 Version 3": "test-06.txt",
            "4x4": "test-07.txt",
            "5x5": "test-08.txt",
            "5x5 Version 2": "test-09.txt",
            "10x10": "test-10x10.txt",
            "10x10 V2": "test-10x10_1",
            "10x10 V3": "test-10x10_2",
            "10x10 V4": "test-10x10_3",
            "10x10 V5": "test-10x10_4",
            "10x10 V6": "test-10x10_5",
            "10x10 V7": "test-10x10_6",
            "10x10 V8": "test-10x10_7",
            "10x10 V9": "test-10x10_8",
            "10x10 V10": "test-10x10_9",
            "10x10 V11": "test-10x10_10",
            "15x15": "test-15x15.txt",
            "20x20": "test-20x20.txt",
            "25x25": "test-25x25.txt",
            "30x30": "test-30x30.txt",
            "35x35": "test-35x35.txt",
            "40x40": "test-40x40.txt",
            "45x45": "test-45x45.txt",
            "50x50": "test-50x50.txt"
        }


algorithmMap = {
    "A*": astar_search,
    "BFS": breadth_first_tree_search,
    "DFS": depth_first_tree_search,
    "Greedy": greedy_search,
    "RBFS": recursive_best_first_search,
}


def start():
    boardWindow = window.changeNextWindow()

    boardSize, algorithm = window.getFormValues()

    path = f"../Tests/{files[boardSize]}"

    board = Board.parse_instance(path)
    problem = PipeMania(board)

    goal_node = algorithmMap[algorithm](problem)
    boardWindow.updateBoard(problem.boards)


if __name__ == '__main__':


    app = QApplication(sys.argv)
    window = MainWindow()
    window.setSignal(start)
    window.show()

    sys.exit(app.exec_())