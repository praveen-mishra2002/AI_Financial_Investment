import { useQuery } from "@tanstack/react-query";
import { Alert, Box, Grid, Paper, Typography } from "@mui/material";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import MetricCard from "../components/MetricCard.jsx";
import { getPortfolios } from "../services/api.js";

export default function Dashboard() {
  const { data = [], isError } = useQuery({ queryKey: ["portfolios"], queryFn: getPortfolios });
  const holdings = data.flatMap((portfolio) => portfolio.holdings || []);
  const totalValue = holdings.reduce((sum, holding) => sum + Number(holding.quantity) * Number(holding.average_price), 0);
  const sectorData = Object.values(
    holdings.reduce((acc, holding) => {
      const sector = holding.sector || "Unknown";
      acc[sector] = acc[sector] || { sector, value: 0 };
      acc[sector].value += Number(holding.quantity) * Number(holding.average_price);
      return acc;
    }, {})
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      {isError && <Alert severity="error">Unable to load dashboard data.</Alert>}
      <div className="metric-grid">
        <MetricCard label="Portfolios" value={data.length} helper="Tracked investment accounts" />
        <MetricCard label="Holdings" value={holdings.length} helper="Equity positions under review" />
        <MetricCard label="Portfolio Value" value={`₹${totalValue.toLocaleString("en-IN")}`} helper="Quantity multiplied by average price" />
      </div>
      <Grid container spacing={2} sx={{ mt: 1 }}>
        <Grid item xs={12} lg={8}>
          <Paper variant="outlined" sx={{ p: 3, height: 360 }}>
            <Typography variant="h6" gutterBottom>
              Sector Allocation
            </Typography>
            <ResponsiveContainer width="100%" height="85%">
              <BarChart data={sectorData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="sector" />
                <YAxis />
                <Tooltip formatter={(value) => `₹${Number(value).toLocaleString("en-IN")}`} />
                <Bar dataKey="value" fill="#0f766e" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} lg={4}>
          <Paper variant="outlined" sx={{ p: 3, minHeight: 360 }}>
            <Typography variant="h6">System Status</Typography>
            <Typography sx={{ mt: 2 }}>Market data, scoring, recommendations, and audit logging are available through the backend API.</Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
