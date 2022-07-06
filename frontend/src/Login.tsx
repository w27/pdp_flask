import { assertExpressionStatement } from "@babel/types";
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
import { useCallback, useState } from "react";
import { ax } from "./axios";

export const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const onSubmit = useCallback(() => {
    setError("");
    ax.post("/auth", { username, password })
      .then((r) => {
        if (r.data.access_token) {
          window.localStorage.setItem("token", r.data.access_token);
          window.localStorage.setItem("refreshToken", r.data.refreshToken);
          window.location.href = "/courses";
        }
      })
      .catch((e: { message: string }) => {
        setError(e.message);
      });
  }, [username, password]);
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
        <Button sx={{ marginTop: 2 }} onClick={onSubmit} variant="contained">
          Войти
        </Button>
        {!!error && (
          <Typography mt={1} variant="subtitle2" sx={{ color: "red" }}>
            {error}
          </Typography>
        )}
      </Box>
    </>
  );
};
