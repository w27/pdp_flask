import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import App from "./App";
import { AuthContext } from "./auth";
import { Course } from "./Course";
import { Courses } from "./Courses";
import "./index.css";
import { IndexPage } from "./IndexPage";
import { Login } from "./Login";
import { NewCourse } from "./NewCourse";
import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

const token = window.localStorage.getItem("token") || "";
const refreshToken = window.localStorage.getItem("refreshToken") || "";

root.render(
  <AuthContext.Provider
    value={{
      token,
      refreshToken,
    }}
  >
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<IndexPage />}></Route>
        <Route path="login" element={<Login />}></Route>
        <Route path="courses" element={<Courses />}></Route>
        <Route path="course/new" element={<NewCourse />}></Route>
        <Route path="course/:courseSlug" element={<Course />}></Route>
      </Routes>
    </BrowserRouter>
  </AuthContext.Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
