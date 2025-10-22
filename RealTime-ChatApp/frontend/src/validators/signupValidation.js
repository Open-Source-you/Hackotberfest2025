import * as Yup from "yup";

const signupValidationSchema = Yup.object().shape({
  fullName: Yup.string().required("Full Name is required"),
  username: Yup.string().min(3, "Username must be at least 3 characters").required("Username is required"),
  password: Yup.string().min(8, "Password must be at least 8 characters").required("Password is required"),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref("password"), null], "Passwords must match")
    .required("Confirm Password is required"),
  gender: Yup.string().required("Please select your gender"),
});

export default signupValidationSchema;
