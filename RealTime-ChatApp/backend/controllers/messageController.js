import { Conversation } from '../models/conversationModel.js';
import { Message } from '../models/messageModel.js';
import { getRecieverSocketId, io } from '../socket/socket.js';
import { Server } from 'socket.io';
export const sendMessage = async (req, res) => {
  try {
    const senderId = req.id;
    const recieverId = req.params.id;
    const { message } = req.body;

    let gotConversation = await Conversation.findOne({
      participants: { $all: [senderId, recieverId] },
    })
    if (!gotConversation) {
     gotConversation = await Conversation.create({
      participants:[senderId ,recieverId]
     })
    }
    const newMessage = await Message.create({
      senderId ,
      recieverId ,
      message
    })
    if(newMessage){
      gotConversation.messages.push(newMessage._id)
    }
    await Promise.all([gotConversation.save() , newMessage.save()])
    //socket IO

    const recieverSocketId = getRecieverSocketId(recieverId);
    if(recieverSocketId){
      io.to(recieverSocketId).emit("newMessage", newMessage)
    }

    return res.status(201).json({
      newMessage
    })
   

  }
  catch (error) {
    console.log(error)
  }
}

export const getMessage = async (req, res) => {
  try {
    const recieverId = req.params.id;
    const senderId = req.id; 
    
    // Check if both senderId and recieverId are present
    if (!senderId || !recieverId) {
      return res.status(400).json({ message: "Sender or Receiver ID missing." });
    }

    const conversation = await Conversation.findOne({
      participants: { $all: [senderId, recieverId] },
    }).populate("messages");

    
    return res.status(200).json(conversation?.messages);
  } catch (error) {
    console.log("Error fetching conversation:", error);
    return res.status(500).json({ message: "Server error" });
  }
};
