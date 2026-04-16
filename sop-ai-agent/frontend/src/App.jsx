import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import InputBar from './components/InputBar';
import ChartPanel from './components/ChartPanel';
import ReportPanel from './components/ReportPanel';
import { sendChatMessage } from './api/chat';
import './styles/report.css';

function App() {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am your S&OP AI agent. How can I assist you today?' }
    ]);
    const [loading, setLoading] = useState(false);
    const [activeDisplay, setActiveDisplay] = useState(null); // { type: 'chart' | 'report', content: ... }

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
            if (data.chart) {
                setActiveDisplay({ type: 'chart', content: data.chart });
            } else if (data.report) {
                setActiveDisplay({ type: 'report', content: data.report });
            }
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
            <main className="main-layout">
                <div className="chat-area">
                    <ChatWindow messages={messages} />
                    {loading && <div className="loading-indicator">Typing...</div>}
                    <InputBar onSend={handleSend} disabled={loading} />
                </div>
                <div className="chart-area">
                    {activeDisplay ? (
                        activeDisplay.type === 'chart' ? (
                            <ChartPanel spec={activeDisplay.content} />
                        ) : (
                            <ReportPanel markdown={activeDisplay.content} />
                        )
                    ) : (
                        <div className="empty-chart-msg">Graphs or reports will dynamically render here...</div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default App;
