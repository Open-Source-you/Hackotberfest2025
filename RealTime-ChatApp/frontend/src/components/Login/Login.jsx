import { Link ,useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import loginValidationSchema from "../../validators/loginValidation"; 
import axios from 'axios'
import toast from 'react-hot-toast'
import { useDispatch } from "react-redux";
import { setAuthUser } from "../../redux/userSlice";
const Login = () => {
  const initialValues = {
    username: "",
    password: "",
  };
  const dispatch = useDispatch();
  const navigate = new useNavigate()

  const handleSubmit = async (values) => {
    console.log("Input data : ", values); // Log form values upon successful login
    try{
      const res = await axios.post("http://localhost:8080/api/v1/user/login" , values, {
      headers:{
        'Content-Type':'application/json'},
         withCredentials:true
    } );
    if(res.status == 200 || res.status == 201){
      navigate('/')
      toast.success(res.data.message)
    }
    dispatch(setAuthUser(res.data))
    }
    catch(error){
      if(axios.isAxiosError(error)){
        const message = error.response?.data?.message || " An error Occurred. Please try again."
        toast.error(message)
      }
      console.log(error)
    }
  };

  return (
    <div className="min-w-96 mx-auto">
      <div className="w-full p-6 rounded-lg shadow-md h-full w-full bg-gray-200 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 border border-gray-100 border-rose-950">
        <h1 className="text-3xl font-bold text-center text-blue-500">Login</h1>

        {/* Formik for handling form submission and validation */}
        <Formik
          initialValues={initialValues}
          validationSchema={loginValidationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form>
              {/* Username Input Field */}
              <div>
                <label className="label">
                  <span className="text-base label-text text-zinc-800">
                    Username
                  </span>
                </label>
                <Field
                  type="text"
                  name="username"
                  className="w-full bg-zinc-800 text-white input input-border h-10"
                  placeholder="JohnDoe69"
                />
                <ErrorMessage
                  name="username"
                  component="div"
                  className="text-red-500 text-sm"
                />
              </div>

              {/* Password Input Field */}
              <div>
                <label className="label">
                  <span className="text-base label-text text-zinc-800">
                    Password
                  </span>
                </label>
                <Field
                  type="password"
                  name="password"
                  className="w-full bg-zinc-800 text-white input input-border h-10"
                  placeholder="Password"
                />
                <ErrorMessage
                  name="password"
                  component="div"
                  className="text-red-500 text-sm"
                />
              </div>

              {/* Link to signup page */}
              <div className="flex justify-between mt-2">
                <Link to="/register">
                  <p className="text-blue-700 underline">
                    Create new Account ?
                  </p>
                </Link>
              </div>

              {/* Submit Button */}
              <div className="mt-4">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-blue-500 border border-blue-500 text-white py-2 rounded-md hover:bg-white hover:border hover:border-blue-600 hover:text-blue-500"
                >
                  {isSubmitting ? "Logging in..." : "Login"}
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default Login;
