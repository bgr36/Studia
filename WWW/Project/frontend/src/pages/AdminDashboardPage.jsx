import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

function AdminDashboardPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token, userRole } = useAuth(); // Potrzebny token i rola do autoryzacji
  const [message, setMessage] = useState('');

  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    setMessage('');
    try {
      // Zmieniamy endpoint z /users na /users/all
      const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/users/all`, {
        headers: {
          Authorization: `Bearer ${token}` // Przekazujemy token autoryzacyjny
        }
      });
      setUsers(response.data);
    } catch (err) {
      console.error("Error fetching users:", err);
      // Bardziej szczegółowe komunikaty błędów z backendu
      const apiErrorMessage = err.response?.data?.message || err.response?.data?.error || 'Failed to load users. Please check your permissions or network connection.';
      setError(apiErrorMessage);
      setUsers([]); // Wyczyść listę użytkowników w przypadku błędu
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm("Are you sure you want to delete this user?")) {
      return;
    }
    setError(null);
    setMessage('');
    try {
      await axios.delete(`${import.meta.env.VITE_API_BASE_URL}/users/${userId}`, {
        headers: {
          Authorization: `Bearer ${token}` // Przekazujemy token autoryzacyjny
        }
      });
      setMessage('User deleted successfully!');
      fetchUsers(); // Odśwież listę użytkowników po usunięciu
    } catch (err) {
      console.error("Error deleting user:", err);
      const apiErrorMessage = err.response?.data?.message || err.response?.data?.error || 'Failed to delete user. Access denied or server error.';
      setError(apiErrorMessage);
    }
  };

  // Możesz dodać funkcję do edycji, jeśli masz endpoint PUT/PATCH /users/:id
  // const handleEditUser = (userId) => {
  //   // Implementuj nawigację do strony edycji lub modal
  //   console.log(`Edit user with ID: ${userId}`);
  // };

  useEffect(() => {
    if (token && userRole === 'admin') { // Pobieraj użytkowników tylko jeśli zalogowany i jest adminem
      fetchUsers();
    } else if (!token) {
      setError("You must be logged in to access the admin dashboard.");
      setLoading(false);
    } else if (userRole !== 'admin') {
        setError("Access Denied: You do not have administrator privileges.");
        setLoading(false);
    }
  }, [token, userRole]); // Re-fetch when token or userRole changes

  if (loading) return <p>Loading admin data...</p>;
  if (error) return <p className="error-message">{error}</p>;

  return (
    <div className="page-container">
      <h1>Admin Dashboard</h1>
      {message && <p className="success-message">{message}</p>}
      <h2>Manage Users</h2>
      {users.length > 0 ? (
        <div className="user-list">
          {users.map(user => (
            <div key={user.id} className="user-card">
              <h3>{user.username} ({user.role})</h3>
              <p>Email: {user.email}</p>
              <div className="user-actions">
                {/* Opcjonalnie: Przycisk edycji użytkownika */}
                {/* <button onClick={() => handleEditUser(user.id)} className="button secondary">Edit</button> */}
                {/* Nie pozwalamy adminowi usuwać siebie ani innych adminów przez ten interfejs */}
                {user.role !== 'admin' && (
                  <button onClick={() => handleDeleteUser(user.id)} className="button danger">Delete User</button>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p>No users found or you don't have permission to view them.</p>
      )}
    </div>
  );
}

export default AdminDashboardPage;