import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import AddProductPage from './pages/AddProductPage';
import LoginPage from './pages/LoginPage';
import ReviewsPage from './pages/ReviewsPage';
import AdminDashboardPage from './pages/AdminDashboardPage';
import { AuthProvider, useAuth } from './context/AuthContext'; // We'll create this

// PrivateRoute component to protect routes
const PrivateRoute = ({ children, allowedRoles }) => {
  const { isAuthenticated, userRole, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading authentication...</div>; // Or a spinner
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(userRole)) {
    return <div style={{ color: 'red', textAlign: 'center', marginTop: '50px' }}>Access Denied: You do not have the required role.</div>;
  }

  return children;
};


function App() {
  return (
    <Router>
      <AuthProvider> {/* Wrap your app with AuthProvider */}
        <Navbar />
        <div className="container"> {/* For basic centering/padding */}
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/add-product" element={
              <PrivateRoute allowedRoles={['admin']}>
                <AddProductPage />
              </PrivateRoute>
            } />
            <Route path="/reviews" element={<ReviewsPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/admin" element={
              <PrivateRoute allowedRoles={['admin']}>
                <AdminDashboardPage />
              </PrivateRoute>
            } />
            <Route path="*" element={<h2>404 - Page Not Found</h2>} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;