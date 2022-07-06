import axios from "axios";
import { useContext } from "react";
import { AuthContext } from "./auth";

export const ax = axios.create({
  baseURL: "http://localhost:5000",
});

export const useAx = () => {
  const { token } = useContext(AuthContext);
  const ax = axios.create({
    baseURL: "http://localhost:5000",
    headers: token
      ? {
          Authorization: `Bearer ${token}`,
        }
      : {},
  });
  ax.interceptors.response.use(
    (r) => {
      return r;
    },
    (error) => {
      if (error.response.status === 401) {
        window.localStorage.setItem("token", "");
        window.localStorage.setItem("refreshToken", "");
        window.location.href = "/login";
      }
    }
  );
  return ax;
};
