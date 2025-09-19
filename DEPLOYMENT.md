# CONVAI Development and Deployment Guide

## Development Setup

### Using Virtual Environment

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run the server**
   ```bash
   python run_server.py
   ```

### Using Docker

1. **Build and run with docker-compose**
   ```bash
   docker-compose up --build
   ```

2. **Environment variables**
   Create a `.env` file for docker-compose:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   SECRET_KEY=your_secret_key_here
   ```

## Production Deployment

### Docker Production Setup

1. **Create production docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     convai:
       image: convai:latest
       ports:
         - "80:8000"
       environment:
         - DATABASE_URL=postgresql://user:pass@db:5432/convai
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - SECRET_KEY=${SECRET_KEY}
         - DEBUG=false
         - HOST=0.0.0.0
         - PORT=8000
       restart: always
   ```

2. **Use a reverse proxy (nginx)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Frontend Production Build

1. **Build the React app**
   ```bash
   cd frontend
   npm run build
   ```

2. **Serve with the FastAPI backend**
   The backend is configured to serve the built React app from `/frontend/build/`

## API Testing

### Using curl

```bash
# Register a user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass"}'

# Login
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass"

# Send a chat message (replace TOKEN with actual token)
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"message": "Hello, AI!"}'
```

### Using the API docs

Visit `http://localhost:8000/docs` for interactive API documentation.

## Database Management

### SQLite (Development)
- Database file: `convai.db`
- No setup required

### PostgreSQL (Production)
```bash
# Create database
createdb convai

# Set DATABASE_URL
export DATABASE_URL="postgresql://username:password@localhost/convai"
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install dependencies with `pip install -r requirements.txt`
2. **Database errors**: Check DATABASE_URL and ensure database exists
3. **CORS errors**: Add your frontend URL to ALLOWED_ORIGINS in config
4. **OpenAI errors**: Verify OPENAI_API_KEY is set correctly

### Logging

Enable debug logging:
```env
DEBUG=true
```

Check logs in docker:
```bash
docker-compose logs convai-backend
```

## Performance Optimization

### Production Settings

```env
DEBUG=false
WORKERS=4  # Number of uvicorn workers
```

### Database Optimization

For PostgreSQL production:
```env
DATABASE_URL=postgresql://user:pass@host:5432/convai?pool_size=20&max_overflow=0
```

## Security Considerations

1. **Change default SECRET_KEY** in production
2. **Use HTTPS** with proper SSL certificates
3. **Restrict CORS origins** to your domain only
4. **Use environment variables** for sensitive data
5. **Regular security updates** for dependencies

## Monitoring

### Health Checks

```bash
curl http://localhost:8000/health
```

### Application Metrics

Consider adding:
- Prometheus metrics
- Application logging
- Error tracking (Sentry)
- Uptime monitoring