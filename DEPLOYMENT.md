# BookMap Web - Deployment Guide

## Railway Deployment

### Prerequisites
1. A Railway account (sign up at [railway.app](https://railway.app))
2. Your YOLOv8X-doclaynet model file (`yolov8x-doclaynet.pt`)
3. Git repository with your BookMap Web code

### Step 1: Prepare Your Repository

1. **Upload your model file**: Place your `yolov8x-doclaynet.pt` file in the root directory of your project.

2. **Set environment variables**: Create a `.env` file (or set in Railway dashboard):
   ```
   MODEL_PATH=yolov8x-doclaynet.pt
   SECRET_KEY=your-secure-secret-key-here
   FLASK_ENV=production
   ```

### Step 2: Deploy to Railway

#### Option A: Deploy from GitHub
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the `Dockerfile` and deploy
3. Set environment variables in Railway dashboard

#### Option B: Deploy with Railway CLI
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Initialize project: `railway init`
4. Deploy: `railway up`

### Step 3: Configure Environment Variables

In Railway dashboard, set these environment variables:
- `MODEL_PATH`: `yolov8x-doclaynet.pt`
- `SECRET_KEY`: A secure random string
- `FLASK_ENV`: `production`
- `PORT`: `5000` (Railway sets this automatically)

### Step 4: Upload Model File

Since the model file is large, you have several options:

1. **Include in repository** (if under 100MB):
   - Add `yolov8x-doclaynet.pt` to your repository
   - Railway will include it in the build

2. **Use external storage**:
   - Upload to cloud storage (AWS S3, Google Cloud, etc.)
   - Download during deployment in `Dockerfile`

3. **Use Railway volumes**:
   - Create a volume in Railway
   - Upload model file to the volume

### Step 5: Verify Deployment

1. Check Railway logs for successful startup
2. Visit your Railway URL
3. Test PDF upload functionality

## Local Development

### Prerequisites
- Python 3.11+
- Tesseract OCR
- Poppler utilities

### Installation

1. **Clone repository**:
   ```bash
   git clone <your-repo-url>
   cd BookMap
   ```

2. **Install system dependencies**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install poppler-utils tesseract-ocr
   
   # macOS
   brew install poppler tesseract
   
   # Windows
   # Download and install from official websites
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

## Docker Deployment

### Build and Run Locally
```bash
# Build image
docker build -t bookmap-web .

# Run container
docker run -p 5000:5000 \
  -e MODEL_PATH=yolov8x-doclaynet.pt \
  -e SECRET_KEY=your-secret-key \
  bookmap-web
```

### Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  bookmap:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MODEL_PATH=yolov8x-doclaynet.pt
      - SECRET_KEY=your-secret-key
    volumes:
      - ./yolov8x-doclaynet.pt:/app/yolov8x-doclaynet.pt
```

## Troubleshooting

### Common Issues

1. **Model not found**:
   - Ensure `yolov8x-doclaynet.pt` is in the correct location
   - Check `MODEL_PATH` environment variable

2. **Tesseract not found**:
   - Install Tesseract OCR system package
   - Set `TESSDATA_PREFIX` if needed

3. **Memory issues**:
   - Reduce batch size in model processing
   - Use smaller model variant
   - Increase Railway plan memory

4. **Upload timeout**:
   - Increase timeout in Railway settings
   - Optimize image processing
   - Use background job processing

### Performance Optimization

1. **Model caching**: The model is loaded once at startup
2. **Image optimization**: Images are processed in batches
3. **Memory management**: Temporary files are cleaned up automatically
4. **Error handling**: Comprehensive error handling and user feedback

## Monitoring

### Railway Metrics
- Monitor CPU and memory usage
- Check deployment logs
- Set up alerts for errors

### Application Logs
- Flask logs are available in Railway dashboard
- Error tracking for debugging
- Performance metrics

## Security Considerations

1. **File upload limits**: 50MB maximum file size
2. **File type validation**: Only PDF files accepted
3. **Temporary file cleanup**: Automatic cleanup after processing
4. **Environment variables**: Secure secret key management
5. **CORS**: Configured for web application use

## Scaling

### Horizontal Scaling
- Use Railway's auto-scaling features
- Implement Redis for session storage
- Use external file storage for uploads

### Vertical Scaling
- Upgrade Railway plan for more resources
- Optimize model processing
- Implement caching strategies

## Support

For issues and questions:
1. Check Railway documentation
2. Review application logs
3. Test locally first
4. Contact support with specific error messages
