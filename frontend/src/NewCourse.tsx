import { Button, TextField, Typography } from "@mui/material";
import { Box } from "@mui/system";
import BackIcon from "@mui/icons-material/ArrowBack";
import { useState } from "react";
import slugify from "slug";
import { useNavigate } from "react-router";
import { useAx } from "./axios";
import { useStorage } from "./useStorage";

export const NewCourse = () => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");
  const [slugPristine, setSlugPristine] = useState(true);
  const [secret, setSecret] = useState("");
  const ax = useAx();

  const [data, setData] = useStorage();
  return (
    <Box
      display="flex"
      p={5}
      sx={{ flex: 1 }}
      width={500}
      flexDirection="column"
      justifyContent="flex-start"
      alignItems={"flex-start"}
    >
      <Box display="flex" alignItems="ceter">
        <Button onClick={() => navigate("/courses")}>
          <BackIcon />
        </Button>
        <Typography variant="h5">Новый курс</Typography>
      </Box>
      <TextField
        sx={{ width: 300 }}
        value={name}
        onChange={(e) => {
          setName(e.target.value);
          if (slugPristine) {
            setSlug(slugify(e.target.value));
          }
        }}
        size="small"
        required
        margin="dense"
        variant="standard"
        label="Название"
      />
      <TextField
        sx={{ width: 300 }}
        value={slug}
        onChange={(e) => {
          setSlugPristine(false);
          setSlug(slugify(e.target.value));
        }}
        size="small"
        required
        margin="dense"
        variant="standard"
        label="Slug"
      />
      <TextField
        sx={{ width: 300 }}
        value={secret}
        onChange={(e) => setSecret(e.target.value)}
        size="small"
        required
        margin="dense"
        variant="standard"
        label="Secret"
      />
      <Box my={2}>
        <Button
          variant="contained"
          disabled={!name || !slug || !secret}
          onClick={() => {
            setData({
              ...data,
              courses: [
                ...data.courses,
                {
                  name,
                  key: secret,
                  slug_name: slug,
                  tasks: [],
                },
              ],
            });
          }}
        >
          Создать
        </Button>
      </Box>
    </Box>
  );
};
