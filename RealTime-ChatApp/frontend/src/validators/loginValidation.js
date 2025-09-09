import * as Yup from 'yup';

const loginValidationSchema =Yup.object().shape({
  username :Yup.string().required("Username is required"),
  password : Yup.string().required("Enter the correct Password")
})
export default loginValidationSchema;