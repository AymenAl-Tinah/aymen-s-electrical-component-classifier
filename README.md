# 🔌 Electrical Component Classifier

A professional-grade web application for AI-powered electrical component classification using deep learning and computer vision.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎬 Demo Video

https://github.com/user-attachments/assets/Demo%20video%20for%20elec_comp_classifier.mp4

> **Note:** Click the video above to watch the full demonstration of the Electrical Component Classifier in action!

## 🚀 Features

- **AI-Powered Classification**: 18 different electrical component types
- **Professional Web Interface**: Modern, responsive design with smooth animations
- **Drag & Drop Upload**: Intuitive file upload with preview
- **Real-time Predictions**: Fast classification with confidence scores
- **Top Predictions**: Shows top 5 predictions with probabilities
- **Download Results**: Export classification results as JSON
- **Mobile Responsive**: Works seamlessly on desktop
- **Error Handling**: Comprehensive error handling and user feedback
- **Security**: Secure file upload with validation and cleanup

## 📋 Supported Components

The classifier can identify 18 different types of electrical components:

- **Capacitor** - Electronic energy storage components
- **Diode** - Semiconductor devices for current direction
- **IC (Integrated Circuit)** - Complex electronic circuits
- **Inductor** - Energy storage in magnetic fields
- **Integrated-micro-circuit** - Advanced microelectronic devices
- **LED** - Light-emitting diodes
- **Resistor** - Current limiting components
- **Transformer** - Voltage transformation devices
- **Cartridge-fuse** - Circuit protection components
- **Electric-relay** - Electromechanical switches
- **Heat-sink** - Thermal management components
- **Jumper-cable** - Electrical connection wires
- **Memory-chip** - Data storage components
- **Omni-directional-antenna** - Wireless communication devices
- **Potentiometer** - Variable resistance components
- **Solenoid** - Electromagnetic actuators
- **Stabilizer** - Voltage regulation components
- **Transistor** - Semiconductor switching devices

## 🏗️ Project Structure

```
electrical-component-classifier-app/
├── backend/
│   ├── app.py                 # Flask application
│   ├── dep.py                # Prediction logic
│   ├── static/
│   │   ├── uploads/          # Temporary file storage
│   │   ├── style.css         # Main stylesheet
│   │   ├── animations.css    # Advanced animations
│   │   └── app.js           # Client-side JavaScript
│   └── templates/
│       └── index.html         # Main page template
├── model/
│   ├── electrical_component_classifier.pth  # Trained model
│   └── class_map.json       # Class mapping
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd electrical-component-classifier-app
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Model Files

Ensure the following files are present in the `model/` directory:
- `electrical_component_classifier.pth` (trained model weights)
- `class_map.json` (class mapping file)

## 🚀 Running the Application

### Development Mode

```bash
cd backend
python app.py
```

The application will start on `http://localhost:5000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📱 Usage

### Web Interface

1. **Open the Application**: Navigate to `http://localhost:5000`
2. **Upload Image**: Drag and drop or click to select an electrical component image
3. **Preview**: Review the uploaded image
4. **Classify**: Click "Classify Component" to run the AI prediction
5. **View Results**: See the predicted component type with confidence score
6. **Download**: Optionally download the results as JSON

### API Endpoints

#### POST `/predict`
Upload an image for classification.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (image file)

**Response:**
```json
{
  "success": true,
  "class_name": "capacitor",
  "confidence": 0.9649,
  "probabilities": {
    "capacitor": 0.9649,
    "resistor": 0.0234,
    "diode": 0.0117
  },
  "filename": "unique_filename.jpg",
  "original_filename": "component.jpg"
}
```

