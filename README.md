# BookMap

This project automates the process of indexing books using the [YOLOv8X-doclaynet](https://huggingface.co/pranavvdhawann/YOLOv8X-doclaynet) model hosted on Hugging Face. It processes PDF documents by converting them into images, detecting document elements (such as section headers) using the YOLOv8X model, extracting text via Tesseract OCR, and finally generating a structured index.

![image](https://github.com/user-attachments/assets/dd53fd20-afd9-411c-95b5-eaad98aa751a)

![image](https://github.com/user-attachments/assets/622f3ff2-6d74-49c2-a5f9-0a569890a8ec)

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
  
## Features
- Accepts input in PDF format.
- Converts PDF pages to images.
- Detects document elements using the YOLOv8X-doclaynet model.
- Extracts text using Tesseract OCR.
- Generates a structured index from extracted section headers.
- Reassembles processed images into a PDF.
- Produces three outputs:
  - An output PDF file with processed images.
  - A JSON file containing detection details.
  - A text file containing the generated index.
  
## Requirements
Ensure you have the following installed:
- **Python 3.x**
- **Python Packages** (install via `pip`):
  - ultralytics
  - pdf2image
  - img2pdf
  - Pillow
  - pytesseract
  - json
  - re
  - shutil
- **System Packages**:
  - poppler-utils
  - tesseract-ocr
    
## Setup
1. **Configure Paths and Model:**
   - Update the `root.json` file with:
     - `model_path`: Path to your YOLOv8X-doclaynet model.
     - `test_file_path`: Path to the input PDF file.
     - `output_index_path`: Path to save the generated index text file.
     - `output_json_path`: Path to save the JSON file with detection details.
     - `output_pdf_path`: Path to save the processed PDF.
     - `converted_images_folder`: Directory for storing images converted from PDF.
     - `processed_images_folder`: Directory for storing processed images with detections.
     - `class_names`: List of class names used by the model.
     - `class_colors`: Dictionary of colors for each class.

2. **Download the YOLOv8X-doclaynet Model:**
   Follow the instructions provided in the repository to set up the model.
   Clone the model repository from Hugging Face:
   ```
   git clone https://huggingface.co/pranavvdhawann/YOLOv8X-doclaynet
   ```
   
## Usage
1. Clone the repository:
   ```
    git clone https://github.com/pranavdhawann/BookMap.git
    cd BookMap
   ```
2. Create a virtual environment:
   ```
    python3 -m venv env
    source env/bin/activate  # For Linux and macOS
    env\Scripts\activate  # For Windows
   ```
3. Install dependencies:
   ```
    pip install -r requirements.txt
    sudo apt-get install poppler-utils tesseract-ocr
   ```
4. Run the script:
   ```
    python BookMap.py
   ```
5. Review the Output:
   The processed PDF file, JSON file with detection details, and text file containing the generated index will be saved at the locations specified in       
   root.json.
   
## Future Work
- [ ] Enhanced OCR Accuracy: Improve text extraction quality.
- [ ] Multi-language Support: Extend capabilities for non-English documents.
- [ ] User Interface: Develop a GUI for easier configuration and interaction.

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For suggestions or improvements, feel free to open an issue.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [tesseract](https://github.com/tesseract-ocr/tesseract) for the OCR functionality.
- [Poppler](https://poppler.freedesktop.org/) for PDF processing.
