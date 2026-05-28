# Hyper PDF Editor

A modern, lightweight desktop PDF editor built with Python and PyQt6. Fast startup, low RAM usage, and enterprise-grade features.

## ✨ Features

- **Fast PDF Reader** - Smooth rendering with multi-page support
- **PDF Editing** - Add text, annotations, and shapes
- **Digital Signatures** - Sign PDFs with certificates and USB tokens
- **USB Token Support** - PKCS#11 compatible hardware security modules
- **Dark/Light Mode** - Adaptive theming with system integration
- **VS Code-style UI** - Modern command palette and sidebar navigation
- **Multi-tab Workspace** - Seamlessly work with multiple documents
- **Professional Design** - Apple-style red PDF icon and enterprise aesthetics

## 🚀 Performance

- **Fast Startup** - Optimized for < 2s launch time
- **Low RAM Usage** - Efficient memory management, ~150MB base
- **Smooth Rendering** - Hardware-accelerated where possible
- **Windows 11 Optimized** - Native OS integration

## 🛠️ Tech Stack

- **UI Framework**: PyQt6
- **PDF Processing**: PyMuPDF (fitz)
- **Digital Signatures**: pyHanko
- **Cryptography**: cryptography
- **Hardware Tokens**: pycryptoki

## 📋 Requirements

- Python 3.10+
- PyQt6 >= 6.5.0
- PyMuPDF >= 1.23.0
- pyHanko >= 0.24.0
- cryptography >= 41.0.0
- pycryptoki >= 5.5.0

## 🏗️ Architecture

```
hyper-pdf-editor/
├── src/
│   ├── ui/                    # PyQt6 UI components
│   │   ├── main_window.py    # Main application window
│   │   ├── editor.py         # PDF editor widget
│   │   ├── viewer.py         # PDF viewer widget
│   │   ├── theme.py          # Dark/Light theme manager
│   │   └── dialogs.py        # Modal dialogs
│   ├── core/                  # Core business logic
│   │   ├── pdf_engine.py     # PDF manipulation
│   │   ├── signature.py      # Digital signature handling
│   │   ├── token.py          # USB token integration
│   │   └── document.py       # Document model
│   ├── resources/             # Static assets
│   │   ├── icons/            # SVG and PNG icons
│   │   ├── styles/           # QSS stylesheets
│   │   └── fonts/            # Custom fonts
│   └── app.py                # Application entry point
├── tests/                     # Unit and integration tests
├── requirements.txt           # Python dependencies
└── setup.py                  # Package configuration
```

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/rootkang/hyper-pdf-editor.git
cd hyper-pdf-editor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Run directly
python src/app.py

# Or install as package
pip install -e .
hyper-pdf-editor
```

## 📖 Usage

### Opening a PDF
1. Click **File** → **Open** or press `Ctrl+O`
2. Select a PDF file from your system

### Adding Annotations
1. Select the annotation tool from the toolbar
2. Click and drag on the PDF to create annotations
3. Use the properties panel to customize

### Digital Signatures
1. Go to **Tools** → **Sign Document**
2. Select your certificate or USB token
3. Click to place signature on page
4. Save the signed PDF

### Theme Selection
- Press `Ctrl+Shift+T` to toggle dark/light mode
- Or use **Settings** → **Appearance**

### Command Palette
- Press `Ctrl+Shift+P` to open command palette
- Type to search and execute commands

## 🔐 Security

- All signature operations use industry-standard cryptography
- USB tokens accessed via secure PKCS#11 interface
- Private keys never stored locally
- Compliant with PDF/A and PDF/X standards

## 🤝 Contributing

Contributions welcome! Please follow our code style and submit PRs with tests.

## 📄 License

MIT License - see LICENSE file for details

## 👥 Author

Created by [rootkang](https://github.com/rootkang)

---

**Made with ❤️ for the modern PDF workflow**
