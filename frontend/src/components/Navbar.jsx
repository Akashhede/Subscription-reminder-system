import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Bell, LogOut } from 'lucide-react';
import { motion } from 'framer-motion';

const Navbar = () => {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    const handleLogout = () => {
        if (window.confirm('Are you sure you want to logout?')) {
            localStorage.removeItem('token');
            navigate('/login');
        }
    };

    if (!token) return null;

    return (
        <motion.nav
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            style={{
                background: 'rgba(26, 31, 58, 0.8)',
                backdropFilter: 'blur(10px)',
                padding: '1rem 2rem',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                borderBottom: '1px solid var(--border-color)',
                position: 'sticky',
                top: 0,
                zIndex: 1000
            }}
        >
            <Link 
                to="/" 
                style={{ 
                    color: 'var(--text-primary)', 
                    textDecoration: 'none', 
                    fontSize: '1.5rem', 
                    fontWeight: 'bold',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    background: 'linear-gradient(135deg, var(--accent) 0%, #764ba2 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text'
                }}
            >
                <Bell size={24} style={{ color: 'var(--accent)' }} />
                Subscription Reminder
            </Link>
            <button 
                onClick={handleLogout} 
                className="btn btn-secondary" 
                style={{ padding: '0.625rem 1.25rem', fontSize: '0.9rem' }}
            >
                <LogOut size={18} />
                Logout
            </button>
        </motion.nav>
    );
};

export default Navbar;
