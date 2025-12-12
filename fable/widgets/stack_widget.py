"""
Animated stack widget for visualizing data and return stacks.
Displays stack operations with smooth animations synchronized to the interpreter.
"""

from typing import List, Optional, Any
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QPushButton, QScrollArea, QFrame, QSizePolicy
)

from .stack_item import StackItemWidget, TYPE_COLORS


def _infer_type(value) -> str:
    """Infer type identifier from value for color coding.
    
    Args:
        value: The value to type check
        
    Returns:
        Type identifier string
    """
    if isinstance(value, bool):
        return 'bool'
    if isinstance(value, int):
        if value in (-1, 0):  # Common flag values
            return 'bool'
        return 'int'
    if isinstance(value, float):
        return 'float'
    if isinstance(value, str):
        return 'string'
    return 'int'


class StackSection(QWidget):
    """A single stack display (data or return).
    
    Displays stack items vertically with the top of stack at the bottom.
    Supports animated push/pop/swap operations.
    """
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self._title = title
        self._items: List[StackItemWidget] = []
        self._animation_duration = 150  # Base duration in ms
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header - no hardcoded style, will be themed
        self.header = QLabel(self._title)
        self.header.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header)
        
        # Scroll area for items - no hardcoded style, will be themed
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container for stack items
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(8, 8, 8, 8)
        self.container_layout.setSpacing(6)
        self.container_layout.addStretch()  # Push items to bottom
        
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)
        
        # Empty indicator
        self.empty_label = QLabel("(empty)")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container_layout.insertWidget(0, self.empty_label)
    
    def set_animation_speed(self, duration_ms: int):
        """Set base animation duration.
        
        Args:
            duration_ms: Duration in milliseconds
        """
        self._animation_duration = duration_ms
    
    def update_stack(self, values: List[Any], animate: bool = True):
        """Update display to match stack state.
        
        Efficiently adds/removes items with animations.
        
        Args:
            values: Current stack values (bottom to top)
            animate: Whether to animate changes
        """
        # Hide empty label if we have items
        self.empty_label.setVisible(len(values) == 0)
        
        current_count = len(self._items)
        new_count = len(values)
        
        if new_count > current_count:
            # Items were pushed
            for i in range(current_count, new_count):
                self._add_item(values[i], animate)
        elif new_count < current_count:
            # Items were popped
            for _ in range(current_count - new_count):
                self._remove_item(animate)
        else:
            # Same count - update values (might be swap, etc.)
            for i, value in enumerate(values):
                if i < len(self._items):
                    self._items[i].value = value
    
    def _add_item(self, value, animate: bool = True):
        """Add a new item (push operation).
        
        Args:
            value: Value to push
            animate: Whether to animate
        """
        value_type = _infer_type(value)
        item = StackItemWidget(value, value_type, self.container)
        
        # Insert before the stretch at the end
        self.container_layout.insertWidget(
            self.container_layout.count() - 1,
            item
        )
        self._items.append(item)
        
        if animate:
            item.animate_push(self._animation_duration)
            
        # Ensure new item is visible
        QTimer.singleShot(10, lambda: self._ensure_visible(item))
    
    def _ensure_visible(self, item):
        """Scroll to make item visible."""
        self.scroll.ensureWidgetVisible(item)
    
    def _remove_item(self, animate: bool = True):
        """Remove top item (pop operation).
        
        Args:
            animate: Whether to animate
        """
        if not self._items:
            return
        
        item = self._items.pop()
        
        if animate:
            item.animate_pop(self._animation_duration)
        else:
            self.container_layout.removeWidget(item)
            item.deleteLater()
    
    def clear_all(self, animate: bool = False):
        """Clear all items.
        
        Args:
            animate: Whether to animate removal
        """
        for item in self._items:
            self.container_layout.removeWidget(item)
            item.deleteLater()
        self._items.clear()
        self.empty_label.setVisible(True)
    
    def highlight_top(self, count: int = 1):
        """Highlight the top N items.
        
        Args:
            count: Number of items to highlight
        """
        for i, item in enumerate(reversed(self._items)):
            if i < count:
                item.highlight_consumed(True)
            else:
                item.highlight_consumed(False)
    
    def clear_highlights(self):
        """Remove all preview highlights."""
        for item in self._items:
            item.highlight_consumed(False)


