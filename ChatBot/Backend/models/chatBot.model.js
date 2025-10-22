import mongoose from "mongoose";
import User from "./user.model.js";

const chatBotSchema = new mongoose.Schema({
  textQuery: {
    type: String,
    require: true,
  },

  chatBotResponse: {
    type: String,
    require: true,
  },
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: User,
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
});

const ChatBot = mongoose.model("ChatBot", chatBotSchema);

export default ChatBot;
