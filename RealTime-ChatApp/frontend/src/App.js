import { useEffect, useState } from 'react';
import { useSelector , useDispatch } from 'react-redux';
import io from 'socket.io-client';
import Allroutes from './routes/Allroutes';
import { setSocket } from './redux/socketSlice';
import { setOnlineUsers } from './redux/userSlice';

function App() {
  const { authUser } = useSelector((store) => store.user);
  const { socket } = useSelector((store) => store.socket);
 
  const dispatch = useDispatch();
  useEffect(() => {
    if (authUser) {
      const socket = io('http://localhost:8080', {
      query :{
        userId :authUser._id}
      });
      dispatch(setSocket(socket));
      socket.on('getOnlineUsers', (onlineUsers)=>{
       dispatch(setOnlineUsers(onlineUsers))
      })
      return ()=> socket.close()
    }
    else{
      if(socket)socket.close();
      dispatch(setSocket(null))
    }
  }, [authUser]);

  return (
    <div className="p-4 h-screen flex items-center justify-center">
      <Allroutes />
    </div>
  );
}

export default App;
