# BookMap Web Application

A modern web application for automatically indexing PDF documents using AI-powered document layout analysis and OCR technology.

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
- **Deployment**: Railway (with Docker support)

## 📋 Prerequisites

- Python 3.8+
- Poppler (for PDF processing)
- Tesseract OCR (optional, has fallback)

### Installing Dependencies

#### Windows
```bash
# Install Poppler
# Download from: https://github.com/oschwartz10612/poppler-windows/releases/
# Extract and add bin folder to PATH

# Install Tesseract (optional)
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

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bookmap-web.git
   cd bookmap-web
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
bookmap-web/
├── app.py                      # Main Flask application
├── book_indexer_web_fixed.py   # AI processing engine
├── templates/
│   └── index.html             # Main web interface
├── static/
│   ├── style.css              # Custom styles
│   └── script.js              # Frontend JavaScript
├── requirements.txt            # Python dependencies
├── Procfile                    # Railway deployment config
├── Dockerfile                  # Docker configuration
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

## 🚀 Deployment

### Railway Deployment

1. **Connect to Railway**
   ```bash
   railway login
   railway init
   ```

2. **Deploy**
   ```bash
   railway up
   ```

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t bookmap-web .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 bookmap-web
   ```

## 📝 API Endpoints

- `GET /`: Main application interface
- `POST /upload`: File upload endpoint
- `GET /status/<session_id>`: Processing status
- `GET /index/<session_id>`: Get processing results
- `GET /get-page-image/<session_id>/<page_number>`: View processed page

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