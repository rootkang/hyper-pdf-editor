"""
PDF Viewer widget for displaying PDF pages.
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtGui import QPixmap, QImage, Qt
from PyQt6.QtCore import pyqtSignal, QSize
from core.pdf_engine import PDFDocument


logger = logging.getLogger(__name__)


class PDFViewer(QWidget):
    """PyQt6 widget for displaying PDF pages."""
    
    page_changed = pyqtSignal(int)  # Emitted when page changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.document: Optional[PDFDocument] = None
        self.current_page = 0
        self.zoom_level = 1.0
        
        # Setup UI
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #1E1E1E; padding: 10px;")
        
        self.scroll_area.setWidget(self.image_label)
        self.layout.addWidget(self.scroll_area)
    
    def load_document(self, document: PDFDocument):
        """Load a PDF document."""
        self.document = document
        self.current_page = 0
        self.display_page(0)
    
    def display_page(self, page_num: int):
        """Display a specific page."""
        if not self.document:
            return
        
        if page_num < 0 or page_num >= self.document.get_page_count():
            logger.warning(f"Invalid page number: {page_num}")
            return
        
        try:
            self.current_page = page_num
            pixmap = self.document.get_page_pixmap(page_num, self.zoom_level)
            
            # Convert PyMuPDF pixmap to QImage
            img_data = pixmap.tobytes("ppm")
            qimage = QImage()
            qimage.loadFromData(img_data, "PPM")
            
            qpixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(qpixmap)
            self.page_changed.emit(page_num)
            
        except Exception as e:
            logger.error(f"Failed to display page {page_num}: {e}")
    
    def next_page(self):
        """Go to next page."""
        if self.document and self.current_page < self.document.get_page_count() - 1:
            self.display_page(self.current_page + 1)
    
    def previous_page(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.display_page(self.current_page - 1)
    
    def go_to_page(self, page_num: int):
        """Go to specific page."""
        self.display_page(page_num)
    
    def set_zoom(self, zoom_level: float):
        """Set zoom level and redisplay."""
        if zoom_level > 0:
            self.zoom_level = zoom_level
            self.display_page(self.current_page)
    
    def zoom_in(self):
        """Zoom in by 20%."""
        self.set_zoom(self.zoom_level * 1.2)
    
    def zoom_out(self):
        """Zoom out by 20%."""
        self.set_zoom(self.zoom_level / 1.2)
    
    def fit_to_width(self):
        """Fit page to window width."""
        if self.scroll_area.width() > 0 and self.document:
            pixmap = self.document.get_page_pixmap(self.current_page, 1.0)
            zoom = self.scroll_area.width() / pixmap.width
            self.set_zoom(zoom)
    
    def get_current_page(self) -> int:
        """Get current page number."""
        return self.current_page
    
    def get_page_count(self) -> int:
        """Get total page count."""
        return self.document.get_page_count() if self.document else 0
