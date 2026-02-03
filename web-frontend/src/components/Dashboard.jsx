import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getDashboardStats, downloadPDF } from '../services/api';
import Upload from './Upload';
import EquipmentChart from './EquipmentChart';
import History from './History';
import './Dashboard.css';

const Dashboard = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showUpload, setShowUpload] = useState(false);
    const [downloadingPDF, setDownloadingPDF] = useState(false);

    const fetchStats = async () => {
        try {
            setLoading(true);
            const data = await getDashboardStats();
            setStats(data);
            setError(null);
        } catch (err) {
            setError('Failed to load dashboard data');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStats();
    }, []);

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    const handleUploadSuccess = () => {
        setShowUpload(false);
        fetchStats();
    };

    const handleDownloadPDF = async () => {
        setDownloadingPDF(true);
        try {
            const blob = await downloadPDF();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `equipment_report.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (err) {
            console.error('PDF download failed:', err);
        } finally {
            setDownloadingPDF(false);
        }
    };

    if (loading && !stats) {
        return (
            <div className="dashboard-loading">
                <div className="loader-ring"></div>
                <p>Loading dashboard...</p>
            </div>
        );
    }

    return (
        <div className="dashboard">
            {/* Header */}
            <header className="dashboard-header">
                <div className="header-left">
                    <div className="logo">
                        <svg viewBox="0 0 24 24" className="logo-icon">
                            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                                stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" />
                        </svg>
                        <span>Chemical Visualizer</span>
                    </div>
                </div>
                <div className="header-right">
                    <button className="header-btn upload-toggle" onClick={() => setShowUpload(!showUpload)}>
                        <svg viewBox="0 0 24 24">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" strokeWidth="2" fill="none" />
                            <polyline points="17 8 12 3 7 8" stroke="currentColor" strokeWidth="2" fill="none" />
                            <line x1="12" y1="3" x2="12" y2="15" stroke="currentColor" strokeWidth="2" />
                        </svg>
                        Upload CSV
                    </button>
                    <button
                        className="header-btn pdf-btn"
                        onClick={handleDownloadPDF}
                        disabled={downloadingPDF || !stats?.total_count}
                    >
                        {downloadingPDF ? (
                            <span className="btn-spinner"></span>
                        ) : (
                            <svg viewBox="0 0 24 24">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2" fill="none" />
                                <polyline points="14 2 14 8 20 8" stroke="currentColor" strokeWidth="2" fill="none" />
                                <line x1="12" y1="18" x2="12" y2="12" stroke="currentColor" strokeWidth="2" />
                                <polyline points="9 15 12 18 15 15" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                        )}
                        Download PDF
                    </button>
                    <div className="user-menu">
                        <span className="user-name">{user?.username}</span>
                        <button className="logout-btn" onClick={handleLogout}>
                            <svg viewBox="0 0 24 24">
                                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" stroke="currentColor" strokeWidth="2" fill="none" />
                                <polyline points="16 17 21 12 16 7" stroke="currentColor" strokeWidth="2" fill="none" />
                                <line x1="21" y1="12" x2="9" y2="12" stroke="currentColor" strokeWidth="2" />
                            </svg>
                        </button>
                    </div>
                </div>
            </header>

            {/* Upload Modal */}
            {showUpload && (
                <div className="upload-modal-overlay" onClick={() => setShowUpload(false)}>
                    <div className="upload-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2>Upload Equipment Data</h2>
                            <button className="close-modal" onClick={() => setShowUpload(false)}>
                                <svg viewBox="0 0 24 24">
                                    <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" strokeWidth="2" />
                                    <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" strokeWidth="2" />
                                </svg>
                            </button>
                        </div>
                        <Upload onUploadSuccess={handleUploadSuccess} />
                    </div>
                </div>
            )}

            {/* Main Content */}
            <main className="dashboard-main">
                {error && (
                    <div className="error-banner">
                        <svg viewBox="0 0 24 24">
                            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" />
                            <line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" strokeWidth="2" />
                            <circle cx="12" cy="16" r="1" fill="currentColor" />
                        </svg>
                        {error}
                    </div>
                )}

                {/* Summary Cards */}
                <section className="summary-cards">
                    <div className="stat-card purple">
                        <div className="stat-icon">
                            <svg viewBox="0 0 24 24">
                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="2" fill="none" />
                                <circle cx="9" cy="7" r="4" stroke="currentColor" strokeWidth="2" fill="none" />
                                <path d="M23 21v-2a4 4 0 0 0-3-3.87" stroke="currentColor" strokeWidth="2" fill="none" />
                                <path d="M16 3.13a4 4 0 0 1 0 7.75" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                        </div>
                        <div className="stat-content">
                            <span className="stat-label">Total Equipment</span>
                            <span className="stat-value">{stats?.total_count || 0}</span>
                        </div>
                    </div>

                    <div className="stat-card blue">
                        <div className="stat-icon">
                            <svg viewBox="0 0 24 24">
                                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" />
                                <path d="M12 6v6l4 2" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                        </div>
                        <div className="stat-content">
                            <span className="stat-label">Avg Flowrate</span>
                            <span className="stat-value">{stats?.average_values?.flowrate || 0}</span>
                        </div>
                    </div>

                    <div className="stat-card green">
                        <div className="stat-icon">
                            <svg viewBox="0 0 24 24">
                                <path d="M22 12h-4l-3 9L9 3l-3 9H2" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                        </div>
                        <div className="stat-content">
                            <span className="stat-label">Avg Pressure</span>
                            <span className="stat-value">{stats?.average_values?.pressure || 0}</span>
                        </div>
                    </div>

                    <div className="stat-card orange">
                        <div className="stat-icon">
                            <svg viewBox="0 0 24 24">
                                <path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                        </div>
                        <div className="stat-content">
                            <span className="stat-label">Avg Temperature</span>
                            <span className="stat-value">{stats?.average_values?.temperature || 0}</span>
                        </div>
                    </div>
                </section>

                {/* Charts Section */}
                <section className="charts-section">
                    <EquipmentChart
                        typeDistribution={stats?.type_distribution || {}}
                        equipmentData={stats?.equipment_data || []}
                    />
                </section>

                {/* Data Table */}
                <section className="data-table-section">
                    <div className="section-header">
                        <h2>Equipment Data</h2>
                        {stats?.latest_batch && (
                            <span className="batch-info">
                                Batch #{stats.latest_batch.id} • {new Date(stats.latest_batch.uploaded_at).toLocaleString()}
                            </span>
                        )}
                    </div>

                    {stats?.equipment_data?.length > 0 ? (
                        <div className="table-wrapper">
                            <table className="data-table">
                                <thead>
                                    <tr>
                                        <th>Equipment Name</th>
                                        <th>Type</th>
                                        <th>Flowrate</th>
                                        <th>Pressure</th>
                                        <th>Temperature</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {stats.equipment_data.map((item) => (
                                        <tr key={item.id}>
                                            <td>{item.equipment_name}</td>
                                            <td>
                                                <span className={`type-badge ${item.type.toLowerCase().replace(/\s+/g, '-')}`}>
                                                    {item.type}
                                                </span>
                                            </td>
                                            <td>{item.flowrate.toFixed(2)}</td>
                                            <td>{item.pressure.toFixed(2)}</td>
                                            <td>{item.temperature.toFixed(2)}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    ) : (
                        <div className="empty-table">
                            <svg viewBox="0 0 24 24" className="empty-icon">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2" fill="none" />
                                <polyline points="14 2 14 8 20 8" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                            <p>No equipment data available</p>
                            <button className="upload-cta" onClick={() => setShowUpload(true)}>
                                Upload your first CSV file
                            </button>
                        </div>
                    )}
                </section>

                {/* History Section */}
                <History />
            </main>

        </div >
    );
};

export default Dashboard;
