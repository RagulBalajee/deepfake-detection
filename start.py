#!/usr/bin/env python3
"""
Startup script for the AI-Powered Fake News & Deepfake Detection System
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        sys.exit(1)
    print("✅ Python version:", sys.version.split()[0])

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import torch
        import transformers
        import cv2
        import librosa
        print("✅ Core dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def setup_environment():
    """Set up environment variables"""
    env_file = Path("env.example")
    if env_file.exists() and not Path(".env").exists():
        print("📝 Creating .env file from template...")
        with open("env.example", "r") as f:
            content = f.read()
        with open(".env", "w") as f:
            f.write(content)
        print("✅ Environment file created. Please edit .env with your API keys.")

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting backend server...")
    try:
        # Start the server
        subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "app:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], cwd="backend")
        print("✅ Backend server started on http://localhost:8000")
        return True
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the frontend development server"""
    print("🌐 Starting frontend server...")
    try:
        # Start a simple HTTP server
        subprocess.Popen([
            sys.executable, "-m", "http.server", "8001"
        ], cwd="frontend")
        print("✅ Frontend server started on http://localhost:8001")
        return True
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False

def open_browser():
    """Open the application in the browser"""
    time.sleep(3)  # Wait for servers to start
    print("🌐 Opening application in browser...")
    webbrowser.open("http://localhost:8001/enhanced.html")
    print("✅ Application opened in browser")

def main():
    """Main startup function"""
    print("🔍 AI-Powered Fake News & Deepfake Detection System")
    print("=" * 60)
    
    # Check Python version
    check_python_version()
    
    # Check and install dependencies
    if not check_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Start backend
    if not start_backend():
        print("❌ Failed to start backend")
        sys.exit(1)
    
    # Start frontend
    if not start_frontend():
        print("❌ Failed to start frontend")
        sys.exit(1)
    
    # Open browser
    open_browser()
    
    print("\n🎉 System is running!")
    print("📊 Backend API: http://localhost:8000")
    print("🌐 Frontend: http://localhost:8001/enhanced.html")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n💡 Press Ctrl+C to stop the servers")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
