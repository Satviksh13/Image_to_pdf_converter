from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os
import io
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    try:
        logger.debug("Received conversion request")
        
        if 'images' not in request.files:
            logger.error("No images key in request.files")
            return jsonify({'error': 'No images provided'}), 400

        images = request.files.getlist('images')
        logger.debug(f"Received {len(images)} images")
        
        if not images:
            logger.error("Empty image list")
            return jsonify({'error': 'No images selected'}), 400

        # Filter out non-image files
        valid_images = [img for img in images if allowed_file(img.filename)]
        logger.debug(f"Found {len(valid_images)} valid images")
        
        if not valid_images:
            logger.error("No valid images found")
            return jsonify({'error': 'No valid images provided. Please upload JPG or PNG files.'}), 400

        # Create a PDF buffer
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        
        for image in valid_images:
            try:
                logger.debug(f"Processing image: {image.filename}")
                
                # Open the image
                img = Image.open(image)
                logger.debug(f"Image mode: {img.mode}, size: {img.size}")
                
                # Convert PNG to RGB if necessary
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    logger.debug(f"Converting {img.mode} to RGB")
                    img = img.convert('RGB')
                
                img_reader = ImageReader(img)
                
                # Get image dimensions
                img_width, img_height = img.size
                
                # Calculate scaling to fit the page
                page_width, page_height = letter
                scale = min(page_width / img_width, page_height / img_height)
                
                # Calculate position to center the image
                x = (page_width - img_width * scale) / 2
                y = (page_height - img_height * scale) / 2
                
                logger.debug(f"Drawing image at ({x}, {y}) with scale {scale}")
                # Draw the image
                c.drawImage(img_reader, x, y, width=img_width * scale, height=img_height * scale)
                c.showPage()
                logger.debug(f"Image {image.filename} added to PDF")
            except Exception as e:
                logger.error(f"Error processing image {image.filename}: {str(e)}")
                logger.error(traceback.format_exc())
                return jsonify({'error': f'Error processing image {image.filename}: {str(e)}'}), 400
        
        logger.debug("Saving PDF")
        c.save()
        pdf_buffer.seek(0)
        logger.debug("PDF created successfully")
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='converted.pdf'
        )
    
    except Exception as e:
        logger.error(f"Error in convert_to_pdf: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    logger.info("Starting Flask server on port 5000")
    app.run(debug=True, port=5000, host='0.0.0.0') 