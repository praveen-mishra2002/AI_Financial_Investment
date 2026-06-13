import { useState } from "react";
import { Alert, Box, Button, Paper, Stack, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext.jsx";

export default function Login() {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ email: "", password: "", full_name: "" });
  const [error, setError] = useState("");
  const { login, register } = useAuth();
  const navigate = useNavigate();

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      if (mode === "register") {
        await register(form);
      } else {
        await login({ email: form.email, password: form.password });
      }
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed");
    }
  }

  return (
    <Box sx={{ minHeight: "100vh", display: "grid", placeItems: "center", bgcolor: "background.default", px: 2 }}>
      <Paper variant="outlined" sx={{ width: "100%", maxWidth: 420, p: 4 }}>
        <Typography variant="h4">AI Investment Copilot</Typography>
        <Typography color="text.secondary" sx={{ mt: 1, mb: 3 }}>
          Sign in to manage portfolios and generate explainable recommendations.
        </Typography>
        <Stack component="form" spacing={2} onSubmit={submit}>
          {error && <Alert severity="error">{error}</Alert>}
          {mode === "register" && (
            <TextField label="Full name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required />
          )}
          <TextField label="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <TextField label="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <Button type="submit" variant="contained" size="large">
            {mode === "register" ? "Create Account" : "Sign In"}
          </Button>
          <Button onClick={() => setMode(mode === "login" ? "register" : "login")}>
            {mode === "login" ? "Create a new account" : "Use existing account"}
          </Button>
        </Stack>
      </Paper>
    </Box>
  );
}
