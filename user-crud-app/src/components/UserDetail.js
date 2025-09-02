import React from 'react';
import '../App.css';

function UserDetail({ user, onClose }) {
  return (
    <div className="user-detail-modal">
      <div className="modal-content">
        <h2>User Details</h2>
        <p><strong>Name:</strong> {user.name}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Phone:</strong> {user.phone || 'N/A'}</p>
        <p><strong>Location:</strong> {user.address || 'N/A'}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default UserDetail;