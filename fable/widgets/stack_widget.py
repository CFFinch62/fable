"""
Animated stack display widget.
The pedagogical centerpiece of FABLE - visualizes stack operations.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QSlider,
    QVBoxLayout, QWidget, QScrollArea
)


# Color scheme
COLORS = {
    'bg_panel': '#252526',
    'bg_container': '#1E1E1E',
    'text_primary': '#D4D4D4',
    'text_secondary': '#808080',
    'accent_amber': '#D4A017',
    'accent_blue': '#2E86AB',
}


class StackWidget(QWidget):
    """Container for animated stack display.
    
    Displays the Data Stack and Return Stack with controls for
    animation speed and step mode.
    
    Signals:
        animation_complete: Emitted when an animation finishes
        step_requested: Emitted when user clicks Step button
        stack_changed(int): Emitted when stack depth changes
    """
    
    animation_complete = pyqtSignal()
    step_requested = pyqtSignal()
    stack_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._animation_speed = 1.0
        self._step_mode = False
        
    def _setup_ui(self):
        """Initialize the user interface."""
        self.setMinimumWidth(250)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_panel']};
                color: {COLORS['text_primary']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Data Stack section
        layout.addWidget(self._create_stack_section("Data Stack"))
        
        # Spacer
        layout.addStretch(1)
        
        # Return Stack section (smaller)
        layout.addWidget(self._create_stack_section("Return Stack", compact=True))
        
        # Controls
        layout.addWidget(self._create_controls())
    
    def _create_stack_section(self, title: str, compact: bool = False) -> QWidget:
        """Create a stack display section.
        
        Args:
            title: Section header text
            compact: If True, use smaller height
        
        Returns:
            QWidget containing the stack section
        """
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        section.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_container']};
                border: 1px solid {COLORS['text_secondary']};
                border-radius: 4px;
            }}
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Header with title and depth
        header = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setFont(QFont("Source Code Pro", 12, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {COLORS['accent_amber']};")
        header.addWidget(title_label)
        
        depth_label = QLabel("(0)")
        depth_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        header.addWidget(depth_label)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Stack items area (scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        items_container = QWidget()
        items_layout = QVBoxLayout(items_container)
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(4)
        items_layout.addStretch()  # Push items to top
        
        scroll.setWidget(items_container)
        layout.addWidget(scroll)
        
        if compact:
            section.setMaximumHeight(150)
        else:
            section.setMinimumHeight(200)
        
        return section
    
    def _create_controls(self) -> QWidget:
        """Create the control panel with speed slider and step button."""
        controls = QWidget()
        layout = QVBoxLayout(controls)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Speed slider
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        speed_layout.addWidget(speed_label)
        
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(25, 400)  # 0.25x to 4.0x
        self.speed_slider.setValue(100)  # 1.0x default
        self.speed_slider.valueChanged.connect(self._on_speed_changed)
        speed_layout.addWidget(self.speed_slider)
        
        self.speed_value = QLabel("1.0x")
        self.speed_value.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.speed_value.setMinimumWidth(35)
        speed_layout.addWidget(self.speed_value)
        
        layout.addLayout(speed_layout)
        
        # Step button
        self.step_button = QPushButton("Step")
        self.step_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_amber']};
                color: {COLORS['bg_container']};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #E5B118;
            }}
            QPushButton:pressed {{
                background-color: #C49015;
            }}
        """)
        self.step_button.clicked.connect(self.step_requested.emit)
        layout.addWidget(self.step_button)
        
        return controls
    
    def _on_speed_changed(self, value: int):
        """Handle speed slider value change."""
        self._animation_speed = value / 100.0
        self.speed_value.setText(f"{self._animation_speed:.1f}x")
    
    @property
    def animation_speed(self) -> float:
        """Current animation speed multiplier."""
        return self._animation_speed
    
    @property
    def step_mode(self) -> bool:
        """Whether step mode is active."""
        return self._step_mode
    
    @step_mode.setter
    def step_mode(self, value: bool):
        self._step_mode = value
        self.step_button.setVisible(value)
