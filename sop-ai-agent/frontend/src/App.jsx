import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import InputBar from './components/InputBar';
import { sendChatMessage } from './api/chat';

function App() {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am your S&OP AI agent. How can I assist you today?' }
    ]);
    const [loading, setLoading] = useState(false);

    const handleSend = async (text) => {
        const userMsg = { role: 'user', content: text };
        setMessages((prev) => [...prev, userMsg]);
        setLoading(true);

        try {
            const data = await sendChatMessage(text);
            const assistantMsg = {
                role: 'assistant',
                content: data.answer,
                chart: data.chart,
                notification: data.notification,
                intent: data.intent
            };
            setMessages((prev) => [...prev, assistantMsg]);
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                { role: 'assistant', content: 'Sorry, there was an error processing your request.' }
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <header className="app-header">
                S&OP AI Agent
            </header>
            <main className="chat-container">
                <ChatWindow messages={messages} />
                {loading && <div className="loading-indicator">Typing...</div>}
                <InputBar onSend={handleSend} disabled={loading} />
            </main>
        </div>
    );
}

export default App;
