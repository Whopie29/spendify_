#!/usr/bin/env python3
"""
SPENDIFY Setup Script
Automated setup for the SPENDIFY financial analyzer
"""

import os
import subprocess
import sys

def create_directories():
    """Create necessary directories"""
    dirs = ['uploads', 'static', 'temp']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✓ Created directory: {dir_name}")

def install_requirements():
    """Install Python requirements"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install requirements")
        return False
    return True

def main():
    print("🚀 Setting up SPENDIFY...")
    
    # Create directories
    create_directories()
    
    # Install requirements
    if install_requirements():
        print("\n✅ Setup completed successfully!")
        print("\nTo run the application:")
        print("  Flask version: python app.py")
        print("  Streamlit version: streamlit run web.py")
    else:
        print("\n❌ Setup failed. Please install requirements manually.")

if __name__ == "__main__":
    main()