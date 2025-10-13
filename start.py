#!/usr/bin/env python3
"""
Electrical Component Classifier - Simple Startup Script
"""

import os
import sys
from pathlib import Path

def main():
    print("🔌 Electrical Component Classifier")
    print("=" * 50)
    
    # Get the current directory
    current_dir = Path(__file__).parent
    backend_dir = current_dir / "backend"
    
    # Check if backend directory exists
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Add current directory to Python path
    sys.path.insert(0, str(backend_dir))
    
    print("✅ Starting Flask application...")
    print("🌐 Server will start at: http://localhost:5000")
    print("📱 Open your browser and navigate to the URL above")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
