import {
  Box,
  Button,
  Card,
  Container,
  FormLabel,
  Grid,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";

export const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  return (
    <>
      <Typography variant="h5">Курсы шмурсы</Typography>
      <Box display="flex" flexDirection="column">
        <TextField
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          size="small"
          required
          margin="dense"
          variant="standard"
          label="Username"
        />
        <TextField
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          size="small"
          required
          margin="dense"
          variant="standard"
          label="Password"
        />
        <Button sx={{ marginTop: 2 }} variant="contained">
          Войти
        </Button>
      </Box>
    </>
  );
};
