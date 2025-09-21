# -*- coding: utf-8 -*-
"""
BookMap Web - Minimal version for deployment
This version provides basic functionality without heavy ML dependencies
"""

import os
import json
import re
import shutil
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
import pytesseract

class BookIndexerMinimal:
    """Minimal book indexer for web application"""
    
    def __init__(self):
        """Initialize with basic configuration"""
        self.class_names = [
            "Caption", "Footnote", "Formula", "List-item", "Page-footer",
            "Page-header", "Picture", "Section-header", "Table", "Text", "Title"
        ]
        self.class_colors = {
            "Caption": [255, 0, 0],
            "Footnote": [0, 255, 0],
            "Formula": [0, 0, 255],
            "List-item": [255, 255, 0],
            "Page-footer": [255, 165, 0],
            "Page-header": [128, 0, 128],
            "Picture": [0, 255, 255],
            "Section-header": [255, 0, 255],
            "Table": [75, 0, 130],
            "Text": [0, 128, 0],
            "Title": [128, 128, 128]
        }
    
    def get_mock_section_header(self, page_num):
        """Generate mock section headers based on page number"""
        mock_headers = [
            "Introduction",
            "Overview",
            "Getting Started",
            "Basic Concepts",
            "Advanced Topics",
            "Implementation",
            "Examples",
            "Best Practices",
            "Troubleshooting",
            "Conclusion"
        ]
        return mock_headers[page_num % len(mock_headers)]
    
    def clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        
        return text
    
    def process_pdf(self, pdf_path, temp_base_dir, progress_callback=None):
        """Process PDF with minimal functionality"""
        try:
            # Create temporary directories
            converted_images_folder = os.path.join(temp_base_dir, 'converted')
            processed_images_folder = os.path.join(temp_base_dir, 'processed')
            
            os.makedirs(converted_images_folder, exist_ok=True)
            os.makedirs(processed_images_folder, exist_ok=True)
            
            # Convert PDF to images
            if progress_callback:
                progress_callback(10, "Converting PDF to images...")
            
            images = convert_from_path(pdf_path, dpi=200)
            num_pages = len(images)
            
            # Save converted images
            for i, image in enumerate(images):
                image_path = os.path.join(converted_images_folder, f'image_{i}.jpg')
                image.save(image_path, 'JPEG', quality=85)
            
            if progress_callback:
                progress_callback(30, "Processing images...")
            
            # Process images with mock detection
            results = self.process_images_minimal(converted_images_folder, processed_images_folder, progress_callback)
            
            if progress_callback:
                progress_callback(90, "Generating index...")
            
            # Generate index
            index = self.generate_index(results)
            
            if progress_callback:
                progress_callback(100, "Processing complete!")
            
            return {
                "index": index,
                "raw_results": results,
                "num_pages": num_pages
            }
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {e}")
    
    def process_images_minimal(self, input_folder, output_folder, progress_callback=None):
        """Process images with mock detection"""
        results = []
        image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]
        
        for i, filename in enumerate(image_files):
            if progress_callback:
                progress = 30 + (i / len(image_files)) * 50
                progress_callback(progress, f"Processing page {i+1}...")
            
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)
            
            # Create mock detections
            mock_detections = self.create_mock_detections(image, i)
            
            # Draw mock detections on image
            processed_image = self.draw_detections(image, mock_detections)
            
            # Save processed image
            output_path = os.path.join(output_folder, filename)
            processed_image.save(output_path, 'JPEG', quality=85)
            
            results.append({
                "filename": filename,
                "detections": mock_detections
            })
        
        return results
    
    def create_mock_detections(self, image, page_num):
        """Create mock detections for demonstration"""
        width, height = image.size
        
        # Create mock section headers
        detections = []
        
        # Add a mock section header
        section_header = {
            "class": "Section-header",
            "confidence": 0.95,
            "bbox": [50, 50, width-50, 100],
            "text": self.get_mock_section_header(page_num)
        }
        detections.append(section_header)
        
        # Add mock text blocks
        for i in range(3):
            y_start = 120 + (i * 150)
            y_end = y_start + 100
            text_block = {
                "class": "Text",
                "confidence": 0.85,
                "bbox": [50, y_start, width-50, y_end],
                "text": f"Sample text content for page {page_num + 1}, paragraph {i + 1}."
            }
            detections.append(text_block)
        
        return detections
    
    def draw_detections(self, image, detections):
        """Draw detections on image"""
        draw = ImageDraw.Draw(image)
        
        for detection in detections:
            class_name = detection["class"]
            bbox = detection["bbox"]
            confidence = detection["confidence"]
            
            # Get color for this class
            color = tuple(self.class_colors.get(class_name, [255, 255, 255]))
            
            # Draw bounding box
            draw.rectangle(bbox, outline=color, width=2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            draw.text((bbox[0], bbox[1] - 20), label, fill=color)
        
        return image
    
    def generate_index(self, results):
        """Generate index from results"""
        index = []
        
        for result in results:
            filename = result["filename"]
            page_num = int(filename.split("_")[1].split(".")[0]) + 1
            
            for detection in result["detections"]:
                if detection["class"] == "Section-header":
                    section_text = detection["text"]
                    if section_text:
                        index.append({
                            "page": page_num,
                            "section": section_text,
                            "confidence": detection["confidence"]
                        })
        
        return index

# Global instance
book_indexer_minimal = BookIndexerMinimal()
