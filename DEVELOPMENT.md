# Hyper PDF Editor - Architecture & Development Guide

## Project Structure

```
hyper-pdf-editor/
├── src/
│   ├── app.py                    # Application entry point
│   ├── __init__.py              # Package initialization
│   ├── ui/                       # PyQt6 UI layer
│   │   ├── __init__.py
│   │   ├── main_window.py       # Main application window
│   │   ├── editor.py            # PDF editor widget
│   │   ├── viewer.py            # PDF viewer widget
│   │   └── theme.py             # Dark/light theme manager
│   ├── core/                     # Business logic layer
│   │   ├── __init__.py
│   │   ├── pdf_engine.py        # PyMuPDF integration
│   │   └── signature.py         # Digital signature & USB tokens
│   └── resources/               # Static assets
│       ├── icons/              # SVG and PNG icons
│       ├── styles/             # QSS stylesheets
│       └── fonts/              # Custom fonts
├── tests/                        # Unit and integration tests
│   ├── conftest.py
│   └── test_pdf_engine.py
├── .gitignore
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Development dependencies
├── setup.py                     # Package configuration
└── README.md                    # Project documentation
```

## Architecture Overview

### Layered Architecture

1. **UI Layer** (`src/ui/`)
   - PyQt6-based user interface
   - Responsive widgets with VS Code-style theming
   - Multi-tab workspace management
   - Dark/light mode support

2. **Core Layer** (`src/core/`)
   - PDF document handling with PyMuPDF
   - Digital signature management with pyHanko
   - USB token/PKCS#11 integration
   - Cryptographic operations

3. **Entry Point** (`src/app.py`)
   - Application initialization
   - Main loop management

### Key Design Patterns

- **Singleton Pattern**: Theme manager, PDF engine, signature manager
- **Signal/Slot Pattern**: PyQt6 event handling
- **Factory Pattern**: Document creation and tab management
- **Observer Pattern**: Theme change notifications

## Core Modules

### PDF Engine (`src/core/pdf_engine.py`)

Handles PDF document operations:
- Load/close documents
- Render pages to pixmaps
- Extract text
- Add annotations (text, highlights)
- Save documents

```python
from core.pdf_engine import get_pdf_engine

engine = get_pdf_engine()
doc = engine.open_document("file.pdf")
pixmap = doc.get_page_pixmap(0, zoom=1.0)
```

### Signature Manager (`src/core/signature.py`)

Manages digital signatures and USB tokens:
- Load X.509 certificates
- Sign PDF documents
- Manage USB tokens (PKCS#11)
- Validate certificates

```python
from core.signature import get_signature_manager

sig_mgr = get_signature_manager()
sig_mgr.load_certificate("cert.pem", "key.pem")
sig_mgr.sign_pdf("doc.pdf", "signed.pdf", "cert.pem")
```

### Theme Manager (`src/ui/theme.py`)

Provides dark/light mode theming:
- VS Code-inspired color schemes
- Dynamic stylesheet generation
- Theme switching with signals

```python
from ui.theme import get_theme_manager, ThemeMode

theme_mgr = get_theme_manager()
theme_mgr.set_theme(ThemeMode.DARK)
stylesheet = theme_mgr.get_stylesheet()
```

### Main Window (`src/ui/main_window.py`)

Main application window with:
- Menu bar (File, Edit, View, Tools, Help)
- Toolbars (navigation, zoom)
- Tab widget (multi-document support)
- Dock widgets (pages panel)
- Status bar

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/rootkang/hyper-pdf-editor.git
cd hyper-pdf-editor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run application
python src/app.py

# Run tests
pytest tests/
```

### Code Style

- Follow PEP 8
- Use type hints
- Docstrings for all modules, classes, and functions
- Max line length: 100 characters (docstrings)

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_pdf_engine.py::TestPDFEngine::test_engine_initialization
```

## Performance Optimization

### Memory Management

- Lazy load PDF pages
- Cache rendered pixmaps
- Close unused documents
- Optimize pixmap resolution

### Startup Optimization

- Minimize imports at startup
- Use lazy imports for heavy modules
- Preload only essential UI components

### Rendering Optimization

- Use PyMuPDF's hardware acceleration where available
- Cache zoom levels
- Implement page rendering queue

## Security Considerations

- Private keys never stored locally
- USB tokens accessed via secure PKCS#11 interface
- Certificate validation before signing
- No plaintext sensitive data in logs

## Adding New Features

### Example: New Annotation Type

1. **Add to PDF Engine** (`src/core/pdf_engine.py`)
   ```python
   def add_annotation_type(self, page_num, ...):
       # Implementation
       pass
   ```

2. **Add UI Control** (`src/ui/editor.py`)
   ```python
   def enable_annotation_type_mode(self):
       # Update toolbar
       pass
   ```

3. **Connect Signals** (`src/ui/main_window.py`)
   ```python
   action = QAction("New Feature", self)
   action.triggered.connect(self.on_new_feature)
   ```

4. **Write Tests** (`tests/test_*.py`)
   ```python
   def test_new_feature():
       # Test implementation
       pass
   ```

## Deployment

### Windows 11 Optimization

- Use PyInstaller for standalone executable
- Native Windows 11 integration
- Taskbar previews for multi-document support

### macOS Build

- Code signing for distribution
- Apple silicon (M1/M2/M3) support

### Linux Packaging

- AppImage for universal Linux distribution
- Snap package for Ubuntu

## Troubleshooting

### PyQt6 Platform Issues

If you encounter platform-specific issues:
- Set environment variable: `QT_QPA_PLATFORM=offscreen`
- For Linux: `QT_QPA_PLATFORM=xcb`

### PDF Rendering Issues

- Check PyMuPDF version compatibility
- Verify font availability
- Check system graphics drivers

## Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [pyHanko Documentation](https://pyhanko.readthedocs.io/)
- [VS Code Theme Reference](https://code.visualstudio.com/api/references/theme-color)

## License

MIT License - See LICENSE file for details
