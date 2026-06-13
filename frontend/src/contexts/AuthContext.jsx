import { createContext, useContext, useMemo, useState } from "react";
import { login as apiLogin, register as apiRegister } from "../services/api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("access_token"));
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  const value = useMemo(
    () => ({
      token,
      user,
      async login(payload) {
        const data = await apiLogin(payload);
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));
        setToken(data.access_token);
        setUser(data.user);
      },
      async register(payload) {
        await apiRegister(payload);
        const data = await apiLogin({ email: payload.email, password: payload.password });
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));
        setToken(data.access_token);
        setUser(data.user);
      },
      logout() {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        setToken(null);
        setUser(null);
      }
    }),
    [token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
