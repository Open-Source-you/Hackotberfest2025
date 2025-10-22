import React from "react";
import MessageContainer from "../MessageContainer/MessageContainer";
import Sidebar from "../Sidebar/Sidebar";

const HomePage = () => {
  return (
    <div className="min-w-96 mx-auto">
      <div className="w-full p-6 rounded-lg shadow-md h-full w-full bg-gray-200 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 border border-gray-100 border-rose-950">
        <h1 className="text-3xl font-bold text-center text-green-500 mb-4">
         Textify
        </h1>

        <div className="flex sm:h-[450px] md:h-[550px] rounded-lg overflow-auto bg-gray-400 bg-clip-padding backdrop-filter backdrop-blur-lg bg-opacity-0">
          <Sidebar />
          <MessageContainer />
        </div>
      </div>
    </div>
  );
};

export default HomePage;
