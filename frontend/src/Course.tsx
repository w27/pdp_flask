import { Button, Card, Typography } from "@mui/material";
import { Box } from "@mui/system";
import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { useAx } from "./axios";
import { TCourse, TTask } from "./types";

export const Course = () => {
  const { courseSlug } = useParams();
  console.log(courseSlug);
  const ax = useAx();
  const [course, setCourse] = useState<TCourse | null>(null);
  const [tasks, setTasks] = useState<TTask[]>([]);
  useEffect(() => {
    ax.get(`/course/${courseSlug}`).then((r) => {
      setCourse(r.data.message);
    });
    ax.get(`/tasks/${courseSlug}`).then((r) => {
      console.log("r.data", r);
      setTasks(r.data["course tasks"]);
    });
  }, []);
  return (
    <Box
      display="flex"
      p={5}
      sx={{ flex: 1 }}
      flexDirection="column"
      justifyContent="flex-start"
      alignItems={"flex-start"}
    >
      <>
        <Typography m={1} variant="h4">
          {course?.name}
        </Typography>
        {tasks?.map((task) => (
          <Button
            onClick={() => {
              window.location.href = `/course/${courseSlug}/task/${task.id}`;
            }}
            sx={{ justifyContent: "flex-start", width: 400 }}
          >
            {task.name}
          </Button>
        ))}
      </>
    </Box>
  );
};
