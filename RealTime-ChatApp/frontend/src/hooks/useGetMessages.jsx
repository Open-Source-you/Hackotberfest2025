import { useEffect } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { setMessages } from "../redux/messageSlice";

const useGetMessages = () => {
  const { selectedUser } = useSelector((store) => store.user);
  const dispatch = useDispatch();
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        
        if (selectedUser?._id) {
          // Ensure selectedUser has a valid ID before fetching
          const selectedUserId = selectedUser._id;
          axios.defaults.withCredentials = true;
          const res = await axios.get(
            `http://localhost:8080/api/v1/message/${selectedUserId}`
          );
          dispatch(setMessages(res.data))
        }
      } catch (error) {
        console.log("Error fetching messages:", error);
      }
    };

    fetchMessages();
  }, [selectedUser]); // Add selectedUser as a dependency
};

export default useGetMessages;
