"""
File browser widget for project navigation.
Includes context menu, file operations, and Forth file filtering.
"""

from pathlib import Path
import os
import shutil

from PyQt6.QtCore import Qt, pyqtSignal, QDir
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView,
    QLabel, QHBoxLayout, QMenu, QInputDialog,
    QMessageBox, QLineEdit
)
from PyQt6.QtGui import QFont, QFileSystemModel, QAction, QIcon
from fable.utils.settings import Settings


class ForthFileSystemModel(QFileSystemModel):
    """File system model with Forth file type awareness."""
    
    # Forth file extensions
    FORTH_EXTENSIONS = {'.fs', '.fth', '.4th', '.forth', '.f'}
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Show all files but can filter to Forth files
        self._show_all_files = True
    
    def setShowAllFiles(self, show_all: bool):
        """Toggle between showing all files or just Forth files."""
        self._show_all_files = show_all
        self.setNameFilters(self._get_filters())
    
    def _get_filters(self):
        """Get name filters based on current mode."""
        if self._show_all_files:
            return []
        return ['*.fs', '*.fth', '*.4th', '*.forth', '*.f']


class FileBrowser(QWidget):
    """File browser panel for project navigation.
    
    Features:
        - Tree view of files and folders
        - Context menu for file operations
        - Forth file type awareness
        - Recent files tracking
    
    Signals:
        file_double_clicked(str): Emitted when a file is double-clicked
        file_selected(str): Emitted when a file is selected
        file_created(str): Emitted when a new file is created
        file_deleted(str): Emitted when a file is deleted
    """
    
    file_double_clicked = pyqtSignal(str)
    file_selected = pyqtSignal(str)
    file_created = pyqtSignal(str)
    file_deleted = pyqtSignal(str)
    bookmarks_changed = pyqtSignal(list)
    root_path_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Settings()
        self._root_path: Path | None = None
        self._bookmarks: list[Path] = []
        self._setup_ui()
        self._setup_context_menu()
        self._load_settings()
    
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
        self.header = QWidget()
        self.header.setStyleSheet("background-color: #2D2D2D; padding: 8px;")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(8, 8, 8, 8)
        
        self.title_label = QLabel("EXPLORER")
        self.title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #808080;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        # Navigation buttons
        from PyQt6.QtWidgets import QToolButton

        # Home button - go to user's home directory
        self.home_btn = QToolButton()
        self.home_btn.setText("⌂")
        self.home_btn.setToolTip("Go to Home Directory")
        self.home_btn.clicked.connect(self._go_home)
        self.home_btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                color: #808080;
                border: none;
                font-size: 14px;
                padding: 0 4px;
            }
            QToolButton:hover {
                color: #D4D4D4;
            }
        """)
        header_layout.addWidget(self.home_btn)

        # Go Up button - navigate to parent folder
        self.up_btn = QToolButton()
        self.up_btn.setText("↑")
        self.up_btn.setToolTip("Go Up to Parent Folder")
        self.up_btn.clicked.connect(self._go_up)
        self.up_btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                color: #808080;
                border: none;
                font-size: 14px;
                padding: 0 4px;
            }
            QToolButton:hover {
                color: #D4D4D4;
            }
        """)
        header_layout.addWidget(self.up_btn)

        # Bookmarks button
        self.bookmarks_btn = QToolButton()
        self.bookmarks_btn.setText("★")
        self.bookmarks_btn.setToolTip("Bookmarks")
        self.bookmarks_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.bookmarks_btn.setStyleSheet("""
            QToolButton {
                background: transparent;
                color: #808080;
                border: none;
                font-size: 14px;
                padding: 0 4px;
            }
            QToolButton::menu-indicator {
                image: none;
            }
            QToolButton:hover {
                color: #D4D4D4;
            }
        """)
        
        self.bookmarks_menu = QMenu(self)
        self.bookmarks_menu.aboutToShow.connect(self._update_bookmarks_menu)
        self.bookmarks_btn.setMenu(self.bookmarks_menu)
        header_layout.addWidget(self.bookmarks_btn)
        
        layout.addWidget(self.header)
        
        # File system model
        self.model = ForthFileSystemModel()
        self.model.setRootPath("")
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        
        # Tree view
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        self.tree.setAnimated(True)
        self.tree.setIndentation(16)
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        
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
            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
            }
            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings {
                border-image: none;
            }
        """)
        
        # Enable context menu
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        
        self.tree.doubleClicked.connect(self._on_double_click)
        self.tree.clicked.connect(self._on_click)
        
        layout.addWidget(self.tree)
    
    def _setup_context_menu(self):
        """Set up the context menu actions."""
        self.context_menu = QMenu(self)
        self.context_menu.setStyleSheet("""
            QMenu {
                background-color: #2D2D2D;
                color: #D4D4D4;
                border: 1px solid #3C3C3C;
            }
            QMenu::item {
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #094771;
            }
            QMenu::separator {
                height: 1px;
                background: #3C3C3C;
                margin: 4px 0;
            }
        """)
        
        # New File
        self.action_new_file = QAction("New File", self)
        self.action_new_file.triggered.connect(self._new_file)
        self.context_menu.addAction(self.action_new_file)
        
        # New Folder
        self.action_new_folder = QAction("New Folder", self)
        self.action_new_folder.triggered.connect(self._new_folder)
        self.context_menu.addAction(self.action_new_folder)
        
        self.context_menu.addSeparator()
        
        # Rename
        self.action_rename = QAction("Rename", self)
        self.action_rename.triggered.connect(self._rename_item)
        self.context_menu.addAction(self.action_rename)
        
        # Delete
        self.action_delete = QAction("Delete", self)
        self.action_delete.triggered.connect(self._delete_item)
        self.context_menu.addAction(self.action_delete)
        
        self.context_menu.addSeparator()
        
        # Refresh
        self.action_refresh = QAction("Refresh", self)
        self.action_refresh.triggered.connect(self._refresh)
        self.context_menu.addAction(self.action_refresh)
        
        # Open Folder (set as root)
        self.action_open_folder = QAction("Open Folder", self)
        self.action_open_folder.triggered.connect(self._open_selected_folder)
        self.context_menu.addAction(self.action_open_folder)
        
        # Go Up
        self.action_go_up = QAction("Go Up", self)
        self.action_go_up.triggered.connect(self._go_up)
        self.context_menu.addAction(self.action_go_up)
        
        self.context_menu.addSeparator()
        
        # Open in System
        self.action_reveal = QAction("Reveal in File Manager", self)
        self.action_reveal.triggered.connect(self._reveal_in_system)
        self.context_menu.addAction(self.action_reveal)
    
    def _show_context_menu(self, position):
        """Show context menu at the given position."""
        index = self.tree.indexAt(position)
        has_selection = index.isValid()
        is_dir = has_selection and self.model.isDir(index)
        
        # Enable/disable actions based on selection
        self.action_rename.setEnabled(has_selection)
        self.action_delete.setEnabled(has_selection)
        self.action_reveal.setEnabled(has_selection)
        self.action_open_folder.setEnabled(is_dir)
        self.action_go_up.setEnabled(self._root_path is not None and self._root_path.parent != self._root_path)
        
        self.context_menu.exec(self.tree.viewport().mapToGlobal(position))
    
    def _new_file(self):
        """Create a new file in the selected folder."""
        parent_path = self._get_selected_folder()
        if not parent_path:
            return
        
        name, ok = QInputDialog.getText(
            self, "New File", "File name:",
            QLineEdit.EchoMode.Normal, "untitled.fs"
        )
        
        if ok and name:
            new_path = parent_path / name
            try:
                new_path.touch()
                self.file_created.emit(str(new_path))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create file:\n{e}")
    
    def _new_folder(self):
        """Create a new folder in the selected location."""
        parent_path = self._get_selected_folder()
        if not parent_path:
            return
        
        name, ok = QInputDialog.getText(
            self, "New Folder", "Folder name:",
            QLineEdit.EchoMode.Normal, "New Folder"
        )
        
        if ok and name:
            new_path = parent_path / name
            try:
                new_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create folder:\n{e}")
    
    def _rename_item(self):
        """Rename the selected item."""
        path = self.get_selected_path()
        if not path:
            return
        
        path = Path(path)
        old_name = path.name
        
        new_name, ok = QInputDialog.getText(
            self, "Rename", "New name:",
            QLineEdit.EchoMode.Normal, old_name
        )
        
        if ok and new_name and new_name != old_name:
            new_path = path.parent / new_name
            try:
                path.rename(new_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not rename:\n{e}")
    
    def _delete_item(self):
        """Delete the selected item."""
        path = self.get_selected_path()
        if not path:
            return
        
        path = Path(path)
        
        reply = QMessageBox.question(
            self, "Delete",
            f"Are you sure you want to delete '{path.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                self.file_deleted.emit(str(path))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete:\n{e}")
    
    def _refresh(self):
        """Refresh the file browser."""
        if self._root_path:
            self.set_root_path(self._root_path)
    
    def _reveal_in_system(self):
        """Open the selected item in the system file manager."""
        path = self.get_selected_path()
        if not path:
            return
        
        path = Path(path)
        folder = path if path.is_dir() else path.parent
        
        import subprocess
        try:
            # Linux
            subprocess.Popen(['xdg-open', str(folder)])
        except Exception:
            pass
    
    def _get_selected_folder(self) -> Path | None:
        """Get the folder path for new item creation."""
        path = self.get_selected_path()
        if path:
            path = Path(path)
            if path.is_file():
                return path.parent
            return path
        return self._root_path
    
    def set_root_path(self, path: str | Path):
        """Set the root folder for the file browser.
        
        Args:
            path: Path to the root folder
        """
        self._root_path = Path(path)
        index = self.model.setRootPath(str(self._root_path))
        self.tree.setRootIndex(index)
        self.title_label.setText(self._root_path.name.upper())
        self.settings.set("browser", "last_directory", str(self._root_path))
        self.settings.save()
        self.root_path_changed.emit(str(self._root_path))

    def get_root_path(self) -> str | None:
        """Get the current root path."""
        return str(self._root_path) if self._root_path else None
        
    def get_bookmarks(self) -> list[str]:
        """Get list of bookmarked paths."""
        return [str(p) for p in self._bookmarks]

    def set_bookmarks(self, paths: list[str]):
        """Set list of bookmarked paths."""
        self._bookmarks = [Path(p) for p in paths if p]
        self._save_bookmarks_to_settings()

    def _save_bookmarks_to_settings(self):
        self.settings.set("browser", "bookmarks", self.get_bookmarks())
        self.settings.save()
        
    def _update_bookmarks_menu(self):
        """Rebuild the bookmarks menu."""
        self.bookmarks_menu.clear()
        
        # Add current
        if self._root_path and self._root_path not in self._bookmarks:
            action = self.bookmarks_menu.addAction(f"Bookmark '{self._root_path.name}'")
            action.triggered.connect(lambda: self._add_bookmark(self._root_path))
            self.bookmarks_menu.addSeparator()
            
        # List bookmarks
        if not self._bookmarks:
            disabled = self.bookmarks_menu.addAction("(No bookmarks)")
            disabled.setEnabled(False)
        else:
            for path in self._bookmarks:
                action = self.bookmarks_menu.addAction(path.name)
                action.setToolTip(str(path))
                action.triggered.connect(lambda checked, p=path: self.set_root_path(p))
            
            self.bookmarks_menu.addSeparator()
            clear_action = self.bookmarks_menu.addAction("Clear Bookmarks")
            clear_action.triggered.connect(self._clear_bookmarks)
            
    def _add_bookmark(self, path: Path):
        """Add a path to bookmarks."""
        if path not in self._bookmarks:
            self._bookmarks.append(path)
            self._save_bookmarks_to_settings()
            self.bookmarks_changed.emit([str(p) for p in self._bookmarks])
            
    def _clear_bookmarks(self):
        """Clear all bookmarks."""
        self._bookmarks.clear()
        self._save_bookmarks_to_settings()
        self.bookmarks_changed.emit([])
    
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
            # Set folder as new root
            self.set_root_path(path)
            return
        self.file_double_clicked.emit(path)
    
    def _on_click(self, index):
        """Handle single click on item."""
        path = self.model.filePath(index)
        self.file_selected.emit(path)
    
    def _open_selected_folder(self):
        """Set selected folder as the root."""
        path = self.get_selected_path()
        if path and Path(path).is_dir():
            self.set_root_path(path)
    
    def _go_up(self):
        """Navigate to parent folder."""
        if self._root_path and self._root_path.parent != self._root_path:
            self.set_root_path(self._root_path.parent)

    def _go_home(self):
        """Navigate to user's home directory."""
        home = Path.home()
        self.set_root_path(home)

    def _load_settings(self):
        last_dir = self.settings.get("browser", "last_directory")
        if last_dir and os.path.isdir(last_dir):
            self.set_root_path(last_dir)
        else:
            self.set_root_path(str(Path.home()))
            
        saved_bookmarks = self.settings.get("browser", "bookmarks")
        if saved_bookmarks and isinstance(saved_bookmarks, list):
            self.set_bookmarks(saved_bookmarks)
