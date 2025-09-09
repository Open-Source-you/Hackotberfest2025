import React, { useEffect } from 'react'
import SendInput from '../SendInput/SendInput';
import Messages from '../Messages/Messages';
import { useSelector , useDispatch } from 'react-redux';
import { setselectedUser } from '../../redux/userSlice';

const MessageContainer = () => {
  const {selectedUser } = useSelector(store=> store.user)
    const dispatch = useDispatch();
  useEffect(()=>{
  }, [])
  if(!selectedUser)
    return (
     <></>
    );
  return (
    <div className="text-black bg-zinc-200 rounded-3xl ml-2  border  md:min-w-[550px]  flex flex-col px-6 ">
      <div className='p-2'>
        <div>
          <div className="  justify-center " >
            <div className=" flex gap-2 text-white items-center bg-zinc-800  rounded-3xl cursor-pointer ">
              <div className=" ">
                <div className="w-12 rounded-full">
                  <img
                    src={selectedUser?.profilePhoto}
                    alt=""
                  />
                </div>
              </div>
              <div className="flex flex-col flex-1 ">
                <div className="flex justify-between gap-2"></div>
                <p className="text-xl leading-tight"> {selectedUser?.fullName}</p>
              </div>
            </div>
            {/* <div className=" divider my-0 py-0 h-1"></div> */}
          </div>
        </div>
      </div>  
      <Messages/>
      <SendInput/>
    </div>
  );
}

export default MessageContainer
