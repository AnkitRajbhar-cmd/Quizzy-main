import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if token exists
    const token = localStorage.getItem('token');
    if (token) {
       // Ideally fetch user /me here
       setUser({ token }); 
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    // Use JSON login endpoint
    const res = await api.post('/auth/login', { email, password });
    localStorage.setItem('token', res.data.access_token);
    setUser({ token: res.data.access_token });
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    // Optional: redirect to login
    try { window.location.href = '/login'; } catch (e) {}
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
