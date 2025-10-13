#!/usr/bin/env python3
"""
Electrical Component Classifier - Startup Script
Professional Flask web application for electrical component classification.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed."""
    try:
        import flask
        import torch
        import torchvision
        from PIL import Image
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_model_files():
    """Check if model files exist."""
    model_dir = Path("model")
    model_file = model_dir / "electrical_component_classifier.pth"
    class_map_file = model_dir / "class_map.json"
    
    if not model_file.exists():
        print(f"❌ Model file not found: {model_file}")
        print("Please ensure the model file is in the model/ directory")
        return False
    
    if not class_map_file.exists():
        print(f"❌ Class map file not found: {class_map_file}")
        print("Please ensure the class_map.json file is in the model/ directory")
        return False
    
    print("✅ Model files found")
    return True

def create_upload_directory():
    """Create upload directory if it doesn't exist."""
    upload_dir = Path("backend/static/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    print("✅ Upload directory ready")

def main():
    """Main startup function."""
    print("🔌 Electrical Component Classifier")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend/app.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check model files
    if not check_model_files():
        sys.exit(1)
    
    # Create upload directory
    create_upload_directory()
    
    print("\n🚀 Starting the application...")
    print("=" * 50)
    
    # Change to backend directory and run the app
    os.chdir("backend")
    
    try:
        # Import and run the Flask app
        import sys
        sys.path.append('.')
        from app import app
        print("✅ Application loaded successfully")
        print("🌐 Server starting at: http://localhost:5000")
        print("📱 Open your browser and navigate to the URL above")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
