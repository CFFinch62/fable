"""
Individual stack item widget.
Displays a single value with type indicator and animation support.
"""

from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel


# Type indicator colors
TYPE_COLORS = {
    'int': '#569CD6',
    'float': '#6A9955', 
    'addr': '#D4A017',
    'string': '#C586C0',
    'bool': '#4EC9B0',
}


class StackItemWidget(QFrame):
    """Visual representation of a single stack value.
    
    Displays the value with a colored type indicator strip on the left.
    Supports animations for push, pop, and movement.
    
    Attributes:
        value: The stored value
        value_type: Type identifier ('int', 'float', 'addr', 'string', 'bool')
    """
    
    def __init__(self, value, value_type: str = "int", parent=None):
        super().__init__(parent)
        self._value = value
        self._value_type = value_type
        self._opacity = 1.0
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        self.setFixedHeight(36)
        self.setMinimumWidth(100)
        
        type_color = TYPE_COLORS.get(self._value_type, TYPE_COLORS['int'])
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-left: 4px solid {type_color};
                border-radius: 4px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Value display
        self.value_label = QLabel(self._format_value())
        self.value_label.setFont(QFont("Source Code Pro", 14))
        self.value_label.setStyleSheet("color: #1E1E1E; border: none;")
        layout.addWidget(self.value_label)
        layout.addStretch()
    
    def _format_value(self) -> str:
        """Format the value for display."""
        if self._value_type == 'bool':
            return 'TRUE' if self._value else 'FALSE'
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
    
    # Opacity property for animation
    def get_opacity(self) -> float:
        return self._opacity
    
    def set_opacity(self, value: float):
        self._opacity = value
        self.setWindowOpacity(value)
    
    opacity = pyqtProperty(float, get_opacity, set_opacity)
    
    def animate_in(self, duration_ms: int = 150):
        """Animate entrance (fade in + slide down).
        
        Args:
            duration_ms: Animation duration in milliseconds
        """
        # Start above and invisible
        start_pos = self.pos() - QPoint(0, 20)
        end_pos = self.pos()
        
        # Position animation
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(duration_ms)
        self.pos_anim.setStartValue(start_pos)
        self.pos_anim.setEndValue(end_pos)
        self.pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.pos_anim.start()
    
    def animate_out(self, duration_ms: int = 150):
        """Animate exit (fade out + slide up).
        
        Args:
            duration_ms: Animation duration in milliseconds
        """
        end_pos = self.pos() - QPoint(0, 20)
        
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(duration_ms)
        self.pos_anim.setStartValue(self.pos())
        self.pos_anim.setEndValue(end_pos)
        self.pos_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self.pos_anim.finished.connect(self.deleteLater)
        self.pos_anim.start()
    
    def highlight(self, color: str = "#D4A017", duration_ms: int = 100):
        """Flash highlight color.
        
        Args:
            color: Highlight color (hex)
            duration_ms: Highlight duration
        """
        original_style = self.styleSheet()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border: 1px solid #CCCCCC;
                border-left: 4px solid {color};
                border-radius: 4px;
            }}
        """)
        # Would use QTimer to revert, but keeping simple for now
