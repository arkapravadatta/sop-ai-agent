import React from 'react';
import ReactMarkdown from 'react-markdown';

const ReportPanel = ({ markdown }) => {
    if (!markdown) return null;

    return (
        <div className="report-panel">
            <ReactMarkdown>{markdown}</ReactMarkdown>
        </div>
    );
};

export default ReportPanel;
