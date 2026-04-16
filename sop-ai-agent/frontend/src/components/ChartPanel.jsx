import React from 'react';
import Plot from 'react-plotly.js';

const ChartPanel = ({ spec }) => {
    if (!spec) return null;
    
    return (
        <div className="chart-panel">
            <Plot
                data={spec.data}
                layout={{ ...spec.layout, autosize: true }}
                useResizeHandler={true}
                style={{ width: "100%", height: "100%" }}
            />
        </div>
    );
};

export default ChartPanel;
