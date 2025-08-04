#!/usr/bin/env python3
"""
AI Energy Optimizer - Startup Script
This script starts the FastAPI backend server and provides instructions for the frontend.
"""

import subprocess
import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'scikit-learn',
        'pandas',
        'numpy',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False
    
    return True

def start_backend_server():
    """Start the FastAPI backend server"""
    print("🚀 Starting AI Energy Optimizer Backend...")
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    os.chdir(backend_dir)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def open_frontend():
    """Open the frontend in a web browser"""
    time.sleep(3)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:8000/frontend/index.html')
        print("🌐 Frontend opened in browser")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print("Please open: http://localhost:8000/frontend/index.html")

def main():
    """Main startup function"""
    print("=" * 60)
    print("🔋 AI Energy Optimizer - Smart Home Energy Management")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("✅ All dependencies are satisfied!")
    print()
    
    # Start frontend thread
    frontend_thread = threading.Thread(target=open_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    # Start backend server
    start_backend_server()

if __name__ == "__main__":
    main() 