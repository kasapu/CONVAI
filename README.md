# CONVAI - Conversational AI Platform

🤖 A modern, full-stack conversational AI platform built with FastAPI and React. CONVAI provides a complete solution for building and deploying AI-powered chat applications with user authentication, conversation management, and real-time messaging capabilities.

## ✨ Features

### 🔧 Backend (FastAPI)
- **🔐 JWT Authentication**: Secure user registration and login
- **💬 Conversation Management**: Create, manage, and organize chat sessions
- **🤖 AI Integration**: OpenAI GPT integration with custom system prompts
- **📝 Message History**: Persistent storage of all conversations
- **⚡ Real-time Chat**: WebSocket support for live messaging
- **🗃️ Database Support**: SQLAlchemy with SQLite/PostgreSQL
- **📚 API Documentation**: Auto-generated OpenAPI/Swagger docs
- **🔒 Security**: Password hashing, CORS protection, token validation

### 🎨 Frontend (React)
- **💅 Modern UI**: Clean, responsive interface with styled-components
- **🔄 Real-time Updates**: Live message updates and conversation sync
- **👤 User Management**: Registration, login, and profile management
- **📱 Responsive Design**: Works seamlessly on desktop and mobile
- **🎯 Intuitive UX**: Easy-to-use chat interface with conversation history
- **🔔 Notifications**: Toast notifications for user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Clone and navigate to the project**
   ```bash
   git clone <repository-url>
   cd CONVAI
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the backend server**
   ```bash
   python run_server.py
   ```

   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## 📖 API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token

### Chat & Conversations
- `POST /chat/` - Send a message and get AI response
- `GET /chat/conversations` - Get user's conversations
- `POST /chat/conversations` - Create a new conversation
- `GET /chat/conversations/{id}` - Get specific conversation
- `GET /chat/conversations/{id}/messages` - Get conversation messages
- `PUT /chat/conversations/{id}` - Update conversation
- `WS /chat/ws` - WebSocket endpoint for real-time chat

### System
- `GET /health` - Health check endpoint

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Database Configuration
DATABASE_URL=sqlite:///./convai.db

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### Database Setup

By default, CONVAI uses SQLite for development. For production, configure PostgreSQL:

```env
DATABASE_URL=postgresql://username:password@localhost/convai
```

## 🏗️ Project Structure

```
CONVAI/
├── convai/                 # Backend Python package
│   ├── api/               # FastAPI route handlers
│   ├── core/              # Core configuration and database
│   ├── models/            # SQLAlchemy models and Pydantic schemas
│   ├── services/          # Business logic services
│   └── utils/             # Utility functions
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API service functions
│   │   └── styles/        # CSS and styling
│   └── public/            # Static assets
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Python package configuration
└── run_server.py         # Server startup script
```

## 🐳 Docker Deployment

Create a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "run_server.py"]
```

## 🔧 Development

### Backend Development

```bash
# Install in development mode
pip install -e .

# Run with auto-reload
python run_server.py
```

### Frontend Development

```bash
cd frontend
npm start
```

### Testing

```bash
# Backend tests (if implemented)
pytest

# Frontend tests
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions and support:

1. Check the [API Documentation](http://localhost:8000/docs) for backend details
2. Review the codebase for implementation examples
3. Create an issue for bugs or feature requests

## 🎯 Roadmap

- [ ] Enhanced AI model support (GPT-4, Claude, local models)
- [ ] File upload and processing capabilities
- [ ] Team collaboration features
- [ ] Advanced conversation analytics
- [ ] Plugin system for custom AI tools
- [ ] Mobile app development
- [ ] Enterprise SSO integration

---

**Built with ❤️ using FastAPI and React**