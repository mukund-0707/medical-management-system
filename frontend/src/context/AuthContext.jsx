import { createContext, useContext, useState } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('msms_user');
    return saved ? JSON.parse(saved) : null;
  });

  const login = async (username, password) => {
    const res = await authAPI.login(username, password);
    const { access, refresh, user: userData } = res.data.data;

    localStorage.setItem('msms_access', access);
    localStorage.setItem('msms_refresh', refresh);
    localStorage.setItem('msms_user', JSON.stringify(userData));
    setUser(userData);
    return userData;
  };

  const logout = async () => {
    try {
      const refresh = localStorage.getItem('msms_refresh');
      if (refresh) await authAPI.logout(refresh);
    } catch {
      // Ignore logout errors — clear local state anyway
    }
    localStorage.removeItem('msms_access');
    localStorage.removeItem('msms_refresh');
    localStorage.removeItem('msms_user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
