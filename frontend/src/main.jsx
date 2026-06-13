import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import App from "./App.jsx";
import "./styles.css";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#14532d" },
    secondary: { main: "#0f766e" },
    warning: { main: "#b45309" },
    error: { main: "#b91c1c" },
    background: { default: "#f7f8f5", paper: "#ffffff" }
  },
  typography: {
    fontFamily: "Inter, Arial, sans-serif",
    h4: { fontWeight: 700 },
    h6: { fontWeight: 700 },
    button: { textTransform: "none", fontWeight: 700 }
  },
  shape: { borderRadius: 8 }
});

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    </ThemeProvider>
  </React.StrictMode>
);
