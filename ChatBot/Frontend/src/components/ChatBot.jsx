import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { FaUserCircle } from "react-icons/fa";
import { Upload } from "lucide-react";
import { Paperclip } from "lucide-react";

function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [uploadedFile, setUploadedFile] = useState([]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    setLoading(true);

    try {
      const res = await axios.post(
        "http://localhost:8080/api/v1/chatbot/message",
        {
          textQuery: input,
        }
      );

      if (res.data.success) {
        setMessages((prev) => [
          ...prev,
          { text: res.data.userText, sender: "user" },
          { text: res.data.chatBotResponse, sender: "bot" },
        ]);
      }
    } catch (error) {
      console.error("Error sending message:", error);
    }

    setInput("");
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSendMessage();
  };

  const handleFileUpload = () => {
    const elm = document.createElement("input");
    elm.setAttribute("type", "file");
    elm.setAttribute("accept", "application/pdf");

    elm.addEventListener("change", async (e) => {
      if (elm.files && elm.files.length > 0) {
        const file = elm.files[0];
        console.log(file);
        if (file) {
          const formData = new FormData();
          formData.append("pdf", file);

          await fetch("http://localhost:8080/upload/pdf", {
            method: "POST",
            body: formData,
          });
          console.log("uploaded");
        }
      }
    });

    elm.click();
  };

  return (
    <div className="flex flex-col min-h-screen bg-[#0d0d0d] text-white">
      {/* Navbar */}
      <header className="fixed top-0 left-0 w-full border-b border-gray-800 bg-[#0d0d0d] z-10">
        <div className="container mx-auto flex justify-between items-center px-6 py-4">
          <h1 className="text-lg font-bold">AI-ChatBot</h1>
          <FaUserCircle size={30} className="cursor-pointer" />
        </div>
      </header>
      {/* Chat area */}
      <main className="flex-1 overflow-y-auto pt-20 pb-24 flex items-center justify-center">
        <div className="w-full max-w-4xl mx-auto px-4 flex flex-col space-y-3">
          {messages.length === 0 ? (
            <div className="text-center text-gray-400 text-lg">
              👋 Hi, I'm{" "}
              <span className="text-green-500 font-semibold">AI-ChatBot</span>.
            </div>
          ) : (
            <>
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`px-4 py-2 rounded-xl max-w-[75%] ${
                    msg.sender === "user"
                      ? "bg-blue-600 text-white self-end"
                      : "bg-gray-800 text-gray-100 self-start"
                  }`}
                >
                  {msg.text}
                </div>
              ))}

              {loading && (
                <div className="bg-gray-700 text-gray-300 px-4 py-2 rounded-xl max-w-[60%] self-start">
                  ChatBot is typing...
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </main>

      <footer className="fixed bottom-0 left-0 w-full border-t border-gray-800 bg-[#0d0d0d] z-10">
        <div className="max-w-4xl mx-auto flex justify-center px-4 py-3">
          <div className="w-full flex items-center bg-gray-900 rounded-full px-3 py-2 shadow-lg space-x-2">
            <button
              onClick={handleFileUpload}
              className="flex items-center justify-center w-10 h-10 rounded-full  hover:bg-gray-700 transition-colors"
            >
              <Paperclip className="text-gray-300" />
            </button>

            {/* Input Field */}
            <input
              type="text"
              className="flex-1 bg-transparent outline-none text-white placeholder-gray-400 px-2"
              placeholder="Ask AI-ChatBot..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
            />

            <button
              onClick={handleSendMessage}
              className="flex items-center justify-center px-5 py-2  rounded-full  bg-green-600 hover:bg-green-700 text-white font-medium transition-colors"
            >
              Send
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default ChatBot;
