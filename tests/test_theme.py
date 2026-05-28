"""
Unit tests for theme manager.
"""

import pytest
from ui.theme import ThemeManager, ThemeMode, DARK_SCHEME, LIGHT_SCHEME


class TestThemeManager:
    """Tests for theme manager."""
    
    @pytest.fixture
    def theme_mgr(self):
        """Create theme manager instance."""
        return ThemeManager()
    
    def test_initialization(self, theme_mgr):
        """Test theme manager initializes with dark theme."""
        assert theme_mgr.get_theme() == ThemeMode.DARK
    
    def test_set_theme(self, theme_mgr):
        """Test setting theme mode."""
        theme_mgr.set_theme(ThemeMode.LIGHT)
        assert theme_mgr.get_theme() == ThemeMode.LIGHT
    
    def test_toggle_theme(self, theme_mgr):
        """Test toggling between themes."""
        initial = theme_mgr.get_theme()
        theme_mgr.toggle_theme()
        assert theme_mgr.get_theme() != initial
    
    def test_get_color_scheme_dark(self, theme_mgr):
        """Test getting dark color scheme."""
        theme_mgr.set_theme(ThemeMode.DARK)
        scheme = theme_mgr.get_color_scheme()
        assert scheme.bg_primary == DARK_SCHEME.bg_primary
    
    def test_get_color_scheme_light(self, theme_mgr):
        """Test getting light color scheme."""
        theme_mgr.set_theme(ThemeMode.LIGHT)
        scheme = theme_mgr.get_color_scheme()
        assert scheme.bg_primary == LIGHT_SCHEME.bg_primary
    
    def test_get_stylesheet(self, theme_mgr):
        """Test stylesheet generation."""
        stylesheet = theme_mgr.get_stylesheet()
        assert len(stylesheet) > 0
        assert "QMainWindow" in stylesheet
        assert "background-color" in stylesheet
