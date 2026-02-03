import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import './Register.css';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await api.register(username, password, passwordConfirm);
            navigate('/login', { state: { message: 'Registration successful! Please login.' } });
        } catch (err) {
            // Handle API errors
            if (err.response?.data) {
                const errors = err.response.data;
                if (typeof errors === 'object') {
                    // Format validation errors
                    const messages = Object.entries(errors)
                        .map(([field, msgs]) => {
                            if (Array.isArray(msgs)) return msgs.join(' ');
                            return msgs;
                        })
                        .join(' ');
                    setError(messages);
                } else {
                    setError('Registration failed. Please try again.');
                }
            } else {
                setError('Unable to connect to server.');
            }
        }
        setIsLoading(false);
    };

    return (
        <div className="register-container">
            <div className="register-background">
                <div className="gradient-orb orb-1"></div>
                <div className="gradient-orb orb-2"></div>
                <div className="gradient-orb orb-3"></div>
            </div>

            <div className="register-card">
                <div className="register-header">
                    <div className="logo-container">
                        <img src="/app-icon.png" alt="Chemical Equipment Visualizer" className="logo-icon" />
                    </div>
                    <h1>Create Account</h1>
                    <p>Join the Chemical Equipment Visualizer</p>
                </div>

                <form onSubmit={handleSubmit} className="register-form">
                    {error && (
                        <div className="error-message">
                            <svg viewBox="0 0 24 24" className="error-icon">
                                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" />
                                <line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" strokeWidth="2" />
                                <circle cx="12" cy="16" r="1" fill="currentColor" />
                            </svg>
                            {error}
                        </div>
                    )}

                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <div className="input-wrapper">
                            <svg viewBox="0 0 24 24" className="input-icon">
                                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="2" fill="none" />
                                <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                            <input
                                type="text"
                                id="username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Choose a username"
                                required
                                minLength={3}
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <div className="input-wrapper">
                            <svg viewBox="0 0 24 24" className="input-icon">
                                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2" fill="none" />
                                <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                            <input
                                type="password"
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Min 8 chars, letters, numbers, special"
                                required
                                minLength={8}
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label htmlFor="passwordConfirm">Confirm Password</label>
                        <div className="input-wrapper">
                            <svg viewBox="0 0 24 24" className="input-icon">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                            <input
                                type="password"
                                id="passwordConfirm"
                                value={passwordConfirm}
                                onChange={(e) => setPasswordConfirm(e.target.value)}
                                placeholder="Confirm your password"
                                required
                                minLength={8}
                            />
                        </div>
                    </div>

                    <button type="submit" className="register-button" disabled={isLoading}>
                        {isLoading ? (
                            <span className="loader"></span>
                        ) : (
                            <>
                                Create Account
                                <svg viewBox="0 0 24 24" className="button-icon">
                                    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="2" fill="none" />
                                    <circle cx="8.5" cy="7" r="4" stroke="currentColor" strokeWidth="2" fill="none" />
                                    <line x1="20" y1="8" x2="20" y2="14" stroke="currentColor" strokeWidth="2" />
                                    <line x1="23" y1="11" x2="17" y2="11" stroke="currentColor" strokeWidth="2" />
                                </svg>
                            </>
                        )}
                    </button>
                </form>

                <div className="register-footer">
                    <p>Already have an account? <Link to="/login">Sign in</Link></p>
                </div>
            </div>
        </div>
    );
};

export default Register;
