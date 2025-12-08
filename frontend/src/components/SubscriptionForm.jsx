import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const SubscriptionForm = ({ onSubmit, initialData, onCancel }) => {
    const [formData, setFormData] = useState({
        name: '',
        start_date: '',
        renewal_date: '',
        note: ''
    });

    useEffect(() => {
        if (initialData) {
            setFormData({
                name: initialData.name,
                start_date: initialData.start_date || '',
                renewal_date: initialData.renewal_date,
                note: initialData.note || ''
            });
        }
    }, [initialData]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Convert empty string to null for optional fields
        const submitData = {
            ...formData,
            start_date: formData.start_date || null,
            note: formData.note || null
        };
        onSubmit(submitData);
    };

    return (
        <motion.form
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            onSubmit={handleSubmit}
            className="card"
            style={{ maxWidth: '600px', margin: '0 auto', background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)', border: '1px solid rgba(102, 126, 234, 0.2)' }}
        >
            <h2 style={{ marginTop: 0, marginBottom: '1.5rem', fontSize: '1.75rem' }}>
                {initialData ? '✏️ Edit Subscription' : '➕ Add New Subscription'}
            </h2>
            <div style={{ marginBottom: '1.5rem' }}>
                <label>Subscription Name</label>
                <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    placeholder="e.g., Netflix, Spotify, Amazon Prime..."
                />
            </div>
            <div style={{ marginBottom: '1.5rem' }}>
                <label>Start Date (Optional)</label>
                <input
                    type="date"
                    name="start_date"
                    value={formData.start_date}
                    onChange={handleChange}
                    placeholder="When did you start this subscription?"
                />
            </div>
            <div style={{ marginBottom: '1.5rem' }}>
                <label>Renewal Date</label>
                <input
                    type="date"
                    name="renewal_date"
                    value={formData.renewal_date}
                    onChange={handleChange}
                    required
                    min={new Date().toISOString().split('T')[0]}
                />
            </div>
            <div style={{ marginBottom: '1.5rem' }}>
                <label>Note (Optional)</label>
                <textarea
                    name="note"
                    value={formData.note}
                    onChange={handleChange}
                    placeholder="Add any additional notes about this subscription..."
                    rows={3}
                    style={{ resize: 'vertical', fontFamily: 'inherit' }}
                />
            </div>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '2rem' }}>
                {onCancel && (
                    <button type="button" onClick={onCancel} className="btn btn-secondary">
                        Cancel
                    </button>
                )}
                <button type="submit" className="btn btn-primary">
                    {initialData ? 'Update Subscription' : 'Add Subscription'}
                </button>
            </div>
        </motion.form>
    );
};

export default SubscriptionForm;
