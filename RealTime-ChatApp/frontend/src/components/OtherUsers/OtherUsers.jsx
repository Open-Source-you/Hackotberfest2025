import OtherUser from "../OtherUser/OtherUser";
import useGetOtherUsers from "../../hooks/useGetOtherUsers";
import { useSelector } from "react-redux";
const OtherUsers = () => {
  // my custom Hook
  useGetOtherUsers();
  const {otherUsers} = useSelector(store => store.user);
  if( !otherUsers ) return ; //early return in react
  return (
    <div className="  rounded-lg p-2 max-h-96 overflow-y-auto  ">
      {
        otherUsers?.map((user)=>{
        return (
          <OtherUser key={user._id} user={user}/>
        )
})}
    </div>
  );
};

export default OtherUsers;
