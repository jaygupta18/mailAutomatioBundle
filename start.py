

import os
import sys
import subprocess

def check_config():
    """Check if configuration is properly set up"""
    if not os.path.exists("config.py"):
        print("❌ config.py not found. Please run setup.py first or create config.py manually.")
        return False
    
    # Check if API key is set
    try:
        from config import GEMINI_API_KEY
        if GEMINI_API_KEY == "your_gemini_api_key_here" or not GEMINI_API_KEY:
            print("❌ GEMINI_API_KEY not configured in config.py")
            return False
    except ImportError:
        print("❌ Could not import config.py")
        return False
    
    if not os.path.exists("credentials.json"):
        print("❌ credentials.json not found. Please download your Gmail API credentials.")
        return False
    
    return True

def main():
    """Start the server"""
    print("🚀 Starting Gmail AI Assistant Server...")
    
    if not check_config():
        print("\nPlease fix the configuration issues above and try again.")
        sys.exit(1)
    
    print("✅ Configuration looks good!")
    print("🌐 Starting server on http://localhost:5000")
    print("📧 Make sure to load the Chrome extension from the gmail-extension folder")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the server
        from server import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
