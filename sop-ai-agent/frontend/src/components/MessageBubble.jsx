import React from 'react';
import ChartPanel from './ChartPanel';
import NotificationToast from './NotificationToast';

const MessageBubble = ({ message }) => {
    const { role, content, chart, notification } = message;
    const isUser = role === 'user';

    return (
        <div className={`message-wrapper ${isUser ? 'user-wrapper' : 'assistant-wrapper'}`}>
            <div className={`bubble ${isUser ? 'user-bubble' : 'assistant-bubble'}`}>
                <div className="message-content">{content}</div>
                {chart && <ChartPanel spec={chart} />}
                {notification && <NotificationToast notification={notification} />}
            </div>
        </div>
    );
};

export default MessageBubble;
