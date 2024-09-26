import { createContext, useState, useEffect } from 'react';
import { getToken, setToken, removeToken } from '../utils/tokenUtils';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authToken, setAuthToken] = useState(getToken());

  const login = (token) => {
    setAuthToken(token);
    setToken(token);
  };

  const logout = () => {
    setAuthToken(null);
    removeToken();
  };

  useEffect(() => {
    setAuthToken(getToken());
  }, []);

  const isAuthenticated = !!authToken;  // This is a boolean, true if a token exists

  return (
    <AuthContext.Provider value={{ authToken, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
