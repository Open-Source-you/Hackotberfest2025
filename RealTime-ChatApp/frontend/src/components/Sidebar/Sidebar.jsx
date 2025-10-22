import React from "react";
import { BiSearchAlt2 } from "react-icons/bi";
import OtherUsers from "../OtherUsers/OtherUsers";
import toast from 'react-hot-toast'
import axios from 'axios'
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { setAuthUser } from "../../redux/userSlice";
const Sidebar = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const logoutHandler = async()=>{
   try{
    const res = await axios.get(`http://localhost:8080/api/v1/user/logout`);
    navigate('/login')
    toast.success(res.data.message)
    dispatch(setAuthUser(null))
   }
   catch(error){
    if(axios.isAxiosError(error)){
      const message = error?.data?.message || 'An error Occured. try again!'
      toast.error(message);
    }
    console.log(error)
   }
  }
  return (
    <div className="bg-zinc-200 w-full p-2 rounded-lg shadow-md h-full bg-gray-200 bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 border border-gray-100 border-rose-950 flex flex-col">
      {/* Search Bar */}
      <form action="" className="flex items-center gap-2 mb-4">
        <input
          className="w-full px-4 py-2 bg-zinc-800 text-white rounded-md border border-gray-600 focus:outline-none   "
          type="text"
          placeholder="Search"
        />
        <button
          type="submit"
          className="px-3 py-2 bg-green-500 hover:bg-green-600 text-white rounded-md"
        >
          <BiSearchAlt2 size="24px" className="w-6 h-6" />
        </button>
      </form>

      {/* Divider */}
      <div className="divider mb-4"></div>

      {/* Other Users with scroll but no scrollbar */}
      <div className="flex-1 overflow-y-auto  ">
        <OtherUsers />
      </div>
      <div className="mt-2  ">
        <button onClick={logoutHandler} className=" btn bg-red-700 border-none text-white btn-sm">
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
