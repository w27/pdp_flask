import { Box, Button, Card, CardActionArea, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useAx } from "./axios";
import { TCourse } from "./types";
import EditIcon from "@mui/icons-material/Edit";
import AddIcon from "@mui/icons-material/Add";
import { Navigate, useNavigate } from "react-router-dom";
import { useStorage } from "./useStorage";

export const Courses = () => {
  const navigate = useNavigate();
  const ax = useAx();
  const [data, setData] = useStorage();
  return (
    <Box
      display="flex"
      p={5}
      sx={{ flex: 1 }}
      flexDirection="column"
      justifyContent="flex-start"
      alignItems={"flex-start"}
    >
      <Card
        sx={{ margin: 1, width: 500, display: "flex", background: "#0d46a0" }}
        onClick={() => {
          navigate("/course/new");
        }}
      >
        <CardActionArea sx={{ display: "flex" }}>
          <Typography color="white" flex={1} m={2}>
            Создать курс
          </Typography>
          <Box mx={2.5}>
            <AddIcon sx={{ color: "white" }} />
          </Box>
        </CardActionArea>
      </Card>
      {data.courses.map((c) => (
        <Card
          key={c.key}
          sx={{ margin: 1, width: 500, display: "flex" }}
          onClick={() => {
            navigate(`/course/${c.slug_name}`);
          }}
        >
          <CardActionArea sx={{ display: "flex" }}>
            <Typography flex={1} m={2}>
              {c.name}
            </Typography>
          </CardActionArea>
          <Button
            onClick={(e) => {
              // window.location.href = `/course/${c.slug_name}`;
            }}
          >
            <EditIcon />
          </Button>
        </Card>
      ))}
    </Box>
  );
};
