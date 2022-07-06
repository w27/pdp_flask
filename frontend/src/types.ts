export type TCourse = {
  id: number;
  name: string;
  key: string;
  slug_name: string;
};

export type TTask = {
  course_id: number;
  flag: null;
  id: number;
  name: string;
  res: string;
  task: string;
};
