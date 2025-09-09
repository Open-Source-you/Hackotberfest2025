import { useSelector } from 'react-redux';

const useGetAuthUser = () => {
  const { authUser } = useSelector((store) => store.user);
  return authUser
}

export default useGetAuthUser
