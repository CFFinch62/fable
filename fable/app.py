"""
Main application window and entry point.
Integrates all FABLE components into a cohesive IDE.
"""

from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from PyQt6.QtWidgets import (
    QMainWindow, QSplitter, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar, QLabel, QTabWidget,
    QFileDialog, QMessageBox
)

from fable.widgets.file_browser import FileBrowser
from fable.widgets.editor import ForthEditor
from fable.widgets.repl import ForthREPL
from fable.widgets.stack_widget import StackWidget
from fable.utils.settings import get_settings
from fable.utils.themes import THEMES, get_theme, apply_theme, DARK_THEMES, LIGHT_THEMES
from fable.interpreter.interpreter import ForthInterpreter


class MainWindow(QMainWindow):
    """Main FABLE application window.
    
    Layout:
        ┌─────────┬──────────────────┬─────────────┐
        │  File   │    Editor        │   Stack     │
        │ Browser │    (tabs)        │   Widget    │
        │         ├──────────────────┤             │
        │         │    REPL          │             │
        └─────────┴──────────────────┴─────────────┘
    """
    
    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        self._setup_window()
        self._create_interpreter()
        self._create_widgets()
        self._create_layout()
        self._create_menus()
        self._create_toolbar()
        self._create_statusbar()
        self._restore_state()
        self._connect_signals()
    
    def _setup_window(self):
        """Configure main window properties."""
        self.setWindowTitle("FABLE - Forth Animated Beginners Learning Environment")
        self.setMinimumSize(800, 600)
        self.resize(1280, 800)
    
    def _create_interpreter(self):
        """Create and configure the Forth interpreter."""
        self.interpreter = ForthInterpreter(self)
    
    def _create_widgets(self):
        """Create all child widgets."""
        # File browser (left panel)
        self.file_browser = FileBrowser()
        
        # Editor with tabs (center top)
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.setMovable(True)
        self.editor_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background-color: #2D2D2D;
                color: #808080;
                padding: 8px 16px;
                border: none;
                border-right: 1px solid #1E1E1E;
            }
            QTabBar::tab:selected {
                background-color: #1E1E1E;
                color: #D4D4D4;
            }
            QTabBar::tab:hover:!selected {
                background-color: #383838;
            }
        """)
        self.editor_tabs.tabCloseRequested.connect(self._close_tab)
        
        # Add initial empty editor
        self._new_file()
        
        # REPL (center bottom)
        self.repl = ForthREPL()
        
        # Stack widget (right panel)
        self.stack_widget = StackWidget()
    
    def _create_layout(self):
        """Set up the panel layout with splitters."""
        # Main horizontal splitter: [File Browser | Center | Stack]
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Center vertical splitter: [Editor / REPL]
        self.center_splitter = QSplitter(Qt.Orientation.Vertical)
        self.center_splitter.addWidget(self.editor_tabs)
        self.center_splitter.addWidget(self.repl)
        self.center_splitter.setSizes([500, 200])
        
        # Add to main splitter
        self.main_splitter.addWidget(self.file_browser)
        self.main_splitter.addWidget(self.center_splitter)
        self.main_splitter.addWidget(self.stack_widget)
        self.main_splitter.setSizes([200, 700, 300])
        
        # Set as central widget
        self.setCentralWidget(self.main_splitter)
    
    def _create_menus(self):
        """Create the menu bar and menus."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New File", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open File...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)
        
        open_folder_action = QAction("Open &Folder...", self)
        open_folder_action.setShortcut("Ctrl+K")
        open_folder_action.triggered.connect(self._open_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self._undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self._redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self._cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self._copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self._paste)
        edit_menu.addAction(paste_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        self.toggle_browser_action = QAction("&File Browser", self)
        self.toggle_browser_action.setShortcut("Ctrl+B")
        self.toggle_browser_action.setCheckable(True)
        self.toggle_browser_action.setChecked(True)
        self.toggle_browser_action.triggered.connect(self._toggle_file_browser)
        view_menu.addAction(self.toggle_browser_action)
        
        self.toggle_repl_action = QAction("&Terminal/REPL", self)
        self.toggle_repl_action.setShortcut("Ctrl+T")
        self.toggle_repl_action.setCheckable(True)
        self.toggle_repl_action.setChecked(True)
        self.toggle_repl_action.triggered.connect(self._toggle_repl)
        view_menu.addAction(self.toggle_repl_action)
        
        view_menu.addSeparator()
        
        # Theme submenu
        theme_menu = view_menu.addMenu("&Theme")
        
        # Dark themes
        dark_menu = theme_menu.addMenu("Dark Themes")
        for theme_id in DARK_THEMES:
            theme = THEMES[theme_id]
            action = QAction(theme.name, self)
            action.setData(theme_id)
            action.triggered.connect(lambda checked, tid=theme_id: self._apply_theme(tid))
            dark_menu.addAction(action)
        
        # Light themes
        light_menu = theme_menu.addMenu("Light Themes")
        for theme_id in LIGHT_THEMES:
            theme = THEMES[theme_id]
            action = QAction(theme.name, self)
            action.setData(theme_id)
            action.triggered.connect(lambda checked, tid=theme_id: self._apply_theme(tid))
            light_menu.addAction(action)
        
        # Run menu
        run_menu = menubar.addMenu("&Run")
        
        run_file_action = QAction("Run &File", self)
        run_file_action.setShortcut("F5")
        run_file_action.triggered.connect(self._run_file)
        run_menu.addAction(run_file_action)
        
        run_selection_action = QAction("Run &Selection", self)
        run_selection_action.setShortcut("F6")
        run_selection_action.triggered.connect(self._run_selection)
        run_menu.addAction(run_selection_action)
        
        run_line_action = QAction("Run &Line", self)
        run_line_action.setShortcut("F7")
        run_line_action.triggered.connect(self._run_line)
        run_menu.addAction(run_line_action)
        
        run_menu.addSeparator()
        
        reset_action = QAction("&Reset Interpreter", self)
        reset_action.setShortcut("Ctrl+R")
        reset_action.triggered.connect(self._reset_interpreter)
        run_menu.addAction(reset_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About FABLE", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """Create the main toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2D2D2D;
                border: none;
                padding: 4px;
                spacing: 4px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 6px;
                color: #D4D4D4;
            }
            QToolButton:hover {
                background-color: #3C3C3C;
            }
        """)
        self.addToolBar(toolbar)
        
        # File actions
        toolbar.addAction("New", self._new_file)
        toolbar.addAction("Open", self._open_file)
        toolbar.addAction("Save", self._save_file)
        toolbar.addSeparator()
        
        # Edit actions
        toolbar.addAction("Undo", self._undo)
        toolbar.addAction("Redo", self._redo) 
        toolbar.addSeparator()
        
        # Run actions
        toolbar.addAction("▶ Run", self._run_file)
        toolbar.addAction("⏸ Step", self._step)
        toolbar.addAction("⏹ Stop", self._stop)
    
    def _create_statusbar(self):
        """Create the status bar."""
        self.statusbar = QStatusBar()
        self.statusbar.setStyleSheet("""
            QStatusBar {
                background-color: #007ACC;
                color: white;
            }
            QStatusBar::item {
                border: none;
            }
        """)
        self.setStatusBar(self.statusbar)
        
        # Mode indicator
        self.mode_label = QLabel("Interpret")
        self.statusbar.addWidget(self.mode_label)
        
        # Spacer
        spacer = QWidget()
        spacer.setMinimumWidth(50)
        self.statusbar.addWidget(spacer, 1)
        
        # Stack effect
        self.stack_effect_label = QLabel("")
        self.statusbar.addWidget(self.stack_effect_label)
        
        # Cursor position
        self.position_label = QLabel("Ln 1, Col 1")
        self.statusbar.addPermanentWidget(self.position_label)
    
    def _connect_signals(self):
        """Connect widget signals."""
        # File browser -> Editor
        self.file_browser.file_double_clicked.connect(self._open_file_path)
        
        # REPL -> Interpreter
        self.repl.input_submitted.connect(self._execute_forth)
        
        # Interpreter -> REPL output
        self.interpreter.output.connect(self.repl.append_output)
        self.interpreter.error_occurred.connect(self.repl.append_error)
        
        # Interpreter -> Status bar and REPL mode updates
        self.interpreter.state_changed.connect(self._update_mode_display)
        self.interpreter.state_changed.connect(self._update_repl_mode)
        
        # Interpreter -> Stack widget
        self.interpreter.word_starting.connect(self.stack_widget.on_word_starting)
        self.interpreter.word_complete.connect(self.stack_widget.on_word_complete)
    
    def _restore_state(self):
        """Restore window geometry and splitter positions."""
        # Restore theme
        try:
            theme_id = self.settings.get('appearance', 'theme', 'dark_default')
            # Validate theme exists
            if theme_id not in THEMES:
                theme_id = 'dark_default'
            self._apply_theme(theme_id)
        except Exception as e:
            print(f"Error restoring theme: {e}")
            self._apply_theme('dark_default')
        
        geometry = self.settings.get_bytes('window', 'geometry')
        if geometry:
            self.restoreGeometry(geometry)
        
        state = self.settings.get_bytes('window', 'state')
        if state:
            self.restoreState(state)
        
        # Restore panel visibility
        browser_visible = self.settings.get('panels', 'file_browser_visible', True)
        self.file_browser.setVisible(browser_visible)
        self.toggle_browser_action.setChecked(browser_visible)
        
        repl_visible = self.settings.get('panels', 'repl_visible', True)
        self.repl.setVisible(repl_visible)
        self.toggle_repl_action.setChecked(repl_visible)
    
    def closeEvent(self, event):
        """Save state before closing."""
        self.settings.set_bytes('window', 'geometry', self.saveGeometry())
        self.settings.set_bytes('window', 'state', self.saveState())
        self.settings.set('panels', 'file_browser_visible', self.file_browser.isVisible())
        self.settings.set('panels', 'repl_visible', self.repl.isVisible())
        self.settings.save()
        event.accept()
    
    # --- File Operations ---
    
    def _new_file(self):
        """Create a new file tab."""
        editor = ForthEditor()
        index = self.editor_tabs.addTab(editor, "Untitled")
        self.editor_tabs.setCurrentIndex(index)
        editor.cursorPositionChanged.connect(self._update_cursor_position)
    
    def _open_file(self):
        """Open a file dialog and load selected file."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "",
            "Forth Files (*.fs *.fth *.4th *.forth);;All Files (*)"
        )
        if path:
            self._open_file_path(path)
    
    def _open_file_path(self, path: str):
        """Open a file by path."""
        try:
            with open(path, 'r') as f:
                content = f.read()
            
            editor = ForthEditor()
            editor.setPlainText(content)
            editor.setProperty("file_path", path)
            editor.cursorPositionChanged.connect(self._update_cursor_position)
            
            name = Path(path).name
            index = self.editor_tabs.addTab(editor, name)
            self.editor_tabs.setCurrentIndex(index)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")
    
    def _open_folder(self):
        """Open a folder as project root."""
        path = QFileDialog.getExistingDirectory(self, "Open Folder")
        if path:
            self.file_browser.set_root_path(path)
    
    def _save_file(self):
        """Save the current file."""
        editor = self.editor_tabs.currentWidget()
        if not editor:
            return
        
        path = editor.property("file_path")
        if path:
            self._save_to_path(editor, path)
        else:
            self._save_file_as()
    
    def _save_file_as(self):
        """Save current file with a new name."""
        editor = self.editor_tabs.currentWidget()
        if not editor:
            return
        
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "",
            "Forth Files (*.fs);;All Files (*)"
        )
        if path:
            self._save_to_path(editor, path)
            editor.setProperty("file_path", path)
            index = self.editor_tabs.currentIndex()
            self.editor_tabs.setTabText(index, Path(path).name)
    
    def _save_to_path(self, editor: ForthEditor, path: str):
        """Save editor content to path."""
        try:
            with open(path, 'w') as f:
                f.write(editor.toPlainText())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")
    
    def _close_tab(self, index: int):
        """Close a tab."""
        self.editor_tabs.removeTab(index)
        if self.editor_tabs.count() == 0:
            self._new_file()
    
    # --- Edit Operations ---
    
    def _undo(self):
        editor = self.editor_tabs.currentWidget()
        if editor:
            editor.undo()
    
    def _redo(self):
        editor = self.editor_tabs.currentWidget()
        if editor:
            editor.redo()
    
    def _cut(self):
        editor = self.editor_tabs.currentWidget()
        if editor:
            editor.cut()
    
    def _copy(self):
        editor = self.editor_tabs.currentWidget()
        if editor:
            editor.copy()
    
    def _paste(self):
        editor = self.editor_tabs.currentWidget()
        if editor:
            editor.paste()
    
    # --- View Operations ---
    
    def _toggle_file_browser(self, checked: bool):
        """Toggle file browser visibility."""
        self.file_browser.setVisible(checked)
    
    def _toggle_repl(self, checked: bool):
        """Toggle REPL visibility."""
        self.repl.setVisible(checked)
    
    # --- Run Operations ---
    
    def _execute_forth(self, code: str):
        """Execute Forth code and handle errors.
        
        Args:
            code: Forth source code to execute
        """
        try:
            self.interpreter.evaluate(code)
        except Exception as e:
            # Error already emitted via signal
            pass
    
    def _run_file(self):
        """Run the entire current file."""
        editor = self.editor_tabs.currentWidget()
        if editor:
            code = editor.toPlainText()
            if code.strip():
                self._execute_forth(code)
    
    def _run_selection(self):
        """Run selected text."""
        editor = self.editor_tabs.currentWidget()
        if editor:
            code = editor.get_selected_text()
            if code.strip():
                self._execute_forth(code)
    
    def _run_line(self):
        """Run current line."""
        editor = self.editor_tabs.currentWidget()
        if editor:
            code = editor.get_current_line()
            if code.strip():
                self._execute_forth(code)
    
    def _step(self):
        """Step through code."""
        self.repl.append_output("[Step mode not yet implemented]\n")
    
    def _stop(self):
        """Stop execution."""
        self.repl.append_output("[Stop]\n")
    
    def _reset_interpreter(self):
        """Reset the interpreter."""
        self.interpreter.reset()
        self.repl.append_output("[Interpreter reset]\n")
    
    def _update_mode_display(self):
        """Update the mode indicator in status bar."""
        mode = "Compile" if self.interpreter.compiling else "Interpret"
        self.mode_label.setText(mode)
    
    def _update_repl_mode(self):
        """Update REPL prompt for compile/interpret mode."""
        self.repl.set_compile_mode(self.interpreter.compiling)
    
    # --- Status Bar ---
    
    def _update_cursor_position(self):
        """Update cursor position in status bar."""
        editor = self.editor_tabs.currentWidget()
        if editor:
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.position_label.setText(f"Ln {line}, Col {col}")
    
    # --- Help ---
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About FABLE",
            "<h2>FABLE</h2>"
            "<p><i>Forth Animated Beginners Learning Environment</i></p>"
            "<p><b>Every stack tells a story</b></p>"
            "<p>Version 0.1.0</p>"
            "<p>© 2025 Chuck / Fragillidae Software</p>"
        )
    
    # --- Theme ---
    
    def _apply_theme(self, theme_id: str):
        """Apply a theme to the application and all widgets."""
        from PyQt6.QtWidgets import QApplication
        theme = get_theme(theme_id)
        
        # Apply global stylesheet
        stylesheet = apply_theme(self, theme)
        QApplication.instance().setStyleSheet(stylesheet)
        
        # Apply to editor tabs
        self.editor_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {theme.editor_bg};
            }}
            QTabBar::tab {{
                background-color: {theme.panel};
                color: {theme.text_secondary};
                padding: 8px 16px;
                border: none;
                border-right: 1px solid {theme.background};
            }}
            QTabBar::tab:selected {{
                background-color: {theme.editor_bg};
                color: {theme.text};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {theme.border};
            }}
        """)
        
        # Apply to each editor
        for i in range(self.editor_tabs.count()):
            editor = self.editor_tabs.widget(i)
            if editor:
                editor.setStyleSheet(f"""
                    QPlainTextEdit {{
                        background-color: {theme.editor_bg};
                        color: {theme.editor_text};
                        border: none;
                        selection-background-color: {theme.editor_selection};
                    }}
                """)
        
        # Apply to REPL
        self.repl.output.setStyleSheet(f"""
            QTextEdit {{
                background-color: {theme.editor_bg};
                color: {theme.text};
                border: none;
                border-bottom: 1px solid {theme.border};
                padding: 8px;
            }}
        """)
        self.repl.input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {theme.panel};
                color: {theme.text};
                border: none;
                padding: 8px 8px 8px 50px;
            }}
        """)
        self.repl.prompt_label.setStyleSheet(f"color: {theme.syntax_logic}; background: transparent;")
        
        # Apply to file browser
        self.file_browser.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.panel};
                color: {theme.text};
            }}
        """)
        self.file_browser.tree.setStyleSheet(f"""
            QTreeView {{
                background-color: {theme.panel};
                color: {theme.text};
                border: none;
                outline: none;
            }}
            QTreeView::item {{
                padding: 4px;
            }}
            QTreeView::item:selected {{
                background-color: {theme.accent};
            }}
            QTreeView::item:hover {{
                background-color: {theme.border};
            }}
        """)
        self.file_browser.header.setStyleSheet(f"background-color: {theme.panel}; padding: 8px;")
        self.file_browser.title_label.setStyleSheet(f"color: {theme.text_secondary}; background: transparent;")
        
        # Apply to stack widget - need to style deeply
        stack_style = f"""
            QWidget {{
                background-color: {theme.panel};
                color: {theme.text};
            }}
            QLabel {{
                color: {theme.text};
                background-color: transparent;
            }}
            QScrollArea {{
                background-color: {theme.editor_bg};
                border: none;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: {theme.editor_bg};
            }}
            QSlider::groove:horizontal {{
                background-color: {theme.border};
                height: 4px;
            }}
            QSlider::handle:horizontal {{
                background-color: {theme.accent};
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }}
            QPushButton {{
                background-color: {theme.panel};
                color: {theme.text};
                border: 1px solid {theme.border};
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: {theme.border};
            }}
        """
        self.stack_widget.setStyleSheet(stack_style)
        
        # Style stack sections components directly
        for section in [self.stack_widget.data_section, self.stack_widget.return_section]:
            # Apply base style to section widget
            section.setStyleSheet(stack_style)
            
            # Style header if exposed
            if hasattr(section, 'header'):
                section.header.setStyleSheet(f"""
                    background-color: {theme.panel}; 
                    color: {theme.text_secondary}; 
                    padding: 8px;
                """)
            
            # Style scroll area
            if hasattr(section, 'scroll'):
                section.scroll.setStyleSheet(f"""
                    QScrollArea {{
                        background-color: {theme.editor_bg};
                        border: none;
                    }}
                    QScrollArea > QWidget > QWidget {{
                        background-color: {theme.editor_bg};
                    }}
                """)
                
            # Style empty label
            if hasattr(section, 'empty_label'):
                section.empty_label.setStyleSheet(f"color: {theme.text_muted}; font-style: italic;")
        
        # Style stack controls
        if hasattr(self.stack_widget, 'controls_widget'):
            self.stack_widget.controls_widget.setStyleSheet(f"background-color: {theme.panel};")
            
        if hasattr(self.stack_widget, 'speed_label'):
            self.stack_widget.speed_label.setStyleSheet(f"color: {theme.text_secondary};")
            
        if hasattr(self.stack_widget, 'speed_slider'):
            self.stack_widget.speed_slider.setStyleSheet(f"""
                QSlider::groove:horizontal {{
                    background: {theme.border};
                    height: 6px;
                    border-radius: 3px;
                }}
                QSlider::handle:horizontal {{
                    background: {theme.accent};
                    width: 16px;
                    margin: -5px 0;
                    border-radius: 8px;
                }}
                QSlider::sub-page:horizontal {{
                    background: {theme.accent};
                    border-radius: 3px;
                }}
            """)
            
        if hasattr(self.stack_widget, 'step_button'):
            self.stack_widget.step_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme.accent};
                    color: white;
                    border: none;
                    padding: 6px 16px;
                    border-radius: 3px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {theme.accent_hover};
                }}
                QPushButton:pressed {{
                    background-color: {theme.accent};
                }}
            """)
        
        # Update splitters
        for splitter in [self.main_splitter, self.center_splitter]:
            splitter.setStyleSheet(f"""
                QSplitter::handle {{
                    background-color: {theme.border};
                }}
            """)
        
        # Save preference
        self.settings.set('appearance', 'theme', theme_id)
        self.settings.save()
        self._current_theme = theme
