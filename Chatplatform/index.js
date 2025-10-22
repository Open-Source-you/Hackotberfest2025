```javascript
const express = require('express');
const path = require('path');
const http = require('http');
const socketio = require('socket.io');
const { userJoin, userLeave, getCurrentUser, getRoomUsers } = require('./utils/users');
const formatMessage = require('./utils/messages');

const app = express();
app.use(express.static(path.join(__dirname, 'public')));

const server = http.createServer(app);
const io = socketio(server);

const botName = 'Admin';
```
io.on('connection', (socket)=>{
    // socket represents an actual user
    // emit a endt to the client
    // socket.emit("welcomemessage", "Welcome to the chat");
    // socket.on("connected", (data)=>{
    //     console.log(data);
    //     console.log(socket.id + " connected");
    // })
    socket.on("joinRoom", ({ username, room }) => {
        const user = userJoin(socket.id, username, room);

        socket.join(user.room);

        // Welcome current user
        socket.emit("message", formatMessage(botName, "Welcome to command tech!"));

        // Broadcast when a user connects
        socket.broadcast
          .to(user.room)
          .emit(
            "message",
            formatMessage(botName, `${user.username} has joined the chat`)
          );

        // Send users and room info
        io.to(user.room).emit("roomUsers", {
          room: user.room,
          users: getRoomUsers(user.room),
        });
      });

      // Listen for chatMessage
        // Listen for chatMessage
  socket.on("chatMessage", (msg) => {
    const user = getCurrentUser(socket.id);
    io.to(user.room).emit("message", formatMessage(user.username, msg));
  });

      // Runs when client disconnects
      socket.on("disconnect", () => {
        const user = userLeave(socket.id);

        if (user) {
          io.to(user.room).emit(
            "message",
            formatMessage(botName, `${user.username} has left the chat`)
          );

          // Send users and room info
          io.to(user.room).emit("roomUsers", {
            room: user.room,
            users: getRoomUsers(user.room),
          });
        }
      });
    });

    const PORT =  3000;

    server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
