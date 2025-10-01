from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import os
from main import run_assistant
import logging

app = Flask(__name__)

# Configure CORS for production
CORS(app, origins=[
    "http://localhost:3000",
    "https://your-frontend-domain.com",
    "chrome-extension://*"  # Allow Chrome extensions
])

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global state
is_processing = False
last_processed_count = 0
last_error = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'is_processing': is_processing,
        'environment': os.getenv('FLASK_ENV', 'development')
    })

@app.route('/process-emails', methods=['POST'])
def process_emails():
    """Process emails endpoint"""
    global is_processing, last_processed_count, last_error
    
    if is_processing:
        return jsonify({
            'success': False,
            'error': 'Already processing emails'
        }), 409
    
    try:
        # Get settings from request
        request_data = request.get_json()
        settings = request_data.get('settings', {}) if request_data else {}
        
        # Extract settings with defaults
        max_emails = int(settings.get('maxEmails', '10'))
        reply_style = settings.get('replyStyle', 'professional')
        custom_prompt = settings.get('customPrompt', '')
        
        logger.info(f"Processing emails with settings: max_emails={max_emails}, reply_style={reply_style}")
        
        is_processing = True
        last_error = None
        
        # Run the email processing in a separate thread to avoid blocking
        def process_emails_thread():
            global is_processing, last_processed_count, last_error
            try:
                logger.info("Starting email processing...")
                
                # Capture the original print function
                import sys
                from io import StringIO
                
                # Redirect stdout to capture output
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                # Run the assistant with settings
                run_assistant(max_emails=max_emails, reply_style=reply_style, custom_prompt=custom_prompt)
                
                # Get the captured output
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout
                
                # Count processed emails (look for "Reply sent!" messages)
                processed_count = output.count("📤 Reply sent!")
                
                last_processed_count = processed_count
                logger.info(f"Email processing completed. Processed {processed_count} emails.")
                
            except Exception as e:
                last_error = str(e)
                logger.error(f"Error processing emails: {e}")
            finally:
                is_processing = False
        
        # Start processing in background thread
        thread = threading.Thread(target=process_emails_thread)
        thread.daemon = True
        thread.start()
        
        # Wait a bit for initial processing
        time.sleep(2)
        
        return jsonify({
            'success': True,
            'message': 'Email processing started',
            'processed_count': last_processed_count
        })
        
    except Exception as e:
        is_processing = False
        last_error = str(e)
        logger.error(f"Error starting email processing: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get processing status"""
    return jsonify({
        'is_processing': is_processing,
        'last_processed_count': last_processed_count,
        'last_error': last_error,
        'timestamp': time.time()
    })

@app.route('/stop', methods=['POST'])
def stop_processing():
    """Stop email processing"""
    global is_processing
    is_processing = False
    return jsonify({
        'success': True,
        'message': 'Processing stopped'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    logger.info("Starting Gmail AI Assistant Server...")
    logger.info(f"Server will be available at http://{host}:{port}")
    logger.info("Make sure you have the required credentials and token files")
    
    try:
        app.run(host=host, port=port, debug=False)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
