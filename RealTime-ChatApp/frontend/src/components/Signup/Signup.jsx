import { Link , useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import signupValidationSchema from "../../validators/signupValidation"; // Importing the Yup validation schema
import axios from 'axios'
import toast from 'react-hot-toast'

const Signup = () => {
  const initialValues = {
    fullName: "",
    username: "",
    password: "",
    confirmPassword: "",
    gender: "",
  };
  const navigate = new useNavigate();

  const handleSubmit = async (values) => {
    console.log("Form Submitted", values);
    try{
      const res = await axios.post(`http://localhost:8080/api/v1/user/register` , values,{
        header: {
          'Content-Type':'application/json'
        },
        withCredentials:true
      })
       if (res.status == 200 || res.status == 201) {
         navigate("/login");
         toast.success(res.data.message);
       }}
    catch(error){
     if(axios.isAxiosError(error)){
      const message = error.response?.data?.message || " An Error Occurred. Please try again."
      toast.error(message)
     }
     console.log(error)
    }
  };

  return (
    <div className="min-w-96 mx-auto">
      <div className="w-full p-6 rounded-lg shadow-md h-full w-full bg-gray-200 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 border border-gray-100 border-rose-950">
        <h1 className="text-3xl font-bold text-center text-blue-500">SignUp</h1>

        <Formik
          initialValues={initialValues}
          validationSchema={signupValidationSchema} // Apply validation schema
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form>
              <div>
                <label className="label">
                  <span className="text-base label-text text-zinc-800">
                    Full Name
                  </span>
                </label>
                <Field
                  type="text"
                  name="fullName"
                  className="w-full bg-zinc-800 text-white input input-border h-10"
                  placeholder="John Doe"
                />
                <ErrorMessage
                  name="fullName"
                  component="div"
                  className="text-red-500 text-sm"
                />
              </div>

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
                  placeholder="password"
                />
                <ErrorMessage
                  name="password"
                  component="div"
                  className="text-red-500 text-sm"
                />
              </div>

              <div>
                <label className="label">
                  <span className="text-base label-text text-zinc-800">
                    Confirm Password
                  </span>
                </label>
                <Field
                  type="password"
                  name="confirmPassword"
                  className="w-full bg-zinc-800 text-white input input-border h-10"
                  placeholder="confirm password"
                />
                <ErrorMessage
                  name="confirmPassword"
                  component="div"
                  className="text-red-500 text-sm"
                />
              </div>

              <div>
                <div className="flex flex-col">
                  <h3 className="text-base label-text text-zinc-800 mt-2 p-1">
                    Select Gender:
                  </h3>
                  <div className="flex gap-2 ml-1">
                    <label className="flex gap-1 text-zinc-800">
                      <Field
                        type="radio"
                        name="gender"
                        value="male"
                        className="focus:ring-0 focus:outline-none"
                      />
                      Male
                    </label>
                    <label className="flex gap-1 text-zinc-800">
                      <Field
                        type="radio"
                        name="gender"
                        value="female"
                        className="focus:ring-0 focus:outline-none"
                      />
                      Female
                    </label>
                  </div>
                  <ErrorMessage
                    name="gender"
                    component="div"
                    className="text-red-500 text-sm"
                  />
                </div>
              </div>

              <div className="flex justify-between mt-2">
                <Link to="/login">
                  <p className="text-blue-700 underline">
                    Already have an Account?
                  </p>
                </Link>
              </div>

              <div className="mt-4">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-blue-500 border border-blue-500 text-white py-2 rounded-md hover:bg-white hover:border hover:border-blue-600 hover:text-blue-500"
                >
                  {isSubmitting ? "Signing Up..." : "Sign Up"}
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default Signup;
