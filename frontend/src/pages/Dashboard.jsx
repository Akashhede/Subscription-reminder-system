import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Edit2, Trash2, Calendar, AlertCircle, Bell, TrendingUp, Clock } from 'lucide-react';
import api from '../api';
import Navbar from '../components/Navbar';
import SubscriptionForm from '../components/SubscriptionForm';

const Dashboard = () => {
    const [subscriptions, setSubscriptions] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [editingSub, setEditingSub] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchSubscriptions();
    }, []);

    const fetchSubscriptions = async () => {
        try {
            setLoading(true);
            setError('');
            const response = await api.get('/subscription/list');
            console.log('Subscriptions fetched:', response.data);
            if (Array.isArray(response.data)) {
                setSubscriptions(response.data);
            } else {
                console.error('Invalid response format:', response.data);
                setError('Invalid response format from server.');
            }
        } catch (error) {
            console.error('Failed to fetch subscriptions', error);
            const errorMessage = error.response?.data?.detail || error.message || 'Failed to load subscriptions. Please try again.';
            setError(errorMessage);
            setSubscriptions([]); // Clear subscriptions on error
        } finally {
            setLoading(false);
        }
    };

    const handleAdd = async (data) => {
        try {
            await api.post('/subscription/add', data);
            setShowForm(false);
            fetchSubscriptions();
        } catch (error) {
            console.error('Failed to add subscription', error);
            alert('Failed to add subscription. Please try again.');
        }
    };

    const handleUpdate = async (data) => {
        try {
            await api.put(`/subscription/update/${editingSub.id}`, data);
            setEditingSub(null);
            fetchSubscriptions();
        } catch (error) {
            console.error('Failed to update subscription', error);
            alert('Failed to update subscription. Please try again.');
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this subscription?')) {
            try {
                await api.delete(`/subscription/delete/${id}`);
                fetchSubscriptions();
            } catch (error) {
                console.error('Failed to delete subscription', error);
                alert('Failed to delete subscription. Please try again.');
            }
        }
    };


    const getDaysUntilRenewal = (dateString) => {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const renewal = new Date(dateString);
        renewal.setHours(0, 0, 0, 0);
        const diffTime = renewal - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays;
    };

    const isExpiringSoon = (dateString) => {
        const days = getDaysUntilRenewal(dateString);
        return days >= 0 && days <= 7;
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    };

    const getStatusColor = (dateString) => {
        const days = getDaysUntilRenewal(dateString);
        if (days < 0) return 'var(--danger)';
        if (days <= 3) return 'var(--danger)';
        if (days <= 7) return 'var(--warning)';
        return 'var(--success)';
    };

    const getStatusText = (dateString) => {
        const days = getDaysUntilRenewal(dateString);
        if (days < 0) return 'Expired';
        if (days === 0) return 'Renews today';
        if (days === 1) return 'Renews tomorrow';
        if (days <= 7) return `${days} days remaining`;
        return `${days} days remaining`;
    };

    const stats = {
        total: subscriptions.length,
        expiringSoon: subscriptions.filter(sub => isExpiringSoon(sub.renewal_date)).length,
        thisMonth: subscriptions.filter(sub => {
            const renewal = new Date(sub.renewal_date);
            const today = new Date();
            return renewal.getMonth() === today.getMonth() && renewal.getFullYear() === today.getFullYear();
        }).length
    };

    return (
        <div className="page-transition">
            <Navbar />
            <div className="container">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
                    <div>
                        <h1 style={{ margin: 0, fontSize: '2.5rem', background: 'linear-gradient(135deg, var(--accent) 0%, #764ba2 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
                            My Subscriptions
                        </h1>
                        <p style={{ margin: '0.5rem 0 0 0', color: 'var(--text-secondary)' }}>
                            Manage your subscription renewals and never miss a payment
                        </p>
                    </div>
                    <button
                        className="btn btn-primary"
                        onClick={() => { setEditingSub(null); setShowForm(true); }}
                        style={{ fontSize: '1rem' }}
                    >
                        <Plus size={20} /> Add New Subscription
                    </button>
                </div>

                {/* Stats Cards */}
                {subscriptions.length > 0 && (
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 }}
                            className="card"
                            style={{ background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%)', border: '1px solid rgba(102, 126, 234, 0.3)' }}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                <div style={{ padding: '0.75rem', borderRadius: '0.75rem', background: 'rgba(102, 126, 234, 0.2)' }}>
                                    <TrendingUp size={24} color="var(--accent)" />
                                </div>
                                <div>
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--text-primary)' }}>{stats.total}</div>
                                    <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Total Subscriptions</div>
                                </div>
                            </div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                            className="card"
                            style={{ background: 'linear-gradient(135deg, rgba(237, 137, 54, 0.2) 0%, rgba(245, 101, 101, 0.2) 100%)', border: '1px solid rgba(237, 137, 54, 0.3)' }}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                <div style={{ padding: '0.75rem', borderRadius: '0.75rem', background: 'rgba(237, 137, 54, 0.2)' }}>
                                    <AlertCircle size={24} color="var(--warning)" />
                                </div>
                                <div>
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--text-primary)' }}>{stats.expiringSoon}</div>
                                    <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Expiring Soon</div>
                                </div>
                            </div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.3 }}
                            className="card"
                            style={{ background: 'linear-gradient(135deg, rgba(72, 187, 120, 0.2) 0%, rgba(102, 126, 234, 0.2) 100%)', border: '1px solid rgba(72, 187, 120, 0.3)' }}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                <div style={{ padding: '0.75rem', borderRadius: '0.75rem', background: 'rgba(72, 187, 120, 0.2)' }}>
                                    <Bell size={24} color="var(--success)" />
                                </div>
                                <div>
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--text-primary)' }}>{stats.thisMonth}</div>
                                    <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>This Month</div>
                                </div>
                            </div>
                        </motion.div>
                    </div>
                )}

                <AnimatePresence>
                    {(showForm || editingSub) && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            style={{ marginBottom: '2rem', overflow: 'hidden' }}
                        >
                            <SubscriptionForm
                                onSubmit={editingSub ? handleUpdate : handleAdd}
                                initialData={editingSub}
                                onCancel={() => { setShowForm(false); setEditingSub(null); }}
                            />
                        </motion.div>
                    )}
                </AnimatePresence>

                {error && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="card"
                        style={{ background: 'rgba(245, 101, 101, 0.1)', border: '1px solid var(--danger)', marginBottom: '2rem' }}
                    >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--danger)' }}>
                            <AlertCircle size={20} />
                            <span>{error}</span>
                        </div>
                    </motion.div>
                )}

                {loading ? (
                    <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-secondary)' }}>
                        <div style={{ fontSize: '1.5rem' }}>Loading subscriptions...</div>
                    </div>
                ) : (
                    <>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1.5rem' }}>
                            {subscriptions.map((sub, index) => {
                                const daysUntil = getDaysUntilRenewal(sub.renewal_date);
                                const statusColor = getStatusColor(sub.renewal_date);
                                const statusText = getStatusText(sub.renewal_date);
                                
                                return (
                                    <motion.div
                                        key={sub.id}
                                        layout
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, scale: 0.9 }}
                                        transition={{ delay: index * 0.05 }}
                                        className="card"
                                        style={{ 
                                            borderLeft: `4px solid ${statusColor}`,
                                            position: 'relative',
                                            overflow: 'hidden'
                                        }}
                                    >
                                        <div style={{ 
                                            position: 'absolute', 
                                            top: 0, 
                                            right: 0, 
                                            width: '100px', 
                                            height: '100px', 
                                            background: `radial-gradient(circle, ${statusColor}20 0%, transparent 70%)`,
                                            borderRadius: '50%',
                                            transform: 'translate(30%, -30%)'
                                        }} />
                                        
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem', position: 'relative', zIndex: 1 }}>
                                            <h3 style={{ margin: 0, fontSize: '1.5rem', fontWeight: '600' }}>{sub.name}</h3>
                                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                                <button
                                                    onClick={() => { setEditingSub(sub); setShowForm(false); }}
                                                    className="btn"
                                                    style={{ padding: '0.5rem', backgroundColor: 'rgba(102, 126, 234, 0.1)', color: 'var(--accent)', border: 'none' }}
                                                    title="Edit"
                                                >
                                                    <Edit2 size={18} />
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(sub.id)}
                                                    className="btn"
                                                    style={{ padding: '0.5rem', backgroundColor: 'rgba(245, 101, 101, 0.1)', color: 'var(--danger)', border: 'none' }}
                                                    title="Delete"
                                                >
                                                    <Trash2 size={18} />
                                                </button>
                                            </div>
                                        </div>

                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', position: 'relative', zIndex: 1 }}>
                                            {sub.start_date && (
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                                                    <Calendar size={16} />
                                                    <span>Started: {formatDate(sub.start_date)}</span>
                                                </div>
                                            )}
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--text-secondary)' }}>
                                                <Calendar size={18} />
                                                <span style={{ fontSize: '0.95rem' }}>Renews: {formatDate(sub.renewal_date)}</span>
                                            </div>

                                            <div style={{ 
                                                display: 'flex', 
                                                alignItems: 'center', 
                                                gap: '0.75rem', 
                                                color: statusColor, 
                                                fontWeight: '600',
                                                fontSize: '0.95rem',
                                                padding: '0.5rem',
                                                borderRadius: '0.5rem',
                                                background: `${statusColor}15`
                                            }}>
                                                <Clock size={18} />
                                                <span>{statusText}</span>
                                            </div>

                                            {sub.note && (
                                                <div style={{ 
                                                    marginTop: '0.5rem', 
                                                    padding: '0.75rem', 
                                                    background: 'rgba(102, 126, 234, 0.05)', 
                                                    borderRadius: '0.5rem',
                                                    border: '1px solid rgba(102, 126, 234, 0.1)'
                                                }}>
                                                    <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.5' }}>
                                                        {sub.note}
                                                    </p>
                                                </div>
                                            )}
                                        </div>
                                    </motion.div>
                                );
                            })}
                        </div>

                        {subscriptions.length === 0 && !loading && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-secondary)' }}
                            >
                                <Bell size={64} style={{ marginBottom: '1rem', opacity: 0.3 }} />
                                <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-primary)' }}>No subscriptions yet</h3>
                                <p style={{ marginBottom: '2rem' }}>Add your first subscription to start tracking renewals</p>
                                <button
                                    className="btn btn-primary"
                                    onClick={() => { setEditingSub(null); setShowForm(true); }}
                                >
                                    <Plus size={20} /> Add Your First Subscription
                                </button>
                            </motion.div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
