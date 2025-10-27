import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; // npm install jwt-decode

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  const [userRole, setUserRole] = useState(null);
  const [userId, setUserId] = useState(null); // <-- Dodaj ten stan
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      try {
        const decoded = jwtDecode(storedToken);
        if (decoded.exp * 1000 < Date.now()) {
          console.log('Token expired.');
          logout();
        } else {
          setToken(storedToken);
          setIsAuthenticated(true);
          setUserRole(decoded.role);
          setUserId(decoded.id); // <-- Ustaw userId przy ładowaniu
        }
      } catch (e) {
        console.error("Invalid token:", e);
        logout();
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email, password) => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/auth/login`, { email, password });
      const newToken = response.data.token;
      localStorage.setItem('token', newToken);
      setToken(newToken);
      setIsAuthenticated(true);
      const decoded = jwtDecode(newToken);
      setUserRole(decoded.role);
      setUserId(decoded.id); // <-- Ustaw userId po pomyślnym logowaniu
      return { success: true };
    } catch (err) {
      console.error("Login failed:", err);
      setIsAuthenticated(false);
      setUserRole(null);
      setUserId(null); // <-- Wyczyść userId w przypadku błędu
      const errorMessage = err.response?.data?.error || 'Login failed. Please check your credentials.';
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setIsAuthenticated(false);
    setUserRole(null);
    setUserId(null); // <-- Wyczyść userId po wylogowaniu
  };

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, userRole, userId, login, logout, isLoading }}> {/* <-- Dodaj userId do wartości kontekstu */}
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);