import { Box, Button, Card, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useAx } from "./axios";
import { TCourse } from "./types";

export const Courses = () => {
  const ax = useAx();
  const [courses, setCourses] = useState<TCourse[]>([]);
  useEffect(() => {
    ax.get("/courses").then((r) => {
      setCourses(r.data["course list"]);
    });
  }, [setCourses]);
  return (
    <Box
      display="flex"
      p={5}
      sx={{ flex: 1 }}
      flexDirection="column"
      justifyContent="flex-start"
      alignItems={"flex-start"}
    >
      <Typography my={3} variant="h3">
        Курсы
      </Typography>
      {courses?.map((c) => (
        <Card
          key={c.key}
          sx={{ margin: 1, width: 500, display: "flex" }}
          onClick={() => {}}
        >
          <Typography flex={1} variant="h6" m={2}>
            {c.name}
          </Typography>
          <Button
            onClick={() => {
              window.location.href = `/course/${c.slug_name}`;
            }}
          >
            Проходить
          </Button>
        </Card>
      ))}
    </Box>
  );
};
