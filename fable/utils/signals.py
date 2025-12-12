"""
Custom Qt signals for FABLE.
Central location for application-wide signal definitions.
"""

from PyQt6.QtCore import QObject, pyqtSignal


class AppSignals(QObject):
    """Application-wide signals for component communication."""
    
    # Interpreter signals
    word_starting = pyqtSignal(str, str)  # word_name, stack_effect
    word_complete = pyqtSignal(str, list)  # word_name, stack_state
    error_occurred = pyqtSignal(str)  # error_message
    output = pyqtSignal(str)  # output_text
    state_changed = pyqtSignal()  # interpreter state changed
    
    # Stack widget signals
    animation_complete = pyqtSignal()
    step_requested = pyqtSignal()
    stack_changed = pyqtSignal(int)  # depth
    
    # Editor signals
    text_changed = pyqtSignal()
    cursor_word_changed = pyqtSignal(str)  # word_under_cursor
    run_requested = pyqtSignal(str)  # code_to_run
    
    # REPL signals
    input_submitted = pyqtSignal(str)  # input_text
    
    # File browser signals
    file_double_clicked = pyqtSignal(str)  # file_path
    file_selected = pyqtSignal(str)  # file_path


# Global signals instance
_app_signals: AppSignals | None = None


def get_app_signals() -> AppSignals:
    """Get the global application signals instance."""
    global _app_signals
    if _app_signals is None:
        _app_signals = AppSignals()
    return _app_signals
