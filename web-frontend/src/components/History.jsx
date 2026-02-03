import React, { useState, useEffect } from 'react';
import api from '../services/api';

const History = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const response = await api.get('/history/');
            setHistory(response.data);
            setLoading(false);
        } catch (err) {
            console.error("History fetch error:", err);
            setError(err.response?.data?.detail || "Failed to load history");
            setLoading(false);
        }
    };

    if (loading) return (
        <div className="history-loading">
            <div className="loader-ring small"></div>
            <span>Loading history...</span>
        </div>
    );

    if (error) return (
        <div className="history-error">
            <span>⚠️ {error}</span>
        </div>
    );

    return (
        <div className="dashboard-card history-section">
            <div className="card-header">
                <h2 className="flex items-center gap-2">
                    <svg viewBox="0 0 24 24" width="20" height="20">
                        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    Upload History
                </h2>
                {history.length > 0 && (
                    <span className="badge">Last 5 Uploads</span>
                )}
            </div>

            <div className="table-responsive">
                <table className="data-table history-table">
                    <thead>
                        <tr>
                            <th>Batch ID</th>
                            <th>Uploaded At</th>
                            <th>Records</th>
                            <th>Avg Flow</th>
                            <th>Avg Press</th>
                            <th>Avg Temp</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.length === 0 ? (
                            <tr>
                                <td colSpan="6" className="empty-state">
                                    <div className="empty-content">
                                        <svg viewBox="0 0 24 24" width="32" height="32" className="text-white/20 mb-2">
                                            <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" strokeWidth="2" fill="none" />
                                        </svg>
                                        <p>No history yet</p>
                                        <span className="text-sm text-white/40">Upload your first CSV to see it here</span>
                                    </div>
                                </td>
                            </tr>
                        ) : (
                            history.map((batch) => (
                                <tr key={batch.id}>
                                    <td className="batch-id">#{batch.id}</td>
                                    <td>
                                        {new Date(batch.uploaded_at).toLocaleString(undefined, {
                                            month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                                        })}
                                    </td>
                                    <td>
                                        <span className="record-count">
                                            {batch.total_records} rows
                                        </span>
                                    </td>
                                    <td>{batch.avg_flowrate?.toFixed(2)}</td>
                                    <td>{batch.avg_pressure?.toFixed(2)}</td>
                                    <td>{batch.avg_temperature?.toFixed(2)}</td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default History;

