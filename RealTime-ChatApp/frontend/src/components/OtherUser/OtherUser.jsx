import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { setselectedUser } from "../../redux/userSlice";

const OtherUser = (props) => {
  const dispatch = useDispatch();
  const { selectedUser, onlineUsers } = useSelector((store) => store.user);
  const user = props.user;

  // Check if the user is online
  const isOnline = onlineUsers?.some((id) => id === user._id); // Ensure comparison is correct

  const selectedUserHandler = (user) => {
    dispatch(setselectedUser(user));
  };

  return (
    <>
      <div
        onClick={() => selectedUserHandler(user)}
        className={`${
          selectedUser?._id === user?._id ? "bg-zinc-600 text-white" : ""
        } m-2 flex gap-2 items-center rounded-3xl cursor-pointer overflow-hidden text-black`}
      >
        {/* Online status indicator with avatar */}
        <div className="relative w-12 h-12 rounded-full overflow-hidden">
          <img
            className="w-full h-full object-cover"
            src={`https://avatar.iran.liara.run/public/boy/${user?.profilePhoto}`}
            alt={`${user?.fullName}'s profile`}
          />
          {isOnline && (
            <span className="  online absolute top-1 right-1 w-3 h-3 bg-green-500 border-2 border-white rounded-full"></span>
          )}
        </div>

        {/* User's name */}
        <div className="flex flex-col flex-1 ml-2">
          <p className="font-medium">{user?.fullName}</p>
        </div>
      </div>
    </>
  );
};

export default OtherUser;
