# Gmail Automation Backend

This is the backend service for the Gmail AI Assistant. It provides a REST API for processing emails using Google's Gmail API and Gemini AI.

## 🚀 Quick Start

### Prerequisites

- Python 3.7+ or Docker
- Google Cloud Project with Gmail API enabled
- Google Generative AI API key (Gemini)

### Option 1: Docker Deployment (Recommended)

1. **Prepare your credentials:**
   ```bash
   # Download credentials.json from Google Cloud Console
   # Create config.py from config.example.py
   # Add your GEMINI_API_KEY to config.py
   ```

2. **Deploy with Docker:**
   ```bash
   # Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh
   
   # Windows
   deploy.bat
   ```

3. **Manual Docker deployment:**
   ```bash
   docker-compose up -d
   ```

### Option 2: Local Python Deployment

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up credentials:**
   - Download `credentials.json` from Google Cloud Console
   - Create `config.py` from `config.example.py`
   - Add your `GEMINI_API_KEY`

3. **Run the server:**
   ```bash
   python server.py
   ```

## 📁 Project Structure

```
backend/
├── server.py              # Flask API server
├── main.py                # Email processing logic
├── openai_reply.py        # AI reply generation
├── gmail_helper.py        # Gmail API helpers
├── auth.py                # Gmail authentication
├── setup.py               # Setup utility
├── start.py               # Application starter
├── requirements.txt       # Python dependencies
├── config.example.py      # Configuration template
├── credentials.example    # Credentials format example
├── token.example          # Token format example
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── deploy.sh              # Linux/Mac deployment script
├── deploy.bat             # Windows deployment script
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Generative AI API key
- `FLASK_ENV`: Set to `production` for production deployment

### Configuration Files

1. **config.py** - Main configuration file
2. **credentials.json** - Google OAuth credentials
3. **token.json** - OAuth tokens (generated automatically)

## 🌐 API Endpoints

- `GET /health` - Health check endpoint
- `POST /process-emails` - Start email processing
- `GET /status` - Get processing status
- `POST /stop` - Stop email processing

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t gmail-backend .

# Run with Docker Compose
docker-compose up -d

# Or run directly
docker run -p 5000:5000 \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  -v $(pwd)/config.py:/app/config.py:ro \
  -e GEMINI_API_KEY=your_api_key \
  gmail-backend
```

### Docker Compose Services

- **gmail-backend**: Main application service
- **Health checks**: Automatic health monitoring
- **Volume mounts**: Secure credential mounting
- **Restart policy**: Automatic restart on failure

## 🔒 Security

- Credentials are mounted as read-only volumes
- Non-root user in Docker container
- Environment variables for sensitive data
- Health checks for monitoring

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:5000/health
```

### Logs

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs <container_id>
```

## 🚀 Production Deployment

### Cloud Platforms

1. **Heroku:**
   ```bash
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY=your_key
   git push heroku main
   ```

2. **AWS ECS:**
   - Use the provided Dockerfile
   - Set up ECS service with load balancer
   - Configure environment variables

3. **Google Cloud Run:**
   ```bash
   gcloud run deploy --source .
   ```

### Environment Setup

1. Set production environment variables
2. Use managed databases for tokens (optional)
3. Set up monitoring and logging
4. Configure SSL/TLS certificates

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
python server.py
```

### Testing

```bash
# Run health check
curl http://localhost:5000/health

# Test email processing
curl -X POST http://localhost:5000/process-emails
```

## 📝 Troubleshooting

### Common Issues

1. **Authentication errors:**
   - Check credentials.json format
   - Verify Gmail API is enabled
   - Delete token.json to re-authenticate

2. **Docker issues:**
   - Ensure Docker is running
   - Check port 5000 is available
   - Verify file permissions

3. **API key issues:**
   - Verify GEMINI_API_KEY is set
   - Check API key permissions
   - Ensure billing is enabled

### Debug Mode

```bash
# Enable debug logging
export FLASK_DEBUG=1
python server.py
```

## 📚 Dependencies

- **Flask**: Web framework
- **google-auth**: Google authentication
- **google-api-python-client**: Gmail API client
- **google-generativeai**: Gemini AI integration
- **flask-cors**: CORS support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and personal use. Please respect Gmail's Terms of Service and API usage limits.
