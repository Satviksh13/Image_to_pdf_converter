const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const PDFDocument = require('pdfkit');
const sharp = require('sharp');
const app = express();

// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Make sure uploads directory exists
if (!fs.existsSync('uploads')) {
    fs.mkdirSync('uploads');
}

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({ 
    storage: storage,
    fileFilter: function(req, file, cb) {
        const filetypes = /jpeg|jpg|png/;
        const mimetype = filetypes.test(file.mimetype);
        const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
        
        if (mimetype && extname) {
            return cb(null, true);
        }
        cb("Error: Only JPG and PNG images are allowed!");
    }
});

// Serve static files
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));

// Routes
app.get('/', (req, res) => {
    res.render('index');
});

app.post('/convert', upload.array('images'), async (req, res) => {
    try {
        if (!req.files || req.files.length === 0) {
            return res.status(400).send('No images uploaded');
        }

        // Create a PDF document
        const doc = new PDFDocument({
            autoFirstPage: false,
            margin: 0
        });

        // Set the response headers
        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', 'attachment; filename=converted.pdf');

        // Pipe the PDF to the response
        doc.pipe(res);

        // Process each uploaded image
        for (const file of req.files) {
            try {
                // Read image with sharp
                const image = await sharp(file.path)
                    .toBuffer({ resolveWithObject: true });
                
                const { data, info } = image;
                
                // Add a new page with the image dimensions
                doc.addPage({
                    size: [info.width, info.height],
                    margin: 0
                });
                
                // Add the image to the PDF
                doc.image(data, 0, 0, {
                    width: info.width,
                    height: info.height
                });
                
            } catch (err) {
                console.error(`Error processing image ${file.filename}:`, err);
            }
        }

        // Finalize the PDF
        doc.end();

        // Clean up uploaded files
        for (const file of req.files) {
            fs.unlinkSync(file.path);
        }
    } catch (error) {
        console.error('Error details:', error.message);
        res.status(500).send('Error converting images to PDF');
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.status(200).send('OK');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 