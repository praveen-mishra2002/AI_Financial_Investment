import { AccountCircle, Analytics, Dashboard, Inventory2, Logout, TrendingUp } from "@mui/icons-material";
import {
  AppBar,
  Box,
  Button,
  Container,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography
} from "@mui/material";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext.jsx";

const navItems = [
  { label: "Dashboard", path: "/", icon: <Dashboard /> },
  { label: "Portfolio", path: "/portfolio", icon: <Inventory2 /> },
  { label: "Recommendations", path: "/recommendations", icon: <TrendingUp /> },
  { label: "Analysis", path: "/analysis", icon: <Analytics /> }
];

export default function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const drawerWidth = 260;

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <AppBar position="fixed" color="inherit" elevation={0} sx={{ borderBottom: "1px solid #e5e7eb", zIndex: 1300 }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            AI Investment Copilot
          </Typography>
          <Button startIcon={<AccountCircle />} color="inherit">
            {user?.full_name || "Investor"}
          </Button>
          <IconButton
            aria-label="logout"
            onClick={() => {
              logout();
              navigate("/login");
            }}
          >
            <Logout />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          "& .MuiDrawer-paper": { width: drawerWidth, borderRight: "1px solid #e5e7eb" }
        }}
      >
        <Toolbar />
        <List sx={{ px: 1 }}>
          {navItems.map((item) => (
            <ListItemButton
              key={item.path}
              component={NavLink}
              to={item.path}
              sx={{
                borderRadius: 1,
                mb: 0.5,
                "&.active": { bgcolor: "primary.main", color: "white", "& .MuiListItemIcon-root": { color: "white" } }
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          ))}
        </List>
        <Divider />
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, pt: 10, pb: 5 }}>
        <Container maxWidth="xl">
          <Outlet />
        </Container>
      </Box>
    </Box>
  );
}
