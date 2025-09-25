
import os
import sys
import subprocess
import shutil

def check_python_version():
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_requirements():
   
    print("📦 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)

def create_config_file():
    if not os.path.exists("config.py"):
        if os.path.exists("config.example.py"):
            shutil.copy("config.example.py", "config.py")
            print("✅ Created config.py from template")
            print("⚠️  Please edit config.py and add your GEMINI_API_KEY")
        else:
            print("❌ config.example.py not found")
    else:
        print("✅ config.py already exists")

def check_credentials():
    if not os.path.exists("credentials.json"):
        print("⚠️  credentials.json not found")
        print("   Please download your Gmail API credentials and save as credentials.json")
    else:
        print("✅ credentials.json found")

def main():
    print("🚀 Setting up Gmail AI Assistant...")
    print("=" * 50)
    
    check_python_version()
    install_requirements()
    create_config_file()
    check_credentials()
    
    print("=" * 50)
    print("✅ Setup completed!")
    print("\nNext steps:")
    print("1. Edit config.py and add your GEMINI_API_KEY")
    print("2. Download Gmail API credentials as credentials.json")
    print("3. Run 'python server.py' to start the backend")
    print("4. Load the gmail-extension folder in Chrome")

if __name__ == "__main__":
    main()
