import openai
import json
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from convai.core.config import settings
from convai.models.database import Conversation, Message, User
from convai.models.schemas import ConversationCreate, MessageCreate, ChatRequest

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY

class ConversationService:
    """Service for managing conversations and AI interactions."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_conversation(self, user: User, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            title=conversation_data.title,
            user_id=user.id,
            ai_model=conversation_data.ai_model,
            system_prompt=conversation_data.system_prompt
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def get_conversation(self, conversation_id: int, user: User) -> Optional[Conversation]:
        """Get a conversation by ID for a specific user."""
        return self.db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id
        ).first()
    
    def get_user_conversations(self, user: User, limit: int = 50) -> List[Conversation]:
        """Get all conversations for a user."""
        return self.db.query(Conversation).filter(
            Conversation.user_id == user.id,
            Conversation.is_active == True
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()
    
    def add_message(self, conversation_id: int, role: str, content: str, metadata: Optional[Dict] = None) -> Message:
        """Add a message to a conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            message_metadata=json.dumps(metadata) if metadata else None
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_conversation_messages(self, conversation_id: int, limit: int = 100) -> List[Message]:
        """Get messages for a conversation."""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).limit(limit).all()
    
    async def chat_with_ai(self, chat_request: ChatRequest, user: User) -> Dict[str, Any]:
        """Process a chat request and get AI response."""
        # Get or create conversation
        if chat_request.conversation_id:
            conversation = self.get_conversation(chat_request.conversation_id, user)
            if not conversation:
                raise ValueError("Conversation not found")
        else:
            # Create new conversation
            conversation_data = ConversationCreate(
                title=chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message,
                ai_model=chat_request.ai_model,
                system_prompt=chat_request.system_prompt
            )
            conversation = self.create_conversation(user, conversation_data)
        
        # Add user message
        user_message = self.add_message(
            conversation.id,
            "user",
            chat_request.message
        )
        
        # Get conversation history
        messages = self.get_conversation_messages(conversation.id)
        
        # Prepare messages for OpenAI
        openai_messages = []
        if conversation.system_prompt:
            openai_messages.append({"role": "system", "content": conversation.system_prompt})
        
        for msg in messages:
            openai_messages.append({"role": msg.role, "content": msg.content})
        
        try:
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=chat_request.ai_model or conversation.ai_model,
                messages=openai_messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to conversation
            ai_message = self.add_message(
                conversation.id,
                "assistant",
                ai_response,
                {"model": chat_request.ai_model or conversation.ai_model}
            )
            
            return {
                "message": ai_response,
                "conversation_id": conversation.id,
                "message_id": ai_message.id
            }
            
        except Exception as e:
            # Handle API errors
            error_message = f"Sorry, I encountered an error: {str(e)}"
            ai_message = self.add_message(
                conversation.id,
                "assistant",
                error_message,
                {"error": True, "error_type": type(e).__name__}
            )
            
            return {
                "message": error_message,
                "conversation_id": conversation.id,
                "message_id": ai_message.id
            }