#### GET `/health`
Check application health and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "num_classes": 18,
  "timestamp": "2025-01-12T10:30:00Z"
}
```

#### GET `/classes`
Get information about available classes.

**Response:**
```json
{
  "success": true,
  "num_classes": 18,
  "classes": ["capacitor", "diode", "ic", ...],
  "class_mapping": {"0": "capacitor", "1": "diode", ...}
}
```

## 🎨 Design Features

### Professional UI/UX
- **Modern Design**: Clean, minimalist interface with professional color palette
- **Smooth Animations**: CSS3 animations and transitions for enhanced user experience
- **Responsive Layout**: Optimized for desktop, tablet, and mobile devices
- **Accessibility**: WCAG compliant with keyboard navigation support

### Visual Elements
- **Color Scheme**: Professional blue and gray palette
- **Typography**: Inter font family for excellent readability
- **Icons**: Font Awesome icons for intuitive navigation
- **Shadows**: Subtle depth and elevation effects
- **Gradients**: Modern gradient backgrounds and effects

### Interactive Features
- **Drag & Drop**: Intuitive file upload with visual feedback
- **Loading States**: Animated spinners and progress indicators
- **Toast Notifications**: Non-intrusive success/error messages
- **Hover Effects**: Smooth hover animations on interactive elements
- **Click Animations**: Satisfying button press feedback

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Model Configuration
MODEL_PATH=../model/electrical_component_classifier.pth
CLASS_MAP_PATH=../model/class_map.json

# Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=static/uploads

# Logging
LOG_LEVEL=INFO
```

### Model Configuration

The application uses a pre-trained ResNet50 model with the following architecture:

- **Backbone**: ResNet50 (frozen)
- **Classifier**: Custom 3-layer fully connected network
- **Input Size**: 128x256 pixels
- **Output**: 18 classes
- **Normalization**: ImageNet mean/std normalization

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-flask pytest-cov

# Run tests
pytest backend/tests/

# Run with coverage
pytest --cov=backend backend/tests/
```

### Test Coverage

The application includes comprehensive tests for:
- API endpoints
- File upload validation
- Model prediction accuracy
- Error handling
- UI interactions

## 🚀 Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]
```

Build and run:

```bash
docker build -t electrical-component-classifier .
docker run -p 5000:5000 electrical-component-classifier
```

### Cloud Deployment

The application can be deployed to various cloud platforms:

- **Heroku**: Use the included `Procfile`
- **AWS**: Deploy using Elastic Beanstalk or ECS
- **Google Cloud**: Use Cloud Run or App Engine
- **Azure**: Deploy using Container Instances or App Service

## 📊 Performance

### Model Performance
- **Accuracy**: 73%+ on test dataset
- **Inference Time**: <2 seconds per image (max)

### Application Performance
- **Response Time**: <3 seconds for classification
- **Concurrent Users**: Supports 10+ simultaneous users
- **File Size Limit**: 16MB maximum
- **Supported Formats**: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP

## 🔒 Security

### Security Features
- **File Validation**: Strict file type and size validation
- **Secure Uploads**: Temporary file storage with automatic cleanup
- **Input Sanitization**: All inputs are sanitized and validated
- **Error Handling**: Comprehensive error handling without information leakage
- **CORS Protection**: Configured for secure cross-origin requests

### Best Practices
- Regular security updates
- Input validation and sanitization
- Secure file handling
- Error logging without sensitive information
- HTTPS enforcement in production

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Run tests: `pytest`
5. Commit changes: `git commit -m "Add new feature"`
6. Push to branch: `git push origin feature/new-feature`
7. Create a Pull Request

### Code Style

The project follows PEP 8 style guidelines:

```bash
# Format code
black backend/

# Check style
flake8 backend/

# Sort imports
isort backend/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 📞 Support

For support, questions, or feature requests:

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the project wiki
- **Email**: [aymnaltynh@gmail.com]

## 🔄 Changelog

### Version 1.0.0 (2025-10-17)
- Initial release
- 18 electrical component classes
- Professional web interface
- REST API endpoints
- Mobile responsive design
- Comprehensive error handling

---

**Built with ❤️ for the electrical engineering community**
