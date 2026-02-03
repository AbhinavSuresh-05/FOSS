import { useState, useCallback } from 'react';
import { uploadCSV } from '../services/api';
import './Upload.css';

const Upload = ({ onUploadSuccess }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);

    const handleDrag = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
    }, []);

    const handleDragIn = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    }, []);

    const handleDragOut = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);

        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            handleFile(files[0]);
        }
    }, []);

    const handleFileSelect = (e) => {
        const files = e.target.files;
        if (files && files.length > 0) {
            handleFile(files[0]);
        }
    };

    const handleFile = (file) => {
        if (!file.name.endsWith('.csv')) {
            setUploadStatus({ type: 'error', message: 'Only CSV files are allowed' });
            return;
        }
        setSelectedFile(file);
        setUploadStatus(null);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setIsUploading(true);
        setUploadStatus(null);

        try {
            const result = await uploadCSV(selectedFile);
            setUploadStatus({
                type: 'success',
                message: `Successfully uploaded ${result.records_created} records`
            });
            setSelectedFile(null);
            if (onUploadSuccess) {
                onUploadSuccess();
            }
        } catch (error) {
            setUploadStatus({
                type: 'error',
                message: error.response?.data?.error || 'Upload failed'
            });
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="upload-container">
            <div
                className={`upload-zone ${isDragging ? 'dragging' : ''} ${selectedFile ? 'has-file' : ''}`}
                onDragEnter={handleDragIn}
                onDragLeave={handleDragOut}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                {selectedFile ? (
                    <div className="file-preview">
                        <svg viewBox="0 0 24 24" className="file-icon">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                                stroke="currentColor" strokeWidth="2" fill="none" />
                            <polyline points="14 2 14 8 20 8" stroke="currentColor" strokeWidth="2" fill="none" />
                            <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" strokeWidth="2" />
                            <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" strokeWidth="2" />
                            <polyline points="10 9 9 9 8 9" stroke="currentColor" strokeWidth="2" fill="none" />
                        </svg>
                        <div className="file-info">
                            <span className="file-name">{selectedFile.name}</span>
                            <span className="file-size">{(selectedFile.size / 1024).toFixed(1)} KB</span>
                        </div>
                        <button
                            className="remove-file"
                            onClick={(e) => { e.stopPropagation(); setSelectedFile(null); }}
                        >
                            <svg viewBox="0 0 24 24">
                                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" strokeWidth="2" />
                                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" strokeWidth="2" />
                            </svg>
                        </button>
                    </div>
                ) : (
                    <div className="upload-prompt">
                        <div className="upload-icon-container">
                            <svg viewBox="0 0 24 24" className="upload-icon">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"
                                    stroke="currentColor" strokeWidth="2" fill="none" />
                                <polyline points="17 8 12 3 7 8" stroke="currentColor" strokeWidth="2" fill="none" />
                                <line x1="12" y1="3" x2="12" y2="15" stroke="currentColor" strokeWidth="2" />
                            </svg>
                        </div>
                        <p className="upload-text">
                            Drag & drop your CSV file here or{' '}
                            <label className="browse-link">
                                browse
                                <input
                                    type="file"
                                    accept=".csv"
                                    onChange={handleFileSelect}
                                    hidden
                                />
                            </label>
                        </p>
                        <p className="upload-hint">Support for CSV files with Equipment Name, Type, Flowrate, Pressure, Temperature columns</p>
                    </div>
                )}
            </div>

            {selectedFile && (
                <button
                    className="upload-button"
                    onClick={handleUpload}
                    disabled={isUploading}
                >
                    {isUploading ? (
                        <>
                            <span className="spinner"></span>
                            Uploading...
                        </>
                    ) : (
                        <>
                            <svg viewBox="0 0 24 24" className="btn-icon">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"
                                    stroke="currentColor" strokeWidth="2" fill="none" />
                                <polyline points="17 8 12 3 7 8" stroke="currentColor" strokeWidth="2" fill="none" />
                                <line x1="12" y1="3" x2="12" y2="15" stroke="currentColor" strokeWidth="2" />
                            </svg>
                            Upload File
                        </>
                    )}
                </button>
            )}

            {uploadStatus && (
                <div className={`upload-status ${uploadStatus.type}`}>
                    {uploadStatus.type === 'success' ? (
                        <svg viewBox="0 0 24 24" className="status-icon">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke="currentColor" strokeWidth="2" fill="none" />
                            <polyline points="22 4 12 14.01 9 11.01" stroke="currentColor" strokeWidth="2" fill="none" />
                        </svg>
                    ) : (
                        <svg viewBox="0 0 24 24" className="status-icon">
                            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" />
                            <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" strokeWidth="2" />
                            <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" strokeWidth="2" />
                        </svg>
                    )}
                    {uploadStatus.message}
                </div>
            )}
        </div>
    );
};

export default Upload;
