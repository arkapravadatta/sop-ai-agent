import React, { useState } from 'react';

const InputBar = ({ onSend, disabled }) => {
    const [input, setInput] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !disabled) {
            onSend(input.trim());
            setInput('');
        }
    };

    return (
        <form className="input-bar" onSubmit={handleSubmit}>
            <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about sales, revenue, or visualization..."
                disabled={disabled}
            />
            <button type="submit" disabled={disabled || !input.trim()}>
                Send
            </button>
        </form>
    );
};

export default InputBar;
