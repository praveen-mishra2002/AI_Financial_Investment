import { Card, CardContent, Typography } from "@mui/material";

export default function MetricCard({ label, value, helper }) {
  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {label}
        </Typography>
        <Typography variant="h4" sx={{ mt: 1 }}>
          {value}
        </Typography>
        {helper && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            {helper}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}
