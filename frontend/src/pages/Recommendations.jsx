import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { Alert, Box, Button, Chip, Drawer, Grid, Paper, Stack, TextField, Typography } from "@mui/material";
import { AutoAwesome, Info } from "@mui/icons-material";
import { generateRecommendations } from "../services/api.js";

export default function Recommendations() {
  const [amount, setAmount] = useState("100000");
  const [tickers, setTickers] = useState("TCS, INFY, HDFCBANK");
  const [selected, setSelected] = useState(null);
  const mutation = useMutation({
    mutationFn: () =>
      generateRecommendations({
        investment_amount: amount,
        candidates: tickers.split(",").map((ticker) => ({ ticker: ticker.trim() })).filter((item) => item.ticker)
      })
  });

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Recommendations
      </Typography>
      <Paper variant="outlined" sx={{ p: 3, mb: 2 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={3}>
            <TextField fullWidth label="Investment amount" value={amount} onChange={(e) => setAmount(e.target.value)} />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField fullWidth label="Candidate tickers" value={tickers} onChange={(e) => setTickers(e.target.value)} />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button fullWidth size="large" variant="contained" startIcon={<AutoAwesome />} onClick={() => mutation.mutate()}>
              Generate
            </Button>
          </Grid>
        </Grid>
      </Paper>
      {mutation.isError && <Alert severity="error">Recommendation generation failed.</Alert>}
      <Grid container spacing={2}>
        {(mutation.data?.recommendations || []).map((item) => (
          <Grid key={item.ticker} item xs={12} md={6} xl={4}>
            <Paper variant="outlined" sx={{ p: 3, height: "100%" }}>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="h6">{item.ticker}</Typography>
                <Chip label={item.action} color={item.action.includes("Buy") ? "success" : item.action === "Sell" ? "error" : "warning"} />
              </Stack>
              <Typography sx={{ mt: 2 }}>Score: {item.final_score}</Typography>
              <Typography>Confidence: {item.confidence}</Typography>
              <Typography>Allocation: ₹{Number(item.allocation_amount || 0).toLocaleString("en-IN")}</Typography>
              <Button sx={{ mt: 2 }} startIcon={<Info />} onClick={() => setSelected(item)}>
                Details
              </Button>
            </Paper>
          </Grid>
        ))}
      </Grid>
      <Drawer anchor="right" open={Boolean(selected)} onClose={() => setSelected(null)}>
        <Box sx={{ width: 420, p: 3 }}>
          <Typography variant="h5">{selected?.ticker}</Typography>
          <Typography sx={{ mt: 2 }}>{selected?.explanation?.summary}</Typography>
          <Typography variant="h6" sx={{ mt: 3 }}>
            Strengths
          </Typography>
          {(selected?.explanation?.key_strengths || []).map((item) => (
            <Typography key={item}>{item}</Typography>
          ))}
          <Typography variant="h6" sx={{ mt: 3 }}>
            Risks
          </Typography>
          {(selected?.explanation?.key_risks || []).map((item) => (
            <Typography key={item}>{item}</Typography>
          ))}
          <Typography color="text.secondary" sx={{ mt: 3 }}>
            {selected?.explanation?.confidence_commentary}
          </Typography>
        </Box>
      </Drawer>
    </Box>
  );
}
