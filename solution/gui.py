import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5 import QtCore

class AnimatedComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Apply stylesheet and properties as needed
        self.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                color: #555;
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 10em; /* Minimum width */
                max-width: 20em; /* Maximum width */
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox:hover {
                border-color: #00aaff;
                background-color: #e0e0e0;
            }
            QComboBox::down-arrow {
                image: url(GUI/images/downArrow.png);
                width: 14px; /* Adjust the width of the arrow image */
                height: 14px; /* Adjust the height of the arrow image */
            }
            QComboBox QAbstractItemView {
                background-color: white; /* background of the dropdown list */
                border: 1px solid #ccc;
                selection-background-color: lightgray; /* selected item color */
            }
            """)
        
        # Add shadow effect to title
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setColor(Qt.black)
        shadow.setOffset(2, 2)
        self.setGraphicsEffect(shadow)

        




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PipeManiaSolver")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):

        fontId = QFontDatabase.addApplicationFont("GUI/fonts/OpenSans/OpenSans-Regular.ttf")
        if fontId == -1:
            print("Error loading font")
        else: 
            fontFamilies = QFontDatabase.applicationFontFamilies(fontId)[0]
            self.setFont(QFont(fontFamilies))


        self.title = QtWidgets.QLabel(self)
        self.title.setFont(self.font())
        self.title.setText("PipeMania AI Solver")
        self.title.setAlignment(Qt.AlignHCenter)

        # Apply stylesheet for modern look
        title_style = "font-size: 32px; color: #ffffff; padding: 10px;"
        self.title.setStyleSheet(title_style)


        central_widget = QtWidgets.QWidget(self)
        central_widget.setStyleSheet("background-color: #595959;")
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.addWidget(self.title)
        layout.setAlignment(self.title, Qt.AlignHCenter)

        self.initButtons(layout)
        self.animateForm()

    def initButtons(self, parent_layout):
        formLayout = QtWidgets.QFormLayout()

        self.algorithmComboBox = AnimatedComboBox()
        self.boardSizeComboBox = AnimatedComboBox()

        self.algorithmComboBox.addItems(["A*", "BFS", "DFS", "Greedy", "RBFS"])

        self.boardSizeComboBox.addItems(["2x2", "2x2 Version 2", "2x2 Version 3", "3x3", "3x3 Version 2", "3x3 Version 3", \
                                    "4x4", "5x5", "5x5 Version 2", "10x10", "10x10 V2", "10x10 V3", "10x10 V4", "10x10 V5", "10x10 V6", \
                                    "10x10 V7", "10x10 V8", "10x10 V9", "10x10 V10", "10x10 V11", "15x15", "20x20", "25x25", "30x30", "35x35", \
                                    "40x40", "45x45", "50x50"])
        
        # Set fixed width for combo boxes
        self.algorithmComboBox.setFixedWidth(50)  # Adjust width as needed
        self.boardSizeComboBox.setFixedWidth(50)  # Adjust width as needed

        # Add labels for the combo boxes
        algorithmLabel = QtWidgets.QLabel("Algorithm")
        boardSizeLabel = QtWidgets.QLabel("Board Size")

        # Style the labels
        labelStyleSheet = """
            QLabel {
                font-size: 14px;
                color: #00aaff;  
            }
        """

        algorithmLabel.setStyleSheet(labelStyleSheet)
        boardSizeLabel.setStyleSheet(labelStyleSheet)

        formLayout.addRow(algorithmLabel, self.algorithmComboBox)
        formLayout.addRow(boardSizeLabel, self.boardSizeComboBox)
     

        # Create the start button
        self.startButton = QtWidgets.QPushButton("Next")
        self.startButton.setFixedWidth(100)  # Adjust width as needed

        self.startButton.setStyleSheet("""
            QPushButton {
                border: 2px solid #8f8f91;
                border-radius: 10px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #f6f7fa, stop: 1 #dadbde);
                min-width: 80px;
                font-size: 18px;
                padding: 10px 20px;
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #dadbde, stop: 1 #f6f7fa);
            }
            QPushButton:hover {
                border: 2px solid #00aaff;
            }
            QPushButton:flat {
                border: none; /* no border for a flat push button */
            }
            QPushButton:default {
                border-color: navy; /* make the default button prominent */
            }
        """)

        # Add shadow effect to title
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setColor(Qt.black)
        shadow.setOffset(2, 2)
        self.startButton.setGraphicsEffect(shadow)

      

        # Create a new horizontal layout to place the form layout and the start button side by side
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addLayout(formLayout)
        hLayout.addWidget(self.startButton)
        hLayout.setAlignment(formLayout, QtCore.Qt.AlignVCenter)
        hLayout.setAlignment(self.startButton, QtCore.Qt.AlignVCenter)
        
        # Create a new vertical layout to center the horizontal layout
        centeredLayout = QtWidgets.QVBoxLayout()
        centeredLayout.addLayout(hLayout)
        centeredLayout.setAlignment(hLayout, QtCore.Qt.AlignCenter)
        centeredLayout.setAlignment(hLayout, QtCore.Qt.AlignTop)
        
        # Add the centered layout to the parent layout
        parent_layout.addLayout(centeredLayout)

    def setSignal(self, func):
        self.startButton.clicked.connect(func)


    def changeNextWindow(self):
        self.hide()
        self.nextWindow = BoardWindow(self.boardSizeComboBox.currentText(), self.algorithmComboBox.currentText())
        self.boardSize = self.boardSizeComboBox.currentText()
        self.algorithm = self.algorithmComboBox.currentText()
        self.nextWindow.show()
        return self.nextWindow

    def getFormValues(self):
        return self.boardSize, self.algorithm


    def animateForm(self):
        # Create animation for opacity
        self.opacityAnimation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.opacityAnimation.setDuration(500)
        self.opacityAnimation.setStartValue(0)
        self.opacityAnimation.setEndValue(1)
        
        # Create animation for scaling
        self.scaleAnimation = QtCore.QPropertyAnimation(self, b"geometry")
        self.scaleAnimation.setDuration(500)
        self.scaleAnimation.setEasingCurve(QtCore.QEasingCurve.OutBack)
        self.scaleAnimation.setStartValue(QtCore.QRect(100, 100, 0, 0))
        self.scaleAnimation.setEndValue(QtCore.QRect(100, 100, 800, 600))
        
        # Group animations together
        self.groupAnimation = QtCore.QParallelAnimationGroup()
        self.groupAnimation.addAnimation(self.opacityAnimation)
        self.groupAnimation.addAnimation(self.scaleAnimation)
        
        # Start animations
        self.groupAnimation.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

       


class BoardWindow(QtWidgets.QWidget):

    def __init__(self, board_size, algorithm):
        super().__init__()
        self.boardSize = board_size
        self.algorithm = algorithm
        self.initUI()
        self.loadBoard()

    def initUI(self):
        pass

    def loadBoard(self):
        
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

        path = f"../Tests/{files[self.boardSize]}"

        self.board = []
        with open(path, "r") as f:
            for line in f:
                row = line.strip().split()
                self.board.append(row)
        
        self.boardLayout = QtWidgets.QGridLayout(self)
        self.setLayout(self.boardLayout)

        num_rows = len(self.board)
        num_cols = len(self.board[0])

        window_width = 900
        window_height = 900
        self.setFixedSize(window_width, window_height)

        self.cell_width = window_width // num_cols
        self.cell_height = window_height // num_rows

        self.printBoard()

    def printBoard(self):

        image_map = {
            "LH": "images/LH.png",
            "LV": "images/LV.png",
            "BC": "images/BC.png",
            "BD": "images/BD.png",
            "BE": "images/BE.png",
            "BB": "images/BB.png",
            "FC": "images/FC.png",
            "FD": "images/FD.png",
            "FE": "images/FE.png",
            "FB": "images/FB.png",
            "VC": "images/VC.png",
            "VD": "images/VD.png",
            "VE": "images/VE.png",
            "VB": "images/VB.png",
        }


        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                label = QtWidgets.QLabel(self)
                im_path = image_map[cell]
                if im_path:
                    pixmap = QPixmap(im_path)
                    if not pixmap.isNull():
                        sclaed_pixmap = pixmap.scaled(self.cell_width, self.cell_height, aspectRatioMode=Qt.KeepAspectRatio)
                        label.setPixmap(sclaed_pixmap)
                        label.setAlignment(Qt.AlignCenter)  # Center-align the image within the QLabel
                        label.setFixedSize(self.cell_width, self.cell_height)  # Ensure fixed size for uniformity
                        label.setContentsMargins(0, 0, 0, 0)  # Remove any content margins
                    else:
                        print(f"Failed to load image for {cell} from {im_path}")
                self.boardLayout.addWidget(label, i, j)

        self.show()


    def startBoardAnimation(self):
        self.boardTimer = QTimer()
        self.boardTimer.timeout.connect(self.updateBoardAnimation)
        self.boardTimer.start(20)

    def updateBoardAnimation(self):
        if self.boardInex < len(self.boards):
            self.board = self.boards[self.boardInex]
            nb = []
            for row in self.board:
                nb.append([cell.str() for cell in row])
            self.board = nb
            self.refreshBoard()
            self.boardInex += 1  

    def updateBoard(self, boards):
        

        self.boards = boards
        self.boardInex = 0
        self.startBoardAnimation()


    def refreshBoard(self):
        while self.boardLayout.count():
            child = self.boardLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.printBoard()



def runGUI():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)


if __name__ == "__main__":
    runGUI()