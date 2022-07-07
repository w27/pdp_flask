import { useCallback, useState } from "react";
import { useLocalStorage } from "react-use-storage";

type Course = {
  name: string;
  key: string;
  slug_name: string;
  tasks: CourseTask[];
};

type Student = {
  courses: Course["slug_name"][];
  id: number;
  fio: string;
  first_name: string;
  last_name: string;
  username: string;
  status: string;
};

type CourseTask = {
  id: number;
  name: string;
  course_id: string;
  task: string;
  flag: string;
  res: string;
};

type Data = {
  courses: Course[];
  students: Student[];
};

const INITIAL_DATA: Data = {
  courses: [
    {
      name: "Курс всем курсам курс",
      slug_name: "kurs",
      key: "topsecret",
      tasks: [],
    },
  ],
  students: [
    {
      courses: [],
      id: 0,
      fio: "fio",
      first_name: "fn",
      last_name: "ln",
      username: "username",
      status: "none",
    },
  ],
};

const initialLocalStorageData = localStorage.getItem("data");

export const useStorage = (): [Data, (d: Data) => void] => {
  const [value, setValue] = useLocalStorage(
    "_data",
    JSON.stringify(INITIAL_DATA)
  );

  const updateData = useCallback(
    (newData: Data) => {
      setValue(JSON.stringify(newData));
    },
    [setValue]
  );
  return [JSON.parse(value) as Data, updateData];
};
