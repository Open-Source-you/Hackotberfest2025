import React from "react";
import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";
import HomePage from "../components/HomePage/HomePage.jsx";
import Signup from "../components/Signup/Signup.jsx";
import Login from "../components/Login/Login.jsx";
import { useSelector } from "react-redux";
import useGetAuthUser from "../hooks/useGetAuthUser.jsx";
const ProtectedRoute = ({element})=>{
  return useGetAuthUser() ? element : <Navigate to='/login'/>
}
const router = createBrowserRouter([
  {
    path: "/",
    element: <ProtectedRoute element={<HomePage/>}/> ,
  },
  {
    path: "/register",
    element: <Signup />,
  },
  {
    path: "/login",
    element: <Login />,
  },
]);
const Allroutes = () => {
  return <RouterProvider router={router} />;
};

export default Allroutes;
