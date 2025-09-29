# 🚀 Lunarbot Document Converter

Convert the Team Task Delegation Framework markdown to professional DOC and PDF formats with style and precision!

## 🛠️ Setup

### 1. Virtual Environment (Already Created!)
```bash
# Virtual environment is already set up at .venv
# Dependencies are already installed!
```

### 2. Verify Installation
```bash
# Activate virtual environment (if not already active)
source .venv/Scripts/activate  # On Windows with Git Bash
# or
.venv\Scripts\activate.bat     # On Windows Command Prompt

# Check if packages are installed
python -c "import docx, weasyprint, markdown2; print('✅ All packages installed!')"
```

## 🎯 Usage

### 🎮 Interactive Mode (Recommended!)
```bash
# Just run without arguments - it will ask you what to convert!
python convert_all.py

# This will:
# 1. 📁 Scan the folder for all markdown files
# 2. 🎯 Let you choose which file to convert
# 3. 📋 Let you choose the output format (DOC, PDF, or both)
# 4. 🚀 Convert with beautiful progress display
```

### Quick Start Options
```bash
# Interactive mode (same as above)
python convert_all.py

# Or use the Windows batch script
convert.bat
```

### Advanced Usage
```bash
# Interactive file selection but specify format
python convert_all.py --format doc     # Choose file, convert to DOC only
python convert_all.py --format pdf     # Choose file, convert to PDF only

# Specify input file directly (skips file selection)
python convert_all.py --input my_document.md

# Batch mode - convert ALL markdown files found
python convert_all.py --batch

# Batch mode with specific format
python convert_all.py --batch --format pdf

# Specify output directory
python convert_all.py --output-dir ./outputs

# Verbose mode (show detailed info)
python convert_all.py --verbose

# Force interactive mode (even if input is specified)
python convert_all.py --input some.md --interactive

# Get help
python convert_all.py --help
```

### Individual Converters
```bash
# Use specific converters directly
python convert_to_doc.py    # Creates .docx file
python convert_to_pdf.py    # Creates .pdf file
```

## 📁 Output Files

After conversion, you'll get:
- `Team_Task_Delegation_Framework.docx` - Professional Word document
- `Team_Task_Delegation_Framework.pdf` - Beautifully formatted PDF

## 🎨 Features

### 🎮 Interactive Mode Features
- ✅ **Smart File Detection**: Automatically scans for .md, .markdown, .mdown, .mkd files
- ✅ **Beautiful File Browser**: Shows file size, modification time, and easy selection
- ✅ **Format Selection**: Choose DOC only, PDF only, or both formats
- ✅ **Batch Processing**: Convert all markdown files at once
- ✅ **Progress Tracking**: Real-time conversion progress with detailed feedback
- ✅ **Error Handling**: Graceful error handling with helpful suggestions

### DOC Converter
- ✅ Professional Microsoft Word formatting
- ✅ Custom styles and colors
- ✅ Proper heading hierarchy
- ✅ Bullet points and lists
- ✅ Bold/italic text preservation
- ✅ Team member sections highlighted

### PDF Converter
- ✅ Beautiful CSS styling
- ✅ Professional typography
- ✅ Page headers and footers
- ✅ Proper page breaks
- ✅ Color-coded sections
- ✅ Table of contents ready
- ✅ Print-optimized layout

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# If you get import errors, reinstall packages
pip install -r requirements.txt
```

#### 2. WeasyPrint Issues on Windows
```bash
# Install Visual C++ Build Tools or use conda
conda install -c conda-forge weasyprint
```

#### 3. PDFKit Issues
```bash
# PDFKit requires wkhtmltopdf (but we use WeasyPrint instead)
# If you want to use PDFKit, install wkhtmltopdf from:
# https://wkhtmltopdf.org/downloads.html
```

#### 4. Virtual Environment Issues
```bash
# Recreate virtual environment if needed
rm -rf .venv                    # Delete old environment
python -m venv .venv           # Create new one
source .venv/Scripts/activate  # Activate it
pip install -r requirements.txt # Reinstall packages
```

## 🚀 Example Output

```
╔════════════════════════════════════════════════════════════════╗
║                   🚀 LUNARBOT CONVERTER 🚀                     ║
║              Smart India Hackathon Document Converter         ║
║                                                                ║
║    Converting Markdown → DOC & PDF like a space-age wizard!   ║
╚════════════════════════════════════════════════════════════════╝

📁 Input file: Team_Task_Delegation_Framework.md
📂 Output directory: .
🎯 Format(s): both
⏰ Started at: 2025-09-27 15:30:45
════════════════════════════════════════════════════════════════

📝 Converting to DOC format...
   Output: Team_Task_Delegation_Framework.docx
✅ Successfully converted to DOC

📋 Converting to PDF format...
   Output: Team_Task_Delegation_Framework.pdf
✅ Successfully converted to PDF

════════════════════════════════════════════════════════════════
🎯 CONVERSION SUMMARY
════════════════════════════════════════════════════════════════
DOC: ✅ SUCCESS
     📄 Team_Task_Delegation_Framework.docx
PDF: ✅ SUCCESS
     📄 Team_Task_Delegation_Framework.pdf

🏆 2/2 conversions successful!
🎉 All conversions completed successfully!
🌙 Ready for lunar mission documentation! 🚀
⏰ Completed at: 2025-09-27 15:31:02
```

## 📋 Dependencies

- `python-docx` - Microsoft Word document creation
- `weasyprint` - HTML/CSS to PDF conversion
- `markdown2` - Markdown parsing with extras
- `reportlab` - PDF generation utilities
- `pypandoc` - Universal document converter (backup)

## 🎯 File Structure

```
Lunarbot/
├── .venv/                              # Virtual environment
├── Team_Task_Delegation_Framework.md   # Source markdown
├── convert_all.py                      # Main converter script
├── convert_to_doc.py                   # DOC converter
├── convert_to_pdf.py                   # PDF converter
├── convert.bat                         # Windows batch script
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── Team_Task_Delegation_Framework.docx # Generated DOC
└── Team_Task_Delegation_Framework.pdf  # Generated PDF
```

## 🌟 Pro Tips

1. **Batch Processing**: Use `convert.bat` on Windows for one-click conversion
2. **Custom Styling**: Modify CSS in `convert_to_pdf.py` for different PDF styles
3. **Team Collaboration**: Share the generated PDFs for team review
4. **Version Control**: Keep both markdown and generated files in sync
5. **Professional Docs**: Use DOC format for collaborative editing
6. **Presentation**: Use PDF format for final presentations and printing

## 🚀 Ready for Launch!

Your lunar robotics documentation is now ready for mission-critical use!

**Bas ek hi baat hai** - we've converted your research dreams into professional documents that even NASA would approve! 🌙✨

---

*Made with 🤖 love for the Smart India Hackathon lunar robotics team!*
