# BookMap Web Application

A modern web application for automatically indexing PDF documents using AI-powered document layout analysis and OCR technology.

![BookMap Web Application](screenshot.png)

## 🚀 Features

- **AI-Powered Indexing**: Uses YOLOv8X-doclaynet model for intelligent document layout analysis
- **OCR Integration**: Tesseract OCR for text extraction from detected sections
- **Modern Web Interface**: Responsive design with drag-and-drop file upload
- **Real-time Processing**: Live progress updates during document processing
- **PDF Viewer**: View processed pages with detected sections highlighted
- **Multiple Export Formats**: Download results as JSON or CSV
- **Session Management**: Secure file handling with automatic cleanup

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5, jQuery)
- **AI Model**: YOLOv8X-doclaynet for document layout analysis
- **OCR**: Tesseract for text extraction
- **PDF Processing**: pdf2image with Poppler

## 📋 Prerequisites

Before running the application, you need to install the following dependencies:

### System Dependencies

#### Windows
```bash
# Install Poppler (required for PDF processing)
# Download from: https://github.com/oschwartz10612/poppler-windows/releases/
# Extract and add bin folder to PATH

# Install Tesseract OCR (optional, has fallback)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install and add to PATH
```

#### macOS
```bash
brew install poppler tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install poppler-utils tesseract-ocr
```

### Python Dependencies
- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/pranavdhawann/BookMap.git
cd BookMap
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Open Your Browser
Navigate to `http://localhost:5000`

## 📁 Project Structure

```
BookMap/
├── app.py                      # Main Flask application
├── book_indexer_web_fixed.py   # AI processing engine
├── book_indexer_minimal.py     # Minimal version (fallback)
├── templates/
│   └── index.html             # Main web interface
├── static/
│   ├── style.css              # Custom styles
│   └── script.js              # Frontend JavaScript
├── requirements.txt            # Python dependencies
├── Input/                      # Sample PDF files
├── Output/                     # Generated results
└── README.md                   # This file
```

## 🔧 Configuration

The application automatically downloads the YOLOv8X-doclaynet model on first run. No additional configuration is required for basic usage.

### Environment Variables (Optional)
- `FLASK_DEBUG`: Set to `true` for development mode
- `PORT`: Port number for the application (default: 5000)

## 📊 How It Works

1. **Upload**: User uploads a PDF file through the web interface
2. **Conversion**: PDF pages are converted to images using pdf2image
3. **AI Analysis**: YOLOv8X-doclaynet model analyzes document layout
4. **Section Detection**: AI identifies section headers and other document elements
5. **OCR Processing**: Tesseract extracts text from detected sections
6. **Index Generation**: Results are compiled into a structured index
7. **Export**: Users can download results in JSON or CSV format

## 🎯 Usage

1. **Upload a PDF**: Drag and drop or click to select a PDF file
2. **Wait for Processing**: The AI will analyze your document (progress shown in real-time)
3. **View Results**: See the generated index with page numbers and section headers
4. **View Pages**: Click "View" to see the processed PDF pages with detected sections
5. **Download**: Export results as JSON or CSV files

## 📝 API Endpoints

- `GET /`: Main application interface
- `POST /upload`: File upload endpoint
- `GET /status/<session_id>`: Processing status
- `GET /index/<session_id>`: Get processing results
- `GET /get-page-image/<session_id>/<page_number>`: View processed page
- `GET /health`: Health check endpoint
- `GET /test`: Simple test endpoint

## 🐛 Troubleshooting

### Common Issues

#### "Poppler not installed" Error
- **Windows**: Download Poppler from the official releases page and add to PATH
- **macOS**: Run `brew install poppler`
- **Linux**: Run `sudo apt install poppler-utils`

#### "Tesseract not found" Error
- The application will use fallback text generation if Tesseract is not available
- To enable OCR: Install Tesseract and add to PATH

#### Model Download Issues
- The AI model (~2GB) downloads automatically on first run
- Ensure stable internet connection for initial setup
- Model is cached locally after first download

#### Port Already in Use
- Change the port: `set PORT=5001 && python app.py` (Windows)
- Or: `PORT=5001 python app.py` (macOS/Linux)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [YOLOv8X-doclaynet](https://huggingface.co/pranavvdhawann/YOLOv8X-doclaynet) for document layout analysis
- [Ultralytics](https://ultralytics.com/) for YOLO implementation
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text extraction
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub or contact the maintainers.

---

**Made with ❤️ for intelligent document processing**