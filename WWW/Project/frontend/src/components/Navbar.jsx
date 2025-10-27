import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Navbar() {
  const { isAuthenticated, logout, userRole } = useAuth();

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">E-Commerce App</Link>
      <ul className="navbar-nav">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/products">Products</Link></li>
        <li><Link to="/reviews">Reviews</Link></li>
        {isAuthenticated && userRole === 'admin' && (
          <>
            <li><Link to="/add-product">Add Product</Link></li>
            <li><Link to="/admin">Admin Dashboard</Link></li>
          </>
        )}
        {isAuthenticated ? (
          <li><button onClick={logout} className="nav-button">Logout</button></li>
        ) : (
          <li><Link to="/login">Login</Link></li>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;