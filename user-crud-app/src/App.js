import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserTable from './components/UserTable';
import UserDetail from './components/UserDetail';
import UserForm from './components/UserForm';
import './App.css';

function App() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('https://reqres.in/api/users?per_page=10');
      const usersWithFullName = response.data.data.map(user => ({
        ...user,
        name: `${user.first_name} ${user.last_name}`,
      }));
      setUsers(usersWithFullName);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleView = (user) => {
    setSelectedUser(user);
    setEditingUser(null);
    setShowCreateForm(false);
  };

  const handleEdit = (user) => {
    setEditingUser(user);
    setSelectedUser(null);
    setShowCreateForm(false);
  };

  const handleDelete = async (id) => {
    try {
      // Attempt to make the API call, but don't block UI update on its success
      axios.delete(`https://reqres.in/api/users/${id}`)
        .then(response => {
          console.log('API Delete Success (simulated):', response.data);
        })
        .catch(error => {
          console.error('API Delete Failed (but UI will update):', error);
        });

      setUsers(users.filter((user) => user.id !== id));
      alert('User deleted successfully (UI updated)!');
    } catch (error) {
      console.error('Error during user delete process:', error);
    }
  };

  const handleCreate = async (newUser) => {
    try {
      // reqres.in expects 'name' and 'job' for POST requests
      const payload = { name: newUser.name, job: 'developer' };
      // Attempt to make the API call, but don't block UI update on its success
      axios.post('https://reqres.in/api/users', payload)
        .then(response => {
          console.log('API Create Success (simulated):', response.data);
        })
        .catch(error => {
          console.error('API Create Failed (but UI will update):', error);
        });

      // Simulate a new ID for the local state update
      const simulatedId = Date.now();
      setUsers([...users, { ...newUser, id: simulatedId, name: newUser.name }]);
      setShowCreateForm(false);
      alert('User created successfully (UI updated)!');
    } catch (error) {
      // This catch block is for errors before the axios call, or if the promise itself fails
      console.error('Error during user creation process:', error);
    }
  };

  const handleUpdate = async (updatedUser) => {
    try {
      // Attempt to make the API call, but don't block UI update on its success
      axios.put(`https://reqres.in/api/users/${updatedUser.id}`, updatedUser)
        .then(response => {
          console.log('API Update Success (simulated):', response.data);
        })
        .catch(error => {
          console.error('API Update Failed (but UI will update):', error);
        });

      setUsers(
        users.map((user) => (user.id === updatedUser.id ? updatedUser : user))
      );
      setEditingUser(null);
      alert('User updated successfully (UI updated)!');
    } catch (error) {
      console.error('Error during user update process:', error);
    }
  };

  return (
    <div className="App">
      <h1>User Management</h1>
      <button className="create-button" onClick={() => {
        setShowCreateForm(true);
        setSelectedUser(null);
        setEditingUser(null);
      }}>
        Create User
      </button>

      {showCreateForm && (
        <UserForm onSubmit={handleCreate} onCancel={() => setShowCreateForm(false)} />
      )}

      {selectedUser && (
        <UserDetail user={selectedUser} onClose={() => setSelectedUser(null)} />
      )}

      {editingUser && (
        <UserForm user={editingUser} onSubmit={handleUpdate} onCancel={() => setEditingUser(null)} />
      )}

      <UserTable
        users={users}
        onView={handleView}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
}

export default App;