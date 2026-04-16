import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';

const ChatWindow = ({ messages }) => {
    const endOfMessagesRef = useRef(null);

    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="chat-window">
            {messages.map((msg, idx) => (
                <MessageBubble key={idx} message={msg} />
            ))}
            <div ref={endOfMessagesRef} />
        </div>
    );
};

export default ChatWindow;
