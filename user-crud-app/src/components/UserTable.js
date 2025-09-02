import React from 'react';
import '../App.css';

function UserTable({ users, onView, onEdit, onDelete }) {
  return (
    <div className="user-table-container">
      <h2>User List</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Location</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.phone || 'N/A'}</td>
              <td>{user.address || 'N/A'}</td>
              <td>
                <button className="view-button" onClick={() => onView(user)}>View</button>
                <button className="edit-button" onClick={() => onEdit(user)}>Edit</button>
                <button className="delete-button" onClick={() => onDelete(user.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserTable;