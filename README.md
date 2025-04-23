# JPG to PDF Converter

A web application that converts multiple JPG images into a single PDF file. Built with Node.js (frontend) and Flask (backend).

## Features

- Drag and drop interface for uploading JPG images
- Preview of uploaded images
- Convert multiple JPG images into a single PDF
- Modern and responsive UI
- Automatic image scaling to fit PDF pages

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.7 or higher)
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd jpg-to-pdf
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask backend server:
```bash
cd backend
python app.py
```

2. In a new terminal, start the Node.js frontend server:
```bash
npm start
```

3. Open your web browser and navigate to:
```
http://localhost:3000
```

## Usage

1. Drag and drop JPG images into the drop zone or click "Select Files" to choose images
2. Preview your uploaded images
3. Click "Convert to PDF" to generate the PDF
4. The PDF will automatically download to your computer

## Notes

- Only JPG images are supported
- Images are automatically scaled to fit the PDF page while maintaining aspect ratio
- Each image is placed on a separate page in the PDF
- The application supports multiple image uploads at once

## License

MIT 