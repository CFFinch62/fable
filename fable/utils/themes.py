"""
UI Theme definitions for FABLE.
Provides 8 themes: 4 dark and 4 light.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Theme:
    """Theme color definition."""
    name: str
    is_dark: bool
    
    # Window/panel colors
    background: str
    panel: str
    border: str
    
    # Text colors
    text: str
    text_secondary: str
    text_muted: str
    
    # Accent colors
    accent: str
    accent_hover: str
    
    # Editor colors
    editor_bg: str
    editor_text: str
    editor_selection: str
    editor_current_line: str
    editor_gutter: str
    
    # Syntax colors
    syntax_keyword: str
    syntax_stack: str
    syntax_math: str
    syntax_logic: str
    syntax_output: str
    syntax_number: str
    syntax_string: str
    syntax_comment: str
    syntax_definition: str


# =============================================================================
# Dark Themes
# =============================================================================

DARK_DEFAULT = Theme(
    name="Dark (Default)",
    is_dark=True,
    background="#1E1E1E",
    panel="#252526",
    border="#3C3C3C",
    text="#D4D4D4",
    text_secondary="#808080",
    text_muted="#5A5A5A",
    accent="#0078D4",
    accent_hover="#1C86DB",
    editor_bg="#1E1E1E",
    editor_text="#D4D4D4",
    editor_selection="#264F78",
    editor_current_line="#2D2D2D",
    editor_gutter="#252526",
    syntax_keyword="#C586C0",
    syntax_stack="#569CD6",
    syntax_math="#4EC9B0",
    syntax_logic="#6A9955",
    syntax_output="#D4A017",
    syntax_number="#B5CEA8",
    syntax_string="#CE9178",
    syntax_comment="#6A9955",
    syntax_definition="#DCDCAA",
)

DARK_OCEAN = Theme(
    name="Dark Ocean",
    is_dark=True,
    background="#0D1B2A",
    panel="#1B263B",
    border="#415A77",
    text="#E0E1DD",
    text_secondary="#778DA9",
    text_muted="#415A77",
    accent="#00B4D8",
    accent_hover="#0096C7",
    editor_bg="#0D1B2A",
    editor_text="#E0E1DD",
    editor_selection="#1B4965",
    editor_current_line="#1B263B",
    editor_gutter="#1B263B",
    syntax_keyword="#90E0EF",
    syntax_stack="#48CAE4",
    syntax_math="#00B4D8",
    syntax_logic="#0077B6",
    syntax_output="#FFB703",
    syntax_number="#ADE8F4",
    syntax_string="#CAF0F8",
    syntax_comment="#5E6472",
    syntax_definition="#FFD60A",
)

DARK_FOREST = Theme(
    name="Dark Forest",
    is_dark=True,
    background="#1A1D1C",
    panel="#222725",
    border="#3D4B44",
    text="#D4E6D8",
    text_secondary="#8BA898",
    text_muted="#556B5A",
    accent="#4CAF50",
    accent_hover="#66BB6A",
    editor_bg="#1A1D1C",
    editor_text="#D4E6D8",
    editor_selection="#2E5033",
    editor_current_line="#242827",
    editor_gutter="#222725",
    syntax_keyword="#A5D6A7",
    syntax_stack="#81C784",
    syntax_math="#66BB6A",
    syntax_logic="#4CAF50",
    syntax_output="#FFD54F",
    syntax_number="#C5E1A5",
    syntax_string="#DCEDC8",
    syntax_comment="#627562",
    syntax_definition="#FFF59D",
)

DARK_SUNSET = Theme(
    name="Dark Sunset",
    is_dark=True,
    background="#1C1017",
    panel="#2D1F28",
    border="#4A3A44",
    text="#F5E6E8",
    text_secondary="#B08D95",
    text_muted="#6B5660",
    accent="#FF6B6B",
    accent_hover="#FF8787",
    editor_bg="#1C1017",
    editor_text="#F5E6E8",
    editor_selection="#5C2020",
    editor_current_line="#261A20",
    editor_gutter="#2D1F28",
    syntax_keyword="#FF8FA3",
    syntax_stack="#FF6B6B",
    syntax_math="#FFA07A",
    syntax_logic="#FFB4A2",
    syntax_output="#FFD93D",
    syntax_number="#FFCDB2",
    syntax_string="#FFE5D9",
    syntax_comment="#6D5461",
    syntax_definition="#FFE66D",
)


# =============================================================================
# Light Themes
# =============================================================================

LIGHT_DEFAULT = Theme(
    name="Light (Default)",
    is_dark=False,
    background="#FFFFFF",
    panel="#F3F3F3",
    border="#E0E0E0",
    text="#333333",
    text_secondary="#666666",
    text_muted="#999999",
    accent="#0078D4",
    accent_hover="#106EBE",
    editor_bg="#FFFFFF",
    editor_text="#333333",
    editor_selection="#ADD6FF",
    editor_current_line="#FFFBDD",
    editor_gutter="#F3F3F3",
    syntax_keyword="#AF00DB",
    syntax_stack="#0000FF",
    syntax_math="#007ACC",
    syntax_logic="#098658",
    syntax_output="#795E26",
    syntax_number="#098658",
    syntax_string="#A31515",
    syntax_comment="#008000",
    syntax_definition="#795E26",
)

LIGHT_PAPER = Theme(
    name="Light Paper",
    is_dark=False,
    background="#FAF9F6",
    panel="#F0EDE5",
    border="#DED9CE",
    text="#3C3836",
    text_secondary="#665C54",
    text_muted="#928374",
    accent="#B16286",
    accent_hover="#D3869B",
    editor_bg="#FBF1C7",
    editor_text="#3C3836",
    editor_selection="#D5C4A1",
    editor_current_line="#F2E5BC",
    editor_gutter="#EBDBB2",
    syntax_keyword="#8F3F71",
    syntax_stack="#458588",
    syntax_math="#689D6A",
    syntax_logic="#98971A",
    syntax_output="#D65D0E",
    syntax_number="#689D6A",
    syntax_string="#CC241D",
    syntax_comment="#7C6F64",
    syntax_definition="#B57614",
)

LIGHT_SKY = Theme(
    name="Light Sky",
    is_dark=False,
    background="#F8FBFE",
    panel="#E8F4FC",
    border="#C2DBF0",
    text="#1E3A5F",
    text_secondary="#436F92",
    text_muted="#7BA3C9",
    accent="#3B82F6",
    accent_hover="#2563EB",
    editor_bg="#FFFFFF",
    editor_text="#1E3A5F",
    editor_selection="#BFDBFE",
    editor_current_line="#F0F9FF",
    editor_gutter="#EFF6FF",
    syntax_keyword="#7C3AED",
    syntax_stack="#3B82F6",
    syntax_math="#0891B2",
    syntax_logic="#059669",
    syntax_output="#D97706",
    syntax_number="#059669",
    syntax_string="#DC2626",
    syntax_comment="#64748B",
    syntax_definition="#B45309",
)

LIGHT_MINT = Theme(
    name="Light Mint",
    is_dark=False,
    background="#F5FAF8",
    panel="#E0F2ED",
    border="#B8E0D2",
    text="#1B4D3E",
    text_secondary="#3D6B5A",
    text_muted="#6B9B89",
    accent="#2D9B7A",
    accent_hover="#25836A",
    editor_bg="#FFFFFF",
    editor_text="#1B4D3E",
    editor_selection="#C6F6D5",
    editor_current_line="#F0FFF4",
    editor_gutter="#F0FFF4",
    syntax_keyword="#9F1239",
    syntax_stack="#0D9488",
    syntax_math="#059669",
    syntax_logic="#65A30D",
    syntax_output="#B45309",
    syntax_number="#059669",
    syntax_string="#BE123C",
    syntax_comment="#6B7280",
    syntax_definition="#A16207",
)


# =============================================================================
# Theme Registry
# =============================================================================

THEMES: Dict[str, Theme] = {
    # Dark themes
    "dark_default": DARK_DEFAULT,
    "dark_ocean": DARK_OCEAN,
    "dark_forest": DARK_FOREST,
    "dark_sunset": DARK_SUNSET,
    # Light themes
    "light_default": LIGHT_DEFAULT,
    "light_paper": LIGHT_PAPER,
    "light_sky": LIGHT_SKY,
    "light_mint": LIGHT_MINT,
}

DARK_THEMES = ["dark_default", "dark_ocean", "dark_forest", "dark_sunset"]
LIGHT_THEMES = ["light_default", "light_paper", "light_sky", "light_mint"]


def get_theme(name: str) -> Theme:
    """Get a theme by name."""
    return THEMES.get(name, DARK_DEFAULT)


def get_theme_names() -> list:
    """Get all theme names."""
    return list(THEMES.keys())


def apply_theme(widget, theme: Theme) -> str:
    """Generate stylesheet for a theme.
    
    Returns the complete application stylesheet.
    """
    return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {theme.background};
        }}
        
        /* Panels */
        QWidget {{
            background-color: {theme.panel};
            color: {theme.text};
        }}
        
        /* Splitters */
        QSplitter::handle {{
            background-color: {theme.border};
        }}
        
        /* Tab Widget */
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
        
        /* Text Edit / Editor */
        QPlainTextEdit, QTextEdit {{
            background-color: {theme.editor_bg};
            color: {theme.editor_text};
            border: none;
            selection-background-color: {theme.editor_selection};
        }}
        
        /* Line Edit / Input */
        QLineEdit {{
            background-color: {theme.panel};
            color: {theme.text};
            border: none;
            padding: 8px;
        }}
        
        /* Tree View */
        QTreeView {{
            background-color: {theme.panel};
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
        
        /* Menu */
        QMenuBar {{
            background-color: {theme.panel};
            color: {theme.text};
        }}
        QMenuBar::item:selected {{
            background-color: {theme.accent};
        }}
        QMenu {{
            background-color: {theme.panel};
            color: {theme.text};
            border: 1px solid {theme.border};
        }}
        QMenu::item:selected {{
            background-color: {theme.accent};
        }}
        
        /* Toolbar */
        QToolBar {{
            background-color: {theme.panel};
            border: none;
            spacing: 4px;
        }}
        QToolButton {{
            background-color: transparent;
            color: {theme.text};
            padding: 4px;
            border: none;
        }}
        QToolButton:hover {{
            background-color: {theme.border};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {theme.accent};
            color: white;
        }}
        QStatusBar QLabel {{
            background-color: transparent;
            color: white;
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background-color: {theme.panel};
            width: 12px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {theme.border};
            border-radius: 4px;
            min-height: 20px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar:horizontal {{
            background-color: {theme.panel};
            height: 12px;
        }}
        QScrollBar::handle:horizontal {{
            background-color: {theme.border};
            border-radius: 4px;
            min-width: 20px;
        }}
        
        /* Slider */
        QSlider::groove:horizontal {{
            background-color: {theme.border};
            height: 4px;
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            background-color: {theme.accent};
            width: 16px;
            margin: -6px 0;
            border-radius: 8px;
        }}
    """
