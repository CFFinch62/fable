from PyQt6.QtWidgets import QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FABLE - Forth Animated Beginners Learning Environment")
        self.resize(1024, 768)
        self.setCentralWidget(QLabel("FABLE Placeholder"))
