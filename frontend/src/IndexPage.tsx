import { useContext, useEffect } from "react";
import { AuthContext } from "./auth";

export const IndexPage = () => {
  const authContext = useContext(AuthContext);
  useEffect(() => {
    if (authContext.token) {
      window.location.href = "/courses";
    } else {
      window.location.href = "/login";
    }
  }, []);
  return null;
};
