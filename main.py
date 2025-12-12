import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from fable.app import MainWindow


def main():
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("FABLE")
    app.setApplicationDisplayName("FABLE - Forth Animated Beginners Learning Environment")
    app.setOrganizationName("Fragillidae Software")
    
    # Set application icon
    icon_path = Path(__file__).parent / "fable" / "resources" / "icons" / "fable_forth_aligned_256x256.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
