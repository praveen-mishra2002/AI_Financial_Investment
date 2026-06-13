import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1"
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function register(payload) {
  const { data } = await api.post("/auth/register", payload);
  return data;
}

export async function login(payload) {
  const { data } = await api.post("/auth/login", payload);
  return data;
}

export async function getPortfolios() {
  const { data } = await api.get("/portfolio");
  return data;
}

export async function createPortfolio(payload) {
  const { data } = await api.post("/portfolio", payload);
  return data;
}

export async function addHolding(portfolioId, payload) {
  const { data } = await api.post(`/portfolio/${portfolioId}/holding`, payload);
  return data;
}

export async function generateRecommendations(payload) {
  const { data } = await api.post("/recommendations", payload);
  return data;
}

export async function analyzePortfolio(portfolioId) {
  const { data } = await api.post("/portfolio/analyze", { portfolio_id: portfolioId });
  return data;
}

export default api;
