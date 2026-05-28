"""
Main application window for Hyper PDF Editor.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, List
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QFileDialog, QMessageBox, QDockWidget, QListWidget, QListWidgetItem,
    QLabel, QLineEdit, QPushButton, QStatusBar, QToolBar, QMenu
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from ui.editor import PDFEditor
from ui.viewer import PDFViewer
from ui.theme import get_theme_manager, ThemeMode
from core.pdf_engine import get_pdf_engine, PDFDocument
from core.signature import get_signature_manager


logger = logging.getLogger(__name__)


class HyperPDFEditor(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hyper PDF Editor")
        self.setGeometry(100, 100, 1400, 900)
        
        self.pdf_engine = get_pdf_engine()
        self.theme_manager = get_theme_manager()
        self.signature_manager = get_signature_manager()
        
        # Document tabs
        self.tabs: Dict[str, PDFEditor] = {}
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Setup UI
        self.setup_ui()
        self.create_menus()
        self.create_toolbars()
        self.create_status_bar()
        self.create_dock_widgets()
        
        # Apply theme
        self.apply_theme()
        self.theme_manager.theme_changed.connect(self.apply_theme)
        
        logger.info("Main window initialized")
    
    def setup_ui(self):
        """Setup main UI."""
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def create_menus(self):
        """Create application menus."""
        # File menu
        file_menu = self.menuBar().addMenu("File")
        
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = self.menuBar().addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(redo_action)
        
        # View menu
        view_menu = self.menuBar().addMenu("View")
        
        theme_action = QAction("Toggle Theme (Dark/Light)", self)
        theme_action.setShortcut("Ctrl+Shift+T")
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        # Tools menu
        tools_menu = self.menuBar().addMenu("Tools")
        
        sign_action = QAction("Sign Document", self)
        sign_action.triggered.connect(self.sign_document)
        tools_menu.addAction(sign_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbars(self):
        """Create application toolbars."""
        # Navigation toolbar
        nav_toolbar = self.addToolBar("Navigation")
        nav_toolbar.setObjectName("NavigationToolbar")
        nav_toolbar.setIconSize(QSize(20, 20))
        
        self.prev_page_btn = QPushButton("← Previous")
        self.prev_page_btn.clicked.connect(self.previous_page)
        nav_toolbar.addWidget(self.prev_page_btn)
        
        self.page_label = QLabel("Page 0/0")
        nav_toolbar.addWidget(self.page_label)
        
        self.next_page_btn = QPushButton("Next →")
        self.next_page_btn.clicked.connect(self.next_page)
        nav_toolbar.addWidget(self.next_page_btn)
    
    def create_status_bar(self):
        """Create status bar."""
        self.statusBar().showMessage("Ready")
    
    def create_dock_widgets(self):
        """Create dock widgets."""
        # Pages panel
        pages_dock = QDockWidget("Pages", self)
        pages_dock.setObjectName("PagesDock")
        self.pages_list = QListWidget()
        pages_dock.setWidget(self.pages_list)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, pages_dock)
    
    def open_file(self):
        """Open PDF file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if file_path:
            try:
                document = self.pdf_engine.open_document(file_path)
                self.add_document_tab(file_path, document)
                self.statusBar().showMessage(f"Opened: {Path(file_path).name}")
                logger.info(f"Opened file: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open PDF: {e}")
                logger.error(f"Failed to open PDF: {e}")
    
    def add_document_tab(self, file_path: str, document: PDFDocument):
        """Add document tab."""
        tab_name = Path(file_path).name
        editor = PDFEditor()
        editor.load_document(document)
        
        self.tabs[tab_name] = editor
        tab_index = self.tab_widget.addTab(editor, tab_name)
        self.tab_widget.setCurrentIndex(tab_index)
        
        # Update pages list
        self.update_pages_list(document)
    
    def close_tab(self, index: int):
        """Close a document tab."""
        if 0 <= index < self.tab_widget.count():
            tab_name = self.tab_widget.tabText(index)
            if tab_name in self.tabs:
                del self.tabs[tab_name]
            self.tab_widget.removeTab(index)
    
    def get_current_editor(self) -> Optional[PDFEditor]:
        """Get current active editor."""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            return self.tab_widget.currentWidget()
        return None
    
    def save_file(self):
        """Save current document."""
        editor = self.get_current_editor()
        if editor:
            if editor.save_document():
                self.statusBar().showMessage("Document saved")
                logger.info("Document saved")
    
    def save_file_as(self):
        """Save current document as new file."""
        editor = self.get_current_editor()
        if not editor:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            if editor.save_document(file_path):
                self.statusBar().showMessage(f"Saved: {Path(file_path).name}")
    
    def previous_page(self):
        """Go to previous page."""
        editor = self.get_current_editor()
        if editor:
            editor.viewer.previous_page()
            self.update_page_label()
    
    def next_page(self):
        """Go to next page."""
        editor = self.get_current_editor()
        if editor:
            editor.viewer.next_page()
            self.update_page_label()
    
    def update_page_label(self):
        """Update page label in toolbar."""
        editor = self.get_current_editor()
        if editor:
            current = editor.viewer.get_current_page() + 1
            total = editor.viewer.get_page_count()
            self.page_label.setText(f"Page {current}/{total}")
    
    def update_pages_list(self, document: PDFDocument):
        """Update pages list widget."""
        self.pages_list.clear()
        for i in range(document.get_page_count()):
            item = QListWidgetItem(f"Page {i + 1}")
            item.setData(Qt.ItemDataRole.UserRole, i)
            self.pages_list.addItem(item)
    
    def toggle_theme(self):
        """Toggle between dark and light themes."""
        self.theme_manager.toggle_theme()
    
    def apply_theme(self):
        """Apply current theme."""
        stylesheet = self.theme_manager.get_stylesheet()
        self.setStyleSheet(stylesheet)
    
    def sign_document(self):
        """Sign current document."""
        editor = self.get_current_editor()
        if not editor:
            QMessageBox.warning(self, "No Document", "Please open a PDF first")
            return
        
        # Placeholder for signing dialog
        QMessageBox.information(self, "Sign Document", 
                              "Signature feature coming soon!")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Hyper PDF Editor",
            "Hyper PDF Editor v0.1.0\n\n"
            "A modern, lightweight PDF editor with digital signatures.\n\n"
            "© 2026 rootkang"
        )
