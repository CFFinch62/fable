"""
File browser widget for project navigation.
"""

from pathlib import Path
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView,
    QLabel, QHBoxLayout
)
from PyQt6.QtGui import QFont, QFileSystemModel


class FileBrowser(QWidget):
    """File browser panel for project navigation.
    
    Displays a tree view of files and folders.
    
    Signals:
        file_double_clicked(str): Emitted when a file is double-clicked
        file_selected(str): Emitted when a file is selected
    """
    
    file_double_clicked = pyqtSignal(str)
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._root_path: Path | None = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        self.setMinimumWidth(200)
        self.setStyleSheet("""
            QWidget {
                background-color: #252526;
                color: #D4D4D4;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setStyleSheet("background-color: #2D2D2D; padding: 8px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 8, 8, 8)
        
        self.title_label = QLabel("EXPLORER")
        self.title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #808080;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        layout.addWidget(header)
        
        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        
        # Tree view
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        
        # Hide size, type, date columns
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        
        self.tree.setStyleSheet("""
            QTreeView {
                background-color: #252526;
                border: none;
                outline: none;
            }
            QTreeView::item {
                padding: 4px;
            }
            QTreeView::item:selected {
                background-color: #094771;
            }
            QTreeView::item:hover {
                background-color: #2A2D2E;
            }
        """)
        
        self.tree.doubleClicked.connect(self._on_double_click)
        self.tree.clicked.connect(self._on_click)
        
        layout.addWidget(self.tree)
    
    def set_root_path(self, path: str | Path):
        """Set the root folder for the file browser.
        
        Args:
            path: Path to the root folder
        """
        self._root_path = Path(path)
        index = self.model.setRootPath(str(self._root_path))
        self.tree.setRootIndex(index)
        self.title_label.setText(self._root_path.name.upper())
    
    def get_selected_path(self) -> str | None:
        """Get the currently selected file/folder path.
        
        Returns:
            Path string or None if nothing selected
        """
        indexes = self.tree.selectedIndexes()
        if indexes:
            return self.model.filePath(indexes[0])
        return None
    
    def _on_double_click(self, index):
        """Handle double-click on item."""
        path = self.model.filePath(index)
        if self.model.isDir(index):
            return  # Expand/collapse handled by tree
        self.file_double_clicked.emit(path)
    
    def _on_click(self, index):
        """Handle single click on item."""
        path = self.model.filePath(index)
        self.file_selected.emit(path)
