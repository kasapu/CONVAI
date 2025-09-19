import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { Send, Plus, MessageSquare, LogOut, Settings, User } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { chatAPI } from '../services/api';
import toast from 'react-hot-toast';

const Container = styled.div`
  display: flex;
  height: 100vh;
  background: ${props => props.theme.colors.background};
`;

const Sidebar = styled.div`
  width: 280px;
  background: ${props => props.theme.colors.white};
  border-right: 1px solid ${props => props.theme.colors.border};
  display: flex;
  flex-direction: column;
`;

const SidebarHeader = styled.div`
  padding: ${props => props.theme.spacing.lg};
  border-bottom: 1px solid ${props => props.theme.colors.border};
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const Logo = styled.h1`
  font-size: 1.5rem;
  font-weight: 700;
  color: ${props => props.theme.colors.primary};
  margin: 0;
`;

const UserMenu = styled.div`
  position: relative;
`;

const UserButton = styled.button`
  background: none;
  border: none;
  color: ${props => props.theme.colors.secondary};
  cursor: pointer;
  padding: ${props => props.theme.spacing.sm};
  border-radius: ${props => props.theme.borderRadius};
  
  &:hover {
    background: ${props => props.theme.colors.light};
  }
`;

const NewChatButton = styled.button`
  margin: ${props => props.theme.spacing.md};
  padding: ${props => props.theme.spacing.md};
  background: ${props => props.theme.colors.primary};
  color: ${props => props.theme.colors.white};
  border: none;
  border-radius: ${props => props.theme.borderRadius};
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  font-weight: 600;
  
  &:hover {
    background: #0056b3;
  }
`;

const ConversationsList = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: ${props => props.theme.spacing.sm};
`;

const ConversationItem = styled.div`
  padding: ${props => props.theme.spacing.md};
  margin-bottom: ${props => props.theme.spacing.sm};
  border-radius: ${props => props.theme.borderRadius};
  cursor: pointer;
  background: ${props => props.active ? props.theme.colors.primary : 'transparent'};
  color: ${props => props.active ? props.theme.colors.white : props.theme.colors.dark};
  
  &:hover {
    background: ${props => props.active ? props.theme.colors.primary : props.theme.colors.light};
  }
`;

const ChatArea = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const ChatHeader = styled.div`
  padding: ${props => props.theme.spacing.lg};
  background: ${props => props.theme.colors.white};
  border-bottom: 1px solid ${props => props.theme.colors.border};
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const ChatTitle = styled.h2`
  margin: 0;
  color: ${props => props.theme.colors.dark};
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: ${props => props.theme.spacing.lg};
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const Message = styled.div`
  max-width: 70%;
  padding: ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius};
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  background: ${props => props.isUser ? props.theme.colors.primary : props.theme.colors.white};
  color: ${props => props.isUser ? props.theme.colors.white : props.theme.colors.dark};
  box-shadow: ${props => props.theme.shadows.sm};
  white-space: pre-wrap;
  word-wrap: break-word;
`;

const InputArea = styled.div`
  padding: ${props => props.theme.spacing.lg};
  background: ${props => props.theme.colors.white};
  border-top: 1px solid ${props => props.theme.colors.border};
`;

const InputForm = styled.form`
  display: flex;
  gap: ${props => props.theme.spacing.md};
`;

const MessageInput = styled.textarea`
  flex: 1;
  padding: ${props => props.theme.spacing.md};
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.borderRadius};
  resize: none;
  font-family: inherit;
  font-size: 1rem;
  min-height: 50px;
  max-height: 150px;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
  }
`;

const SendButton = styled.button`
  padding: ${props => props.theme.spacing.md};
  background: ${props => props.theme.colors.primary};
  color: ${props => props.theme.colors.white};
  border: none;
  border-radius: ${props => props.theme.borderRadius};
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    background: #0056b3;
  }
  
  &:disabled {
    background: ${props => props.theme.colors.secondary};
    cursor: not-allowed;
  }
`;

const EmptyState = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: ${props => props.theme.colors.secondary};
`;

const ChatPage = () => {
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const { user, logout } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    if (currentConversation) {
      loadMessages(currentConversation.id);
    }
  }, [currentConversation]);

  const loadConversations = async () => {
    try {
      const response = await chatAPI.getConversations();
      setConversations(response.data);
    } catch (error) {
      toast.error('Failed to load conversations');
    }
  };

  const loadMessages = async (conversationId) => {
    try {
      const response = await chatAPI.getMessages(conversationId);
      setMessages(response.data);
    } catch (error) {
      toast.error('Failed to load messages');
    }
  };

  const createNewChat = async () => {
    try {
      const response = await chatAPI.createConversation({
        title: 'New Conversation',
        ai_model: 'gpt-3.5-turbo'
      });
      
      const newConversation = response.data;
      setConversations(prev => [newConversation, ...prev]);
      setCurrentConversation(newConversation);
      setMessages([]);
    } catch (error) {
      toast.error('Failed to create new conversation');
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || loading) return;

    const messageText = newMessage.trim();
    setNewMessage('');
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage({
        message: messageText,
        conversation_id: currentConversation?.id
      });

      const { conversation_id } = response.data;
      
      // If this was a new conversation, update the current conversation
      if (!currentConversation || currentConversation.id !== conversation_id) {
        await loadConversations();
        const newConv = conversations.find(c => c.id === conversation_id) || 
                        { id: conversation_id, title: messageText.slice(0, 50) + '...' };
        setCurrentConversation(newConv);
      }
      
      // Reload messages to get the latest conversation
      await loadMessages(conversation_id);
    } catch (error) {
      toast.error('Failed to send message');
      setNewMessage(messageText); // Restore the message
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(e);
    }
  };

  return (
    <Container>
      <Sidebar>
        <SidebarHeader>
          <Logo>🤖 CONVAI</Logo>
          <UserMenu>
            <UserButton onClick={logout}>
              <LogOut size={20} />
            </UserButton>
          </UserMenu>
        </SidebarHeader>
        
        <NewChatButton onClick={createNewChat}>
          <Plus size={20} />
          New Chat
        </NewChatButton>
        
        <ConversationsList>
          {conversations.map(conversation => (
            <ConversationItem
              key={conversation.id}
              active={currentConversation?.id === conversation.id}
              onClick={() => setCurrentConversation(conversation)}
            >
              <MessageSquare size={16} style={{ marginRight: '8px', display: 'inline' }} />
              {conversation.title}
            </ConversationItem>
          ))}
        </ConversationsList>
      </Sidebar>

      <ChatArea>
        <ChatHeader>
          <ChatTitle>
            {currentConversation ? currentConversation.title : 'Select a conversation or start a new one'}
          </ChatTitle>
          {user && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <User size={16} />
              {user.username}
            </div>
          )}
        </ChatHeader>

        <MessagesContainer>
          {messages.length === 0 ? (
            <EmptyState>
              <MessageSquare size={64} style={{ marginBottom: '16px' }} />
              <h3>No messages yet</h3>
              <p>Start a conversation by typing a message below</p>
            </EmptyState>
          ) : (
            messages.map(message => (
              <Message key={message.id} isUser={message.role === 'user'}>
                {message.content}
              </Message>
            ))
          )}
          <div ref={messagesEndRef} />
        </MessagesContainer>

        <InputArea>
          <InputForm onSubmit={sendMessage}>
            <MessageInput
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={loading}
            />
            <SendButton type="submit" disabled={loading || !newMessage.trim()}>
              <Send size={20} />
            </SendButton>
          </InputForm>
        </InputArea>
      </ChatArea>
    </Container>
  );
};

export default ChatPage;