import sys
import chess
import AI

from PyQt5.QtCore import Qt, QPoint 
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel 
from PyQt5.QtWidgets import QVBoxLayout ,QPushButton , QHBoxLayout ,QListWidget,QDesktopWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets  import QApplication
from PyQt5.QtCore import QDateTime



class GameMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle("Game Menu")
        self.setFixedSize(400, 150)
        self.setStyleSheet("background-color: #AFD6C5;")

        
        startb_button = QPushButton("Start Game As Black", self)
        startb_button.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        startw_button = QPushButton("Start Game As White", self)
        startw_button.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        close_button = QPushButton("Close Game", self)
        close_button.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        about_button = QPushButton("About Us", self)
        about_button.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        
        startb_button.clicked.connect(self.open_window_asb)
        startw_button.clicked.connect(self.open_window_asw)
        close_button.clicked.connect(self.close_window)
        about_button.clicked.connect(self.open_aboutus)
        self.setWindowFlag(Qt.FramelessWindowHint)

        
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 10, 0, 10)
        vbox.addWidget(QLabel("Game Menu", self))
        vbox.addStretch(1)
        vbox.addWidget(startb_button)
        vbox.addSpacing(10)
        vbox.addWidget(startw_button)
        vbox.addSpacing(10)
        vbox.addWidget(about_button)
        vbox.addStretch(1)
        vbox.addSpacing(10)
        vbox.addWidget(close_button)
        vbox.addStretch(1)
        
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(10, 0, 10, 0)
        hbox.addLayout(vbox)

        self.setLayout(hbox)


    def open_window_asb(self):
        self.window = ChessWindow("b")
        self.window.show()
        self.close()

    def open_window_asw(self):
        self.window = ChessWindow("w")
        self.window.show()
        self.close()

    def open_aboutus(self):
        self.window = AboutUs()
        self.window.show()
        self.close()
    
    def close_window(self):
        sys.exit()


        

class ChessBoardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(900, 605)
        self.setWindowFlag(Qt.FramelessWindowHint)
        

        self.setFocusPolicy(Qt.StrongFocus)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(610, 0, 300, 400)

        unselect_button = QPushButton("Unselect Move", self)
        unselect_button.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        unselect_button.setGeometry(610, 410, 300, 40)
        unselect_button.clicked.connect(self.unselect_move)
        
        undo_button = QPushButton("Undo Move", self)
        undo_button.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        undo_button.setGeometry(610, 460, 300, 40)
        undo_button.clicked.connect(self.undo_move)

        save_button = QPushButton("Save Current Notation", self)
        save_button.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        save_button.setGeometry(610, 510, 300, 40)
        save_button.clicked.connect(self.save_notation)

        close_button = QPushButton("Close Game", self)
        close_button.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        close_button.setGeometry(610, 560, 300, 40)
        close_button.clicked.connect(self.close_window)

        
        self.pieces = {
            "P": QPixmap("Images/wP.png"),
            "N": QPixmap("Images/wN.png"),
            "B": QPixmap("Images/wB.png"),
            "R": QPixmap("Images/wR.png"),
            "Q": QPixmap("Images/wQ.png"),
            "K": QPixmap("Images/wK.png"),
            "p": QPixmap("Images/bP.png"),
            "n": QPixmap("Images/bN.png"),
            "b": QPixmap("Images/bB.png"),
            "r": QPixmap("Images/bR.png"),
            "q": QPixmap("Images/bQ.png"),
            "k": QPixmap("Images/bK.png"),
        }

        # Create a chess board and set the initial position
        self.board = chess.Board()

        # Initialize variables for storing the source and destination squares
        # for the current move
        self.src_square = None
        self.dst_square = None

        self.user="w"
        self.turn = "w"; 
    
    def undo_move(self):
        if self.board.move_stack:
            self.board.pop()
            self.list_widget.takeItem(self.list_widget.count()-1)
            self.turn = "w" if self.turn == "b" else "b"
            self.update()
            
    def unselect_move(self):
        self.src_square = None
        self.dst_square = None
        self.update()
    
    def save_notation(self):
        current_datetime = QDateTime.currentDateTime()
        filename = current_datetime.toString("yyyyMMdd-hhmmss") + ".txt"
        with open(filename, "w") as file:
            for index in range(self.list_widget.count()):
                item = self.list_widget.item(index)
                text = item.text()
                file.write(text + "\n")

        print("Notation saved to:", filename)

        
    def close_window(self):
        sys.exit()      
    
    

    def paintEvent(self, event):
     qp = QPainter(self)

     if(self.user=="w"):          
          # Draw the chess board starting from the bottom row and working upwards
        for r in range(7, -1, -1):
         for c in range(8):
            color = QColor(245, 222, 179) if (r + c) % 2 == 0 else QColor(0, 0, 0)
            qp.setBrush(color)
            qp.drawRect(c * 75, r * 75, 75, 75)

    # Draw the chess pieces starting from the bottom row and inverting the row and column indices
        for r in range(7, -1, -1):
         for c in range(8):
            piece = self.board.piece_at(8 * (7 - r) + c)
            if piece:
                qp.drawPixmap(c * 75, r * 75, 75, 75, self.pieces[piece.symbol()])

        
         # Highlight the source and destination squares for the current move
        if self.src_square:
         qp.setBrush(QColor(0, 255, 0, 100))
         qp.drawRect(self.src_square[1] * 75, (7 - self.src_square[0]) * 75, 75, 75)
        if self.dst_square:
         qp.setBrush(QColor(255, 0, 0, 100))
         qp.drawRect(self.dst_square[1] * 75, (7 - self.dst_square[0]) * 75, 75, 75)
      
     else:
         for r in range(8):
            for c in range(8):
                color = QColor(245, 222, 179) if (r + c) % 2 == 0 else QColor(0, 0, 0)
                qp.setBrush(color)
                qp.drawRect(c * 75, r * 75, 75, 75)

        # Draw the chess pieces
         for r in range(8):
            for c in range(8):
                piece = self.board.piece_at(8 * r + c)
                if piece:
                    qp.drawPixmap(c * 75, r * 75, 75, 75, self.pieces[piece.symbol()])
         if self.src_square:
           qp.setBrush(QColor(0, 255, 0, 100))
           qp.drawRect((self.src_square[1]) * 75, (self.src_square[0]) * 75, 75, 75)
         if self.dst_square:
           qp.setBrush(QColor(255, 0, 0, 100))
           qp.drawRect((self.dst_square[1]) * 75, (self.dst_square[0]) * 75, 75, 75)
    
     
                    
 







