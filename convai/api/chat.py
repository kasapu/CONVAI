from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from convai.core.database import get_db
from convai.models.database import User
from convai.models.schemas import (
    ChatRequest, ChatResponse, ConversationCreate, Conversation, 
    ConversationUpdate, Message
)
from convai.services.conversation import ConversationService
from convai.api.dependencies import get_current_active_user
import json

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Send a message and get AI response."""
    service = ConversationService(db)
    try:
        response = await service.chat_with_ai(chat_request, current_user)
        return ChatResponse(**response)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/conversations", response_model=Conversation)
async def create_conversation(
    conversation: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new conversation."""
    service = ConversationService(db)
    return service.create_conversation(current_user, conversation)

@router.get("/conversations", response_model=List[Conversation])
async def get_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for the current user."""
    service = ConversationService(db)
    return service.get_user_conversations(current_user)

@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific conversation."""
    service = ConversationService(db)
    conversation = service.get_conversation(conversation_id, current_user)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.get("/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get messages for a conversation."""
    service = ConversationService(db)
    conversation = service.get_conversation(conversation_id, current_user)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return service.get_conversation_messages(conversation_id)

@router.put("/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(
    conversation_id: int,
    conversation_update: ConversationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a conversation."""
    service = ConversationService(db)
    conversation = service.get_conversation(conversation_id, current_user)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Update fields
    for field, value in conversation_update.dict(exclude_unset=True).items():
        setattr(conversation, field, value)
    
    db.commit()
    db.refresh(conversation)
    return conversation

# WebSocket endpoint for real-time chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time chat."""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Here you would typically authenticate the user via token
            # For simplicity, we'll skip authentication in WebSocket for now
            
            # Process the chat request
            # This is a simplified version - in production you'd want proper auth
            await manager.send_personal_message(
                json.dumps({"message": f"Echo: {message_data.get('message', '')}"}),
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)