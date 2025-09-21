# -*- coding: utf-8 -*-
"""
BookMap Web Application
A modern web app for indexing PDFs using YOLOv8X-doclaynet and Tesseract OCR
"""

import os
import json
import tempfile
import uuid
import shutil
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, send_file, abort
from werkzeug.utils import secure_filename
import csv
import io
from book_indexer_web_fixed import book_indexer_web as book_indexer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables for processing
processing_status = {}
current_index = {}

def cleanup_old_sessions():
    """Clean up old sessions and their temporary files"""
    try:
        current_time = datetime.now()
        sessions_to_remove = []
        
        for session_id, data in current_index.items():
            created_at = datetime.fromisoformat(data['created_at'])
            if current_time - created_at > timedelta(hours=1):  # 1 hour expiry
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            # Remove from memory
            if session_id in current_index:
                del current_index[session_id]
            if session_id in processing_status:
                del processing_status[session_id]
            
            # Remove temporary files
            temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_{session_id}')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            
            # Remove uploaded file
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if filename.startswith(session_id):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
        
        if sessions_to_remove:
            print(f"Cleaned up {len(sessions_to_remove)} old sessions")
            
    except Exception as e:
        print(f"Error during cleanup: {e}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


def process_pdf_async(pdf_path, session_id):
    """Process PDF asynchronously"""
    try:
        processing_status[session_id] = {"status": "processing", "progress": 0, "message": "Starting processing..."}
        
        # Create temporary directory for this session
        temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_{session_id}')
        os.makedirs(temp_dir, exist_ok=True)
        
        def progress_callback(progress, message):
            processing_status[session_id]["progress"] = progress
            processing_status[session_id]["message"] = message
        
        # Process PDF using the book indexer
        result = book_indexer.process_pdf(pdf_path, temp_dir, progress_callback)
        
        processing_status[session_id]["progress"] = 100
        processing_status[session_id]["status"] = "completed"
        processing_status[session_id]["message"] = "Processing completed!"
        
        # Store results
        current_index[session_id] = {
            "index": result["index"],
            "raw_results": result["raw_results"],
            "num_pages": result["num_pages"],
            "created_at": datetime.now().isoformat()
        }
        
        # Keep processed images for viewing (don't cleanup immediately)
        # Cleanup will happen when session expires or new file is uploaded
        print(f"Session {session_id} completed. Images kept for viewing.")
        
    except Exception as e:
        processing_status[session_id] = {
            "status": "error", 
            "progress": 0, 
            "message": f"Error: {str(e)}"
        }

@app.route('/')
def index():
    """Homepage with upload form"""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return f"BookMap Web Application is running! Error: {e}", 200

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF uploads"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{session_id}_{filename}')
    file.save(file_path)
    
    # Start processing
    if not book_indexer.model:
        return jsonify({'error': 'AI model not loaded'}), 500
    
    # Process in background (in production, use Celery or similar)
    process_pdf_async(file_path, session_id)
    
    return jsonify({
        'session_id': session_id,
        'message': 'File uploaded successfully. Processing started.'
    })

@app.route('/status/<session_id>')
def get_status(session_id):
    """Get processing status"""
    if session_id not in processing_status:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify(processing_status[session_id])

@app.route('/index/<session_id>')
def get_index(session_id):
    """Return structured index JSON"""
    if session_id not in current_index:
        return jsonify({'error': 'Index not found'}), 404
    
    # Cleanup old sessions periodically
    cleanup_old_sessions()
    
    return jsonify(current_index[session_id])

@app.route('/download/<session_id>/<format>')
def download_index(session_id, format):
    """Download index as JSON or CSV"""
    if session_id not in current_index:
        abort(404)
    
    index_data = current_index[session_id]['index']
    
    if format == 'json':
        output = io.StringIO()
        json.dump(index_data, output, indent=2)
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'index_{session_id}.json'
        )
    
    elif format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Page', 'Title'])
        for item in index_data:
            writer.writerow([item['page'], item['title']])
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'index_{session_id}.csv'
        )
    
    else:
        abort(400)

@app.route('/get-page-image/<session_id>/<int:page_number>')
def get_page_image(session_id, page_number):
    """Get processed page image for viewing"""
    if session_id not in current_index:
        print(f"Session {session_id} not found in current_index")
        abort(404)
    
    try:
        # Look for the processed image in the session's temp directory
        temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_{session_id}')
        processed_folder = os.path.join(temp_dir, 'processed')
        converted_folder = os.path.join(temp_dir, 'converted')
        
        print(f"Looking for page {page_number} in session {session_id}")
        print(f"Temp dir: {temp_dir}")
        print(f"Processed folder exists: {os.path.exists(processed_folder)}")
        print(f"Converted folder exists: {os.path.exists(converted_folder)}")
        
        # Try processed images first, then converted images
        image_path = None
        
        if os.path.exists(processed_folder):
            image_path = os.path.join(processed_folder, f'image_{page_number - 1}.jpg')
            print(f"Trying processed image: {image_path}")
            if not os.path.exists(image_path):
                image_path = None
                print("Processed image not found")
        
        if not image_path and os.path.exists(converted_folder):
            image_path = os.path.join(converted_folder, f'image_{page_number - 1}.jpg')
            print(f"Trying converted image: {image_path}")
            if not os.path.exists(image_path):
                image_path = None
                print("Converted image not found")
        
        if image_path and os.path.exists(image_path):
            print(f"Serving image: {image_path}")
            return send_file(image_path, mimetype='image/jpeg')
        else:
            print(f"Image not found for page {page_number}")
            # List available files for debugging
            if os.path.exists(temp_dir):
                print(f"Available files in {temp_dir}:")
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        print(f"  {os.path.join(root, file)}")
            abort(404)
            
    except Exception as e:
        print(f"Error serving page image: {e}")
        import traceback
        traceback.print_exc()
        abort(500)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 50MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({'status': 'healthy', 'message': 'BookMap Web Application is running'}), 200

@app.route('/test')
def test():
    """Simple test endpoint"""
    return "BookMap Web Application is working!", 200

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting BookMap Web Application...")
    
    # Load the AI model on startup
    if book_indexer.load_model():
        print("AI model loaded successfully")
    else:
        print("Warning: AI model could not be loaded")
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    print("Directories created successfully")
    
    # Get port from environment
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    
    # Run in production mode to avoid constant restarts
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"Debug mode: {debug_mode}")
    
    try:
        app.run(debug=debug_mode, host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Failed to start server: {e}")
        raise
