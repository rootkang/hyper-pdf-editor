"""
Theme manager for dark/light mode support with VS Code-style aesthetics.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import QObject, pyqtSignal


class ThemeMode(Enum):
    """Available theme modes."""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


@dataclass
class ColorScheme:
    """Color palette for a theme."""
    # Primary colors
    primary: str
    secondary: str
    accent: str
    
    # Backgrounds
    bg_primary: str
    bg_secondary: str
    bg_tertiary: str
    
    # Text
    text_primary: str
    text_secondary: str
    text_disabled: str
    
    # Borders
    border: str
    border_focus: str
    
    # Status
    success: str
    warning: str
    error: str
    info: str
    
    # Editor
    editor_bg: str
    editor_line_number: str
    editor_line_highlight: str
    editor_cursor: str


# VS Code Dark Theme
DARK_SCHEME = ColorScheme(
    primary="#0E639C",
    secondary="#1E1E1E",
    accent="#007ACC",
    
    bg_primary="#1E1E1E",
    bg_secondary="#252526",
    bg_tertiary="#2D2D30",
    
    text_primary="#E0E0E0",
    text_secondary="#858585",
    text_disabled="#6A6A6A",
    
    border="#3E3E42",
    border_focus="#007ACC",
    
    success="#4EC9B0",
    warning="#DCD7B8",
    error="#F48771",
    info="#569CD6",
    
    editor_bg="#1E1E1E",
    editor_line_number="#858585",
    editor_line_highlight="#2D2D30",
    editor_cursor="#AEAFAD",
)

# VS Code Light Theme
LIGHT_SCHEME = ColorScheme(
    primary="#0078D4",
    secondary="#FFFFFF",
    accent="#0078D4",
    
    bg_primary="#FFFFFF",
    bg_secondary="#F3F3F3",
    bg_tertiary="#ECECEC",
    
    text_primary="#333333",
    text_secondary="#6A6A6A",
    text_disabled="#999999",
    
    border="#D0D0D0",
    border_focus="#0078D4",
    
    success="#107C10",
    warning="#FFB900",
    error="#E81123",
    info="#0078D4",
    
    editor_bg="#FFFFFF",
    editor_line_number="#999999",
    editor_line_highlight="#F0F0F0",
    editor_cursor="#000000",
)


class ThemeManager(QObject):
    """Manages application theming."""
    
    theme_changed = pyqtSignal(ThemeMode)
    
    def __init__(self):
        super().__init__()
        self._mode = ThemeMode.DARK
        self._custom_schemes = {}
        self._register_default_schemes()
    
    def _register_default_schemes(self):
        """Register built-in color schemes."""
        self._custom_schemes[ThemeMode.DARK] = DARK_SCHEME
        self._custom_schemes[ThemeMode.LIGHT] = LIGHT_SCHEME
    
    def set_theme(self, mode: ThemeMode):
        """Set the current theme mode."""
        if self._mode != mode:
            self._mode = mode
            self.theme_changed.emit(mode)
    
    def get_theme(self) -> ThemeMode:
        """Get current theme mode."""
        return self._mode
    
    def get_color_scheme(self) -> ColorScheme:
        """Get current color scheme."""
        return self._custom_schemes[self._mode]
    
    def toggle_theme(self):
        """Toggle between dark and light themes."""
        new_mode = ThemeMode.LIGHT if self._mode == ThemeMode.DARK else ThemeMode.DARK
        self.set_theme(new_mode)
    
    def get_stylesheet(self) -> str:
        """Generate QSS stylesheet for current theme."""
        scheme = self.get_color_scheme()
        
        stylesheet = f"""
        QMainWindow {{
            background-color: {scheme.bg_primary};
            color: {scheme.text_primary};
        }}
        
        QWidget {{
            background-color: {scheme.bg_primary};
            color: {scheme.text_primary};
        }}
        
        QMenuBar {{
            background-color: {scheme.bg_secondary};
            color: {scheme.text_primary};
            border-bottom: 1px solid {scheme.border};
        }}
        
        QMenuBar::item:selected {{
            background-color: {scheme.bg_tertiary};
        }}
        
        QMenu {{
            background-color: {scheme.bg_secondary};
            color: {scheme.text_primary};
            border: 1px solid {scheme.border};
        }}
        
        QMenu::item:selected {{
            background-color: {scheme.accent};
        }}
        
        QToolBar {{
            background-color: {scheme.bg_secondary};
            border: none;
            padding: 4px;
        }}
        
        QToolButton {{
            background-color: transparent;
            color: {scheme.text_primary};
            padding: 4px;
            border-radius: 3px;
        }}
        
        QToolButton:hover {{
            background-color: {scheme.bg_tertiary};
        }}
        
        QToolButton:pressed {{
            background-color: {scheme.accent};
        }}
        
        QLineEdit {{
            background-color: {scheme.bg_tertiary};
            color: {scheme.text_primary};
            border: 1px solid {scheme.border};
            border-radius: 3px;
            padding: 4px;
        }}
        
        QLineEdit:focus {{
            border: 1px solid {scheme.border_focus};
        }}
        
        QPushButton {{
            background-color: {scheme.accent};
            color: #FFFFFF;
            border: none;
            border-radius: 3px;
            padding: 6px 12px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {scheme.primary};
        }}
        
        QPushButton:pressed {{
            background-color: {scheme.secondary};
        }}
        
        QDockWidget {{
            color: {scheme.text_primary};
            titlebar-close-icon: url();
        }}
        
        QDockWidget::title {{
            background-color: {scheme.bg_secondary};
            padding: 4px;
            border-bottom: 1px solid {scheme.border};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {scheme.border};
        }}
        
        QTabBar::tab {{
            background-color: {scheme.bg_secondary};
            color: {scheme.text_secondary};
            padding: 4px 12px;
            border-right: 1px solid {scheme.border};
        }}
        
        QTabBar::tab:selected {{
            background-color: {scheme.bg_primary};
            color: {scheme.text_primary};
            border-bottom: 2px solid {scheme.accent};
        }}
        
        QStatusBar {{
            background-color: {scheme.bg_secondary};
            color: {scheme.text_secondary};
            border-top: 1px solid {scheme.border};
        }}
        """
        
        return stylesheet


# Global theme manager instance
_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    """Get or create global theme manager."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
