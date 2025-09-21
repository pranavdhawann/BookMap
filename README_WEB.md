# BookMap Web - AI-Powered PDF Indexing

A modern web application for automatically generating structured indexes from PDF documents using YOLOv8X-doclaynet and Tesseract OCR.

![BookMap Web](https://img.shields.io/badge/BookMap-Web-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red)
![AI](https://img.shields.io/badge/AI-YOLOv8X--doclaynet-purple)

## 🚀 Features

- **Modern Web Interface**: Clean, responsive design with Bootstrap 5
- **Drag & Drop Upload**: Easy PDF file upload with progress tracking
- **AI-Powered Processing**: Uses YOLOv8X-doclaynet for document layout analysis
- **OCR Text Extraction**: Tesseract OCR for section header recognition
- **Interactive Results**: Clickable table of contents with page navigation
- **Multiple Export Formats**: Download indexes as JSON or CSV
- **Real-time Progress**: Live progress updates during processing
- **Error Handling**: Comprehensive error handling and user feedback

## 🏗️ Architecture

### Frontend
- **HTML5/CSS3/JavaScript**: Modern web standards
- **Bootstrap 5**: Responsive UI framework
- **FontAwesome**: Icon library
- **jQuery**: DOM manipulation and AJAX

### Backend
- **Flask**: Python web framework
- **YOLOv8X-doclaynet**: Document layout detection
- **Tesseract OCR**: Text extraction
- **PDF2Image**: PDF to image conversion

### Deployment
- **Railway**: Cloud deployment platform
- **Docker**: Containerization
- **Gunicorn**: WSGI server

## 📁 Project Structure

```
BookMap/
├── app.py                 # Main Flask application
├── book_indexer_web.py    # Refactored indexer for web use
├── book_indexer.py        # Original indexer (Colab version)
├── templates/
│   └── index.html         # Main web interface
├── static/
│   ├── style.css          # Custom styles
│   └── script.js          # Frontend JavaScript
├── temp_uploads/          # Temporary file storage
├── Input/                 # Sample PDF files
├── Output/                # Generated outputs
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment
├── runtime.txt           # Python version
├── Dockerfile            # Docker configuration
├── railway.json          # Railway configuration
├── test_app.py           # Test suite
└── DEPLOYMENT.md         # Deployment guide
```

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Tesseract OCR
- Poppler utilities
- YOLOv8X-doclaynet model file

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BookMap
   ```

2. **Install system dependencies**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install poppler-utils tesseract-ocr
   
   # macOS
   brew install poppler tesseract
   
   # Windows
   # Download from official websites
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   export MODEL_PATH=yolov8x-doclaynet.pt
   export SECRET_KEY=your-secret-key
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser**:
   Navigate to `http://localhost:5000`

## 🚀 Deployment

### Railway Deployment

1. **Prepare your model file**:
   - Place `yolov8x-doclaynet.pt` in the project root
   - Or configure `MODEL_PATH` environment variable

2. **Deploy to Railway**:
   ```bash
   # Option 1: Connect GitHub repository
   # Option 2: Use Railway CLI
   npm install -g @railway/cli
   railway login
   railway init
   railway up
   ```

3. **Set environment variables**:
   - `MODEL_PATH`: Path to your model file
   - `SECRET_KEY`: Secure random string
   - `FLASK_ENV`: `production`

### Docker Deployment

```bash
# Build image
docker build -t bookmap-web .

# Run container
docker run -p 5000:5000 \
  -e MODEL_PATH=yolov8x-doclaynet.pt \
  -e SECRET_KEY=your-secret-key \
  bookmap-web
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python test_app.py
```

The test suite checks:
- Flask app initialization
- Book indexer functionality
- File validation
- Static file presence
- Deployment configuration

## 📖 Usage

1. **Upload PDF**: Drag and drop or click to select a PDF file
2. **Processing**: Watch real-time progress as the AI processes your document
3. **View Results**: Browse the generated table of contents
4. **Download**: Export the index as JSON or CSV
5. **Navigate**: Click on sections to jump to specific pages

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PATH` | Path to YOLOv8X-doclaynet model | `yolov8x-doclaynet.pt` |
| `SECRET_KEY` | Flask secret key | Required |
| `FLASK_ENV` | Flask environment | `development` |
| `PORT` | Server port | `5000` |
| `MAX_CONTENT_LENGTH` | Max upload size | `50MB` |

### Model Configuration

The application uses the following document element classes:
- Section-header (primary for indexing)
- Text, Title, Caption
- List-item, Table, Picture
- Page-header, Page-footer
- Footnote, Formula

## 🎨 UI Design

### Color Scheme
- **Primary**: #4a90e2 (Blue)
- **Secondary**: #ffffff (White)
- **Accent**: #e94e77 (Pink)
- **Background**: #f9f9f9 (Light Gray)
- **Text**: #333333 (Dark Gray)

### Typography
- **Headings**: Roboto, sans-serif
- **Body**: Open Sans, sans-serif

### Components
- Responsive navigation bar
- Drag-and-drop upload area
- Animated progress bar
- Interactive results table
- Download dropdown menu

## 🔍 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Homepage with upload form |
| `POST` | `/upload` | Handle PDF uploads |
| `GET` | `/status/<session_id>` | Get processing status |
| `GET` | `/index/<session_id>` | Get structured index JSON |
| `GET` | `/download/<session_id>/<format>` | Download index (JSON/CSV) |

## 🐛 Troubleshooting

### Common Issues

1. **Model not found**:
   - Ensure model file exists and path is correct
   - Check `MODEL_PATH` environment variable

2. **Tesseract errors**:
   - Install Tesseract OCR system package
   - Set `TESSDATA_PREFIX` if needed

3. **Memory issues**:
   - Reduce file size or use smaller model
   - Increase server memory allocation

4. **Upload failures**:
   - Check file size (max 50MB)
   - Ensure file is valid PDF

### Performance Tips

- Use SSD storage for faster I/O
- Allocate sufficient RAM (4GB+ recommended)
- Enable GPU acceleration if available
- Optimize image processing parameters

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics](https://ultralytics.com/) for YOLOv8
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Flask](https://flask.palletsprojects.com/) web framework
- [Bootstrap](https://getbootstrap.com/) UI framework
- [Railway](https://railway.app/) deployment platform

## 📞 Support

For issues and questions:
1. Check the [troubleshooting section](#-troubleshooting)
2. Review the [deployment guide](DEPLOYMENT.md)
3. Open an issue on GitHub
4. Contact the development team

---

**BookMap Web** - Making document indexing intelligent and accessible! 🚀
