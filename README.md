# Gmail AI Assistant - Browser Extension

A Chrome browser extension that adds an AI-powered email processing button to Gmail. The extension integrates with your existing Python mail automation tool to automatically fetch, process, and send email replies.

## Features

- 🤖 **AI-Powered Email Processing**: Automatically generates professional replies using Google's Gemini AI
- 📧 **Gmail Integration**: Seamlessly integrates with Gmail's interface
- 🎯 **One-Click Processing**: Process all unread emails with a single click
- 📊 **Real-time Statistics**: Track processed emails and success rates
- 🔄 **Background Processing**: Non-blocking email processing
- 🎨 **Modern UI**: Beautiful, responsive design that matches Gmail's aesthetic

## Project Structure

```
mailAutomatioBundle/
├── Extension Files/
│   ├── manifest.json          # Extension configuration
│   ├── content.js             # Gmail interface integration
│   ├── background.js          # Background processing
│   ├── popup.html             # Extension popup UI
│   ├── popup.js               # Popup functionality
│   ├── styles.css             # Extension styling
│   └── icons/                 # Extension icons
├── Python Backend/
│   ├── server.py              # Flask API server
│   ├── main.py                # Original email processing logic
│   ├── openai_reply.py        # AI reply generation
│   ├── gmail_helper.py        # Gmail API helpers
│   ├── auth.py                # Gmail authentication
│   └── requirements.txt       # Python dependencies
└── README.md                  # This file
```

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Chrome Browser** (for the extension)
3. **Gmail Account** with API access
4. **Google Cloud Project** with Gmail API enabled
5. **Google Generative AI API Key** (for Gemini)

## Setup Instructions

### 1. Python Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Gmail API credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download the credentials file and save as `credentials.json` in the project root

3. **Configure AI API Key:**
   - Get your Google Generative AI API key
   - Update the API key in `openai_reply.py`

4. **Generate extension icons (optional):**
   ```bash
   pip install Pillow
   python create_icons.py
   ```

### 2. Chrome Extension Setup

1. **Load the extension in Chrome:**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the folder containing the extension files

2. **Grant permissions:**
   - The extension will request permissions for Gmail and localhost
   - Click "Allow" when prompted

### 3. Start the Server

1. **Run the Flask server:**
   ```bash
   python server.py
   ```
   
   The server will start on `http://localhost:5000`

2. **Verify the server is running:**
   - Open `http://localhost:5000/health` in your browser
   - You should see a JSON response indicating the server is healthy

## Usage

### Using the Extension

1. **Open Gmail** in your Chrome browser
2. **Look for the "AI Assistant" button** in Gmail's toolbar
3. **Click the button** to start processing unread emails
4. **Monitor progress** through the extension popup

### Extension Popup

- **Server Status**: Shows if the Python backend is running
- **Process Emails**: Manually trigger email processing
- **Statistics**: View processed email count and success rate
- **Settings**: Access extension configuration

### API Endpoints

The Flask server provides the following endpoints:

- `GET /health` - Health check
- `POST /process-emails` - Start email processing
- `GET /status` - Get processing status
- `POST /stop` - Stop email processing

## Configuration

### Gmail API Setup

1. **Enable Gmail API:**
   ```bash
   # In Google Cloud Console
   # APIs & Services > Library > Gmail API > Enable
   ```

2. **Create OAuth credentials:**
   - Go to "Credentials" section
   - Create OAuth 2.0 Client ID
   - Set authorized redirect URIs
   - Download and save as `credentials.json`

3. **First-time authentication:**
   - Run `python main.py` once to authenticate
   - This will create `token.json` for future use

### AI Configuration

Update the API key in `openai_reply.py`:
```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```

## Troubleshooting

### Common Issues

1. **"Server Offline" error:**
   - Make sure `python server.py` is running
   - Check if port 5000 is available
   - Verify firewall settings

2. **Authentication errors:**
   - Delete `token.json` and re-authenticate
   - Check if `credentials.json` is valid
   - Ensure Gmail API is enabled

3. **Extension not appearing in Gmail:**
   - Refresh Gmail page
   - Check browser console for errors
   - Verify extension is loaded in Chrome

4. **CORS errors:**
   - Ensure Flask-CORS is installed
   - Check if server is running on correct port

### Debug Mode

Enable debug logging in `server.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## Security Considerations

- **API Keys**: Never commit API keys to version control
- **OAuth Tokens**: Keep `token.json` secure and private
- **Local Server**: The Flask server runs locally for security
- **Permissions**: Extension only requests necessary permissions

## Development

### Adding New Features

1. **Backend**: Modify `main.py` or `server.py`
2. **Frontend**: Update extension files
3. **Testing**: Test both components independently

### File Structure for Development

```
extension/
├── manifest.json
├── content.js
├── background.js
├── popup.html
├── popup.js
├── styles.css
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

## License

This project is for educational and personal use. Please respect Gmail's Terms of Service and API usage limits.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Chrome extension documentation
3. Check Gmail API documentation
4. Verify all dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This extension requires the Python backend to be running locally. The extension communicates with the Flask server to process emails using your existing automation logic. 