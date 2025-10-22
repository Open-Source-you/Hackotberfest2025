import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
  sender: {
    type: String,
    require: true,
    enum: ["user"],
  },
  textQuery: {
    type: String,
    require: true,
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
});

const User = mongoose.model("User", userSchema);

export default User;
