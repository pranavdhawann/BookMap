# Use Python slim image
FROM python:3.11-slim

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install only essential Python packages first
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    Flask==2.3.3 \
    gunicorn==21.2.0 \
    pdf2image==1.16.3 \
    Pillow==10.0.0 \
    pytesseract==0.3.10 \
    requests==2.31.0 \
    numpy==1.24.3 \
    PyYAML==6.0.1 \
    && pip cache purge

# Copy application files
COPY app.py .
COPY book_indexer_minimal.py .
COPY templates/ templates/
COPY static/ static/

# Create directories
RUN mkdir -p temp_uploads

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "300", "app:app"]