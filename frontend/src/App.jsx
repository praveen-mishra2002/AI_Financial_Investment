import { Navigate, Route, BrowserRouter as Router, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Portfolio from "./pages/Portfolio.jsx";
import Recommendations from "./pages/Recommendations.jsx";
import Analysis from "./pages/Analysis.jsx";
import Login from "./pages/Login.jsx";
import { AuthProvider, useAuth } from "./contexts/AuthContext.jsx";

function Protected({ children }) {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <Protected>
                <AppLayout />
              </Protected>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="portfolio" element={<Portfolio />} />
            <Route path="recommendations" element={<Recommendations />} />
            <Route path="analysis" element={<Analysis />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}