class ChessWindow(QMainWindow):
    def __init__(self,color):
        super().__init__()

        screen_geometry = QDesktopWidget().screenGeometry()

        center_point = screen_geometry.center()

        frame_geometry = self.frameGeometry()
        frame_size = frame_geometry.size()

        offset = -100
        window_position = center_point - QPoint((frame_size.width() / 2)- offset, (frame_size.height() / 2)-offset)

        self.move(window_position)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Chess")
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(QHBoxLayout())
        
        
        self.chess_board = ChessBoardWidget(self)
        self.chess_board.mousePressEvent = self.on_mouse_press
        self.chess_board.keyPressEvent = self.on_key_press
        self.centralWidget().layout().addWidget(self.chess_board)
        self.chess_board.user=color
        print(self.chess_board.user)

        

        if self.chess_board.user == "b":  # Assuming user is playing as white
            self.madeMoveAI()
            self.chess_board.turn = "w"
            self.getNotation()
          
    def convertUCIToAlgebraic(self, uci):
     file_map = {
         'a': '1',
         'b': '2',
         'c': '3',
         'd': '4',
         'e': '5',
         'f': '6',
         'g': '7',
         'h': '8'
     }
     rank_map = {
         '1': 'a',
         '2': 'b',
         '3': 'c',
         '4': 'd',
         '5': 'e',
         '6': 'f',
         '7': 'g',
         '8': 'h'
     }

     source_square = uci[:2]
     target_square = uci[2:]
     source_file = file_map[source_square[0]]
     source_rank = source_square[1]
     target_file = file_map[target_square[0]]
     target_rank = target_square[1]
     algebraic_notation = rank_map[source_rank] + source_file + rank_map[target_rank] + target_file
 
     return algebraic_notation
    
    
        
    def getNotation(self):
     if self.chess_board.board.move_stack:
        last_move = self.chess_board.board.peek()
        notation = last_move.uci()
        algebraic_notation = self.convertUCIToAlgebraic(notation)
        last_item = self.chess_board.list_widget.item(self.chess_board.list_widget.count() - 1)

        if last_item:
            last_notations = last_item.text().split()
            print(last_notations)
            result =""
            if len(last_notations) % 2 == 0:
                move_number = str(len(last_notations) // 2 + 1) + "."
                result = move_number + algebraic_notation
            else :
                result = algebraic_notation
            last_notations.append(result)
            updated_notation = " ".join(last_notations)
            self.chess_board.list_widget.item(self.chess_board.list_widget.count() - 1).setText(updated_notation)
        else:
            self.chess_board.list_widget.addItem("1." + algebraic_notation)
    
    def undoLastNotation(self):
     self.chess_board.list_widget.takeItem(self.chess_board.list_widget.count() - 1)

    def pushMove(self,move):
     self.chess_board.board.push(move)
     self.chess_board.src_square = None
     self.chess_board.dst_square = None

    def madeMoveAI(self):
        aimove = AI.GetAiMove(self.chess_board.board,1)
        self.chess_board.board.push(aimove)
        self.chess_board.src_square = None
        self.chess_board.dst_square = None
    
    
   

    def on_mouse_press(self, event):
      if(self.chess_board.user=="w"):
        # Convert the mouse position to a square on the chess board
        row = 7 - event.pos().y() // 75
        col = event.pos().x() // 75
      else:
        row = event.pos().y() // 75
        col = event.pos().x() // 75
    
        # If no source square has been selected, set it to the current square
      if not self.chess_board.src_square:
            self.chess_board.src_square = (row, col)
            self.chess_board.update()
        # Otherwise, set the destination square and try to make the move
      else:
            self.chess_board.dst_square = (row, col)
            self.chess_board.update()
            move = chess.Move(8 * self.chess_board.src_square[0] + self.chess_board.src_square[1],
                              8 * self.chess_board.dst_square[0] + self.chess_board.dst_square[1])
            
            if self.chess_board.board.is_legal(move):
                self.pushMove(move)
                self.getNotation()
                self.chess_board.update()
                
                if(self.chess_board.turn == "w"):
                 self.chess_board.turn="b"
                else:
                 self.chess_board.turn="w"
                 print(self.chess_board.turn)
                
                self.madeMoveAI()
                self.getNotation()
                self.chess_board.update()

                if(self.chess_board.turn == "w"):
                 self.chess_board.turn="b"
                else:
                 self.chess_board.turn="w"
                 print(self.chess_board.turn)
            else:
                # Display an error message or take some other action
                pass
      
      

    
    def on_key_press(self, event):
        if event.key() == Qt.Key_P:
            self.chess_board.src_square = None
            self.chess_board.dst_square = None
            self.chess_board.update()
        elif event.key() == Qt.Key_U:
             self.chess_board.board.pop()
             self.chess_board.update()
             self.undoLastNotation()
        else:
           # Call th e base class implementation to handle other keys
            super().keyPressEvent(event)

class AboutUs(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        self.setWindowTitle("About Us")
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: #AFD6C5;")
        self.setWindowFlag(Qt.FramelessWindowHint)
        coder_label = QLabel()
        coder_label.setText("Programmer : Emir Görkem Özdemir")
        manager_label = QLabel()
        manager_label.setText("Project Manager : Çağdaş Allahverdi")
        designer_label = QLabel()
        designer_label.setText("Designer : Çağatay Toksözoğlu")
        close_button = QPushButton("Close Game", self)
        close_button.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        close_button.clicked.connect(self.openGameMenu)
        
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 10, 0, 10)
        vbox.addWidget(QLabel("About Us", self))
        vbox.addStretch(1)
        vbox.addWidget(coder_label)
        vbox.addSpacing(10)
        vbox.addWidget(manager_label)
        vbox.addSpacing(10)
        vbox.addWidget(designer_label)
        vbox.addStretch(1)
        vbox.addSpacing(10)
        vbox.addWidget(close_button)
        vbox.addStretch(1)
        
        # Create a horizontal layout and add the vertical layout to it
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(10, 0, 10, 0)
        hbox.addLayout(vbox)

        # Set the layout of the widget
        self.setLayout(hbox)

        
    
    def openGameMenu(self):
         self.window = GameMenu()
         self.window.show()
         self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = GameMenu()
    menu.show()
    sys.exit(app.exec_())