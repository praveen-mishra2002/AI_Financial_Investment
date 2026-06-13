import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Alert, Box, Button, Grid, Paper, Stack, TextField, Typography } from "@mui/material";
import { Add } from "@mui/icons-material";
import { addHolding, createPortfolio, getPortfolios } from "../services/api.js";

export default function Portfolio() {
  const queryClient = useQueryClient();
  const { data = [], isError } = useQuery({ queryKey: ["portfolios"], queryFn: getPortfolios });
  const [portfolioName, setPortfolioName] = useState("");
  const [holding, setHolding] = useState({ ticker: "", company_name: "", sector: "", quantity: "", average_price: "" });
  const activePortfolio = data[0];
  const createMutation = useMutation({ mutationFn: createPortfolio, onSuccess: () => queryClient.invalidateQueries({ queryKey: ["portfolios"] }) });
  const holdingMutation = useMutation({
    mutationFn: (payload) => addHolding(activePortfolio.id, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["portfolios"] })
  });

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Portfolio
      </Typography>
      {isError && <Alert severity="error">Unable to load portfolios.</Alert>}
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Paper variant="outlined" sx={{ p: 3 }}>
            <Typography variant="h6">Create Portfolio</Typography>
            <Stack spacing={2} sx={{ mt: 2 }}>
              <TextField label="Portfolio name" value={portfolioName} onChange={(e) => setPortfolioName(e.target.value)} />
              <Button
                startIcon={<Add />}
                variant="contained"
                onClick={() => createMutation.mutate({ name: portfolioName })}
                disabled={!portfolioName}
              >
                Add Portfolio
              </Button>
            </Stack>
          </Paper>
          <Paper variant="outlined" sx={{ p: 3, mt: 2 }}>
            <Typography variant="h6">Add Holding</Typography>
            <Stack spacing={2} sx={{ mt: 2 }}>
              {["ticker", "company_name", "sector", "quantity", "average_price"].map((field) => (
                <TextField key={field} label={field.replace("_", " ")} value={holding[field]} onChange={(e) => setHolding({ ...holding, [field]: e.target.value })} />
              ))}
              <Button startIcon={<Add />} variant="contained" onClick={() => holdingMutation.mutate(holding)} disabled={!activePortfolio}>
                Add Holding
              </Button>
            </Stack>
          </Paper>
        </Grid>
        <Grid item xs={12} md={8}>
          <Stack spacing={2}>
            {data.map((portfolio) => (
              <Paper key={portfolio.id} variant="outlined" sx={{ p: 3 }}>
                <Typography variant="h6">{portfolio.name}</Typography>
                {(portfolio.holdings || []).map((item) => (
                  <Box key={item.id} sx={{ display: "flex", justifyContent: "space-between", py: 1, borderBottom: "1px solid #edf0ee" }}>
                    <Typography>{item.ticker}</Typography>
                    <Typography color="text.secondary">
                      {item.quantity} @ ₹{item.average_price}
                    </Typography>
                  </Box>
                ))}
              </Paper>
            ))}
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
}
