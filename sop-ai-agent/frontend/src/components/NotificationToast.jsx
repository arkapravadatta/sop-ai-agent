import React, { useState } from 'react';

const NotificationToast = ({ notification }) => {
    const [visible, setVisible] = useState(true);

    if (!visible) return null;

    return (
        <div className="notification-toast">
            <span>
                🔔 Notification sent to <strong>{notification.person_in_charge}</strong> ({notification.role}): {notification.message}
            </span>
            <button className="dismiss-btn" onClick={() => setVisible(false)}>×</button>
        </div>
    );
};

export default NotificationToast;
