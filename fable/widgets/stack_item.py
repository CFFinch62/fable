"""
Individual stack item widget with full animation support.
Displays a single value with type indicator and smooth animations.
"""

from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QPoint, QEasingCurve, 
    pyqtProperty, QParallelAnimationGroup, QSequentialAnimationGroup,
    pyqtSignal, QTimer
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QGraphicsOpacityEffect


# Type indicator colors
TYPE_COLORS = {
    'int': '#569CD6',
    'float': '#6A9955', 
    'addr': '#D4A017',
    'string': '#C586C0',
    'bool': '#4EC9B0',
}


class StackItemWidget(QFrame):
    """Visual representation of a single stack value with animations.
    
    Displays the value with a colored type indicator strip on the left.
    Supports smooth animations for push, pop, highlight, and movement.
    
    Signals:
        animation_finished: Emitted when any animation completes
    
    Attributes:
        value: The stored value
        value_type: Type identifier ('int', 'float', 'addr', 'string', 'bool')
    """
    
    animation_finished = pyqtSignal()
    
    def __init__(self, value, value_type: str = "int", parent=None):
        super().__init__(parent)
        self._value = value
        self._value_type = value_type
        self._setup_ui()
        self._setup_effects()
        self._current_animation = None
    
    def _setup_ui(self):
        """Initialize the user interface."""
        self.setFixedHeight(40)
        self.setMinimumWidth(120)
        
        type_color = TYPE_COLORS.get(self._value_type, TYPE_COLORS['int'])
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-left: 5px solid {type_color};
                border-radius: 4px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 4)
        
        # Value display
        self.value_label = QLabel(self._format_value())
        self.value_label.setFont(QFont("Source Code Pro", 14, QFont.Weight.Bold))
        self.value_label.setStyleSheet("color: #1E1E1E; border: none; background: transparent;")
        layout.addWidget(self.value_label)
        layout.addStretch()
    
    def _setup_effects(self):
        """Set up graphics effects for animations."""
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self.opacity_effect)
    
    def _format_value(self) -> str:
        """Format the value for display."""
        if self._value_type == 'bool':
            return 'TRUE' if self._value else 'FALSE'
        if isinstance(self._value, float):
            return f"{self._value:.4f}".rstrip('0').rstrip('.')
        return str(self._value)
    
    @property
    def value(self):
        """The stored value."""
        return self._value
    
    @value.setter
    def value(self, val):
        self._value = val
        self.value_label.setText(self._format_value())
    
    @property
    def value_type(self) -> str:
        """Type identifier for color coding."""
        return self._value_type
    
    def animate_push(self, duration_ms: int = 150):
        """Animate entrance (fade in from transparent).

        Args:
            duration_ms: Animation duration in milliseconds

        Note: We only animate opacity, not position, because the layout
        manager handles positioning. Animating position interferes with
        the layout and causes overlapping items.
        """
        # Start invisible
        self.opacity_effect.setOpacity(0)
        self.show()

        # Fade in animation only
        opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        opacity_anim.setDuration(duration_ms)
        opacity_anim.setStartValue(0.0)
        opacity_anim.setEndValue(1.0)
        opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        opacity_anim.finished.connect(self.animation_finished.emit)
        self._current_animation = opacity_anim
        opacity_anim.start()
    
    def animate_pop(self, duration_ms: int = 150, on_complete=None):
        """Animate exit (highlight amber, then fade out + slide up).
        
        Args:
            duration_ms: Animation duration in milliseconds
            on_complete: Callback function when animation finishes
        """
        # First highlight amber
        self._flash_highlight('#D4A017', duration_ms // 2)
        
        # Then fade out after highlight
        QTimer.singleShot(duration_ms // 2, lambda: self._do_pop_animation(duration_ms, on_complete))
    
    def _do_pop_animation(self, duration_ms: int, on_complete=None):
        """Execute the pop fade-out animation.

        Note: We only animate opacity, not position, to avoid
        interfering with the layout manager.
        """
        # Fade out animation only
        opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        opacity_anim.setDuration(duration_ms)
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.0)
        opacity_anim.setEasingCurve(QEasingCurve.Type.InCubic)

        def on_finished():
            self.animation_finished.emit()
            self.hide()
            self.deleteLater()
            if on_complete:
                on_complete()

        opacity_anim.finished.connect(on_finished)
        self._current_animation = opacity_anim
        opacity_anim.start()
    
    def animate_move_to(self, target_pos: QPoint, duration_ms: int = 300):
        """Animate movement to a new position.
        
        Args:
            target_pos: Target position
            duration_ms: Animation duration
        """
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(duration_ms)
        anim.setStartValue(self.pos())
        anim.setEndValue(target_pos)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.finished.connect(self.animation_finished.emit)
        self._current_animation = anim
        anim.start()
    
    def _flash_highlight(self, color: str, duration_ms: int = 100):
        """Flash a highlight color briefly.
        
        Args:
            color: Highlight color (hex)
            duration_ms: Duration of highlight
        """
        type_color = TYPE_COLORS.get(self._value_type, TYPE_COLORS['int'])
        original_style = f"""
            QFrame {{
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-left: 5px solid {type_color};
                border-radius: 4px;
            }}
        """
        highlight_style = f"""
            QFrame {{
                background-color: {color};
                border: 1px solid {color};
                border-left: 5px solid {color};
                border-radius: 4px;
            }}
        """
        self.setStyleSheet(highlight_style)
        self.value_label.setStyleSheet("color: #1E1E1E; border: none; background: transparent;")
        QTimer.singleShot(duration_ms, lambda: self.setStyleSheet(original_style))
    
    def highlight_consumed(self, enabled: bool = True):
        """Show/hide consumption preview indicator.
        
        Args:
            enabled: Whether to show the indicator
        """
        if enabled:
            self.setStyleSheet("""
                QFrame {
                    background-color: rgba(245, 245, 245, 0.5);
                    border: 2px dashed #808080;
                    border-left: 5px solid #808080;
                    border-radius: 4px;
                }
            """)
        else:
            type_color = TYPE_COLORS.get(self._value_type, TYPE_COLORS['int'])
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: #F5F5F5;
                    border: 1px solid #CCCCCC;
                    border-left: 5px solid {type_color};
                    border-radius: 4px;
                }}
            """)
    
    def pulse(self, duration_ms: int = 200):
        """Pulse animation for DUP-like operations.
        
        Args:
            duration_ms: Duration of pulse
        """
        self._flash_highlight('#4EC9B0', duration_ms)