class StackWidget(QWidget):
    """Complete animated stack display with data and return stacks.
    
    Features:
    - Dual stack display (data stack, return stack)
    - Smooth push/pop/swap animations
    - Animation speed control
    - Interpreter signal synchronization
    
    Signals:
        step_clicked: Emitted when step button is clicked
    """
    
    step_clicked = pyqtSignal()
    speed_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._current_stack: List[Any] = []
        self._current_rstack: List[Any] = []
    
    def _setup_ui(self):
        """Initialize the UI."""
        self.setMinimumWidth(250)
        self.setStyleSheet("""
            QWidget {
                background-color: #252526;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Data stack section
        self.data_section = StackSection("DATA STACK")
        layout.addWidget(self.data_section, stretch=3)
        
        # Return stack section  
        self.return_section = StackSection("RETURN STACK")
        layout.addWidget(self.return_section, stretch=1)
        
        # Control bar
        self.controls_widget = QWidget()
        self.controls_widget.setStyleSheet("background-color: #2D2D2D;")
        controls_layout = QHBoxLayout(self.controls_widget)
        controls_layout.setContentsMargins(8, 8, 8, 8)
        
        # Speed label
        self.speed_label = QLabel("Speed:")
        self.speed_label.setStyleSheet("color: #808080;")
        controls_layout.addWidget(self.speed_label)
        
        # Speed slider
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(50, 3000)  # Up to 3 seconds
        self.speed_slider.setValue(150)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #3C3C3C;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #007ACC;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #007ACC;
                border-radius: 3px;
            }
        """)
        self.speed_slider.valueChanged.connect(self._on_speed_changed)
        controls_layout.addWidget(self.speed_slider)
        
        # Step button
        self.step_button = QPushButton("Step")
        self.step_button.setStyleSheet("""
            QPushButton {
                background-color: #0E639C;
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177BB;
            }
            QPushButton:pressed {
                background-color: #0D5A8C;
            }
        """)
        self.step_button.clicked.connect(self.step_clicked.emit)
        controls_layout.addWidget(self.step_button)
        
        layout.addWidget(self.controls_widget)
    
    def _on_speed_changed(self, value: int):
        """Handle speed slider change.
        
        Args:
            value: New duration in ms (lower = faster)
        """
        self.data_section.set_animation_speed(value)
        self.return_section.set_animation_speed(value)
        self.speed_changed.emit(value)
    
    def update_data_stack(self, values: List[Any], animate: bool = True):
        """Update the data stack display.
        
        Args:
            values: Current stack values (bottom to top)
            animate: Whether to animate changes
        """
        self._current_stack = list(values)
        self.data_section.update_stack(values, animate)
    
    def update_return_stack(self, values: List[Any], animate: bool = True):
        """Update the return stack display.
        
        Args:
            values: Current stack values
            animate: Whether to animate
        """
        self._current_rstack = list(values)
        self.return_section.update_stack(values, animate)
    
    def clear(self):
        """Clear both stacks."""
        self.data_section.clear_all()
        self.return_section.clear_all()
        self._current_stack = []
        self._current_rstack = []
    
    def show_operation_preview(self, word: str):
        """Show preview of which items an operation will consume.
        
        Args:
            word: Word being executed
        """
        # Map words to how many items they consume
        consume_counts = {
            '+': 2, '-': 2, '*': 2, '/': 2, 'MOD': 2,
            'DUP': 1, 'DROP': 1, 'SWAP': 2, 'OVER': 2, 'ROT': 3,
            '.': 1, 'NEGATE': 1, 'ABS': 1, '1+': 1, '1-': 1,
            '=': 2, '<': 2, '>': 2, 'AND': 2, 'OR': 2, 'XOR': 2,
        }
        count = consume_counts.get(word.upper(), 0)
        if count > 0:
            self.data_section.highlight_top(count)
    
    def clear_preview(self):
        """Clear operation preview highlights."""
        self.data_section.clear_highlights()
    
    # Slots for interpreter signals
    def on_word_starting(self, word: str, stack_effect: str):
        """Handle word_starting signal from interpreter.
        
        Args:
            word: Word about to execute
            stack_effect: Stack effect notation
        """
        self.show_operation_preview(word)
    
    def on_word_complete(self, word: str, stack_state: List[Any]):
        """Handle word_complete signal from interpreter.
        
        Args:
            word: Word that finished
            stack_state: Current stack after operation
        """
        self.clear_preview()
        self.update_data_stack(stack_state)
    
    def on_state_changed(self, data_stack: List[Any], return_stack: List[Any]):
        """Handle full state update.
        
        Args:
            data_stack: Current data stack
            return_stack: Current return stack
        """
        self.update_data_stack(data_stack)
        self.update_return_stack(return_stack)
