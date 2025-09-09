import React, { useRef, useState } from "react";
import { IoSend } from "react-icons/io5";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { setMessages } from "../../redux/messageSlice";
import useGetMessages from "../../hooks/useGetMessages";
import useGetRealTimeMessage from "../../hooks/useGetRealTimeMessage";
const SendInput = () => {
  
const [message, setMessage] = useState("");
  const dispatch = useDispatch();
  const {selectedUser} = useSelector(store => store.user);
  const {messages} = useSelector(store => store.message);
  const onSubmitHandler = async (e) => {
    e.preventDefault();
    
    try {
      const res = await axios.post(
        `http://localhost:8080/api/v1/message/send/${selectedUser?._id}`,
        {message},
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,
        }
      ); 
      console.log(res)
      dispatch(setMessages([...messages ,res?.data?.newMessage]))
      
    } catch (error) {
      console.log(error);
    }
    setMessage("")  };
  return (
    <form onSubmit={onSubmitHandler} className="px-4 my-3">
      <div className="w-full relative">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Send a message..."
          className="w-full p-3 pl-4 text-sm rounded-lg block bg-gray-700 text-white focus:outline-none  "
        />
        <button
          type="submit"
          className="absolute inset-y-0 right-0 text-white flex items-center pr-4 text-green-400  hover:text-green-700 transition-colors"
        >
          <IoSend size="20px" />
        </button>
      </div>
    </form>
  );
};

export default SendInput;
