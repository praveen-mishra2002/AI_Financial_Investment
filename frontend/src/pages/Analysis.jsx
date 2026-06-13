import { useMutation, useQuery } from "@tanstack/react-query";
import { Alert, Box, Button, Chip, MenuItem, Paper, Stack, TextField, Typography } from "@mui/material";
import { Analytics } from "@mui/icons-material";
import { analyzePortfolio, getPortfolios } from "../services/api.js";

export default function Analysis() {
  const { data = [] } = useQuery({ queryKey: ["portfolios"], queryFn: getPortfolios });
  const mutation = useMutation({ mutationFn: analyzePortfolio });
  const selectedId = data[0]?.id || "";

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Portfolio Analysis
      </Typography>
      <Paper variant="outlined" sx={{ p: 3, mb: 2 }}>
        <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
          <TextField select label="Portfolio" value={selectedId} sx={{ minWidth: 260 }}>
            {data.map((portfolio) => (
              <MenuItem key={portfolio.id} value={portfolio.id}>
                {portfolio.name}
              </MenuItem>
            ))}
          </TextField>
          <Button variant="contained" startIcon={<Analytics />} disabled={!selectedId} onClick={() => mutation.mutate(selectedId)}>
            Analyze
          </Button>
        </Stack>
      </Paper>
      {mutation.isError && <Alert severity="error">Portfolio analysis failed.</Alert>}
      {mutation.data && (
        <Stack spacing={2}>
          <Paper variant="outlined" sx={{ p: 3 }}>
            <Typography variant="h6">Risk Score: {mutation.data.risk_score}</Typography>
            {mutation.data.warnings.map((warning) => (
              <Chip key={warning} label={warning} color="warning" sx={{ mr: 1, mt: 1 }} />
            ))}
          </Paper>
          {mutation.data.holdings.map((item) => (
            <Paper key={item.ticker} variant="outlined" sx={{ p: 3 }}>
              <Stack direction="row" justifyContent="space-between">
                <Typography variant="h6">{item.ticker}</Typography>
                <Chip label={item.action} />
              </Stack>
              <Typography sx={{ mt: 1 }}>Score: {item.score}</Typography>
              <Typography color="text.secondary">{item.rationale}</Typography>
            </Paper>
          ))}
        </Stack>
      )}
    </Box>
  );
}
