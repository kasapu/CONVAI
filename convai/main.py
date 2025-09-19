from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from convai.core.config import settings
from convai.core.database import engine, Base
from convai.api import auth, chat
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="CONVAI - Conversational AI Platform",
    description="A modern platform for building and deploying conversational AI applications",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)

# Serve static files if frontend directory exists
if os.path.exists("frontend/build"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint serving basic info or frontend."""
    if os.path.exists("frontend/build/index.html"):
        with open("frontend/build/index.html") as f:
            return HTMLResponse(f.read())
    
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CONVAI - Conversational AI Platform</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; }
            h1 { color: #333; }
            .api-links { margin: 20px 0; }
            .api-links a { display: inline-block; margin: 5px 10px 5px 0; padding: 10px 15px; 
                          background: #007bff; color: white; text-decoration: none; border-radius: 4px; }
            .api-links a:hover { background: #0056b3; }
            .features { list-style-type: none; padding: 0; }
            .features li { padding: 10px 0; border-bottom: 1px solid #eee; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 CONVAI - Conversational AI Platform</h1>
            <p>Welcome to CONVAI, a modern platform for building and deploying conversational AI applications.</p>
            
            <div class="api-links">
                <a href="/docs">📚 API Documentation</a>
                <a href="/redoc">📖 ReDoc</a>
            </div>
            
            <h2>Features</h2>
            <ul class="features">
                <li>🔐 <strong>User Authentication</strong> - Secure JWT-based authentication</li>
                <li>💬 <strong>Conversation Management</strong> - Create and manage chat sessions</li>
                <li>🤖 <strong>AI Integration</strong> - OpenAI GPT integration with custom prompts</li>
                <li>📝 <strong>Message History</strong> - Persistent conversation storage</li>
                <li>⚡ <strong>Real-time Chat</strong> - WebSocket support for live conversations</li>
                <li>🔧 <strong>RESTful API</strong> - Complete REST API for all operations</li>
            </ul>
            
            <h2>Quick Start</h2>
            <ol>
                <li>Register a new user account via <code>POST /auth/register</code></li>
                <li>Login to get an access token via <code>POST /auth/token</code></li>
                <li>Start chatting via <code>POST /chat/</code></li>
            </ol>
            
            <p><em>For detailed API usage, visit the <a href="/docs">API Documentation</a>.</em></p>
        </div>
    </body>
    </html>
    """)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return HTMLResponse(
        content="""
        <html>
        <body>
            <h1>404 - Page Not Found</h1>
            <p>The requested page could not be found.</p>
            <a href="/">Go back to home</a>
        </body>
        </html>
        """,
        status_code=404
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "convai.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )