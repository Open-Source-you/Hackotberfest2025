import dotenv from "dotenv";
dotenv.config();
import express from "express";
import mongoose from "mongoose";
import connectDB from "./connectDb.js";
import ChatBotRoute from "./routes/chatBot.route.js";
import cors from "cors";
import multer from "multer";
import fs from "fs";

// Ensure uploads directory exists
const uploadDir = "./uploads";
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Connect to MongoDB
connectDB();

// Multer configuration
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "./uploads");
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(null, file.fieldname + "-" + uniqueSuffix);
  },
});

const upload = multer({ storage: storage });

// Routes
app.post("/upload/pdf", upload.single("pdf"), (req, res, next) => {
  try {
    if (!req.file) {
      return res.status(400).json({ message: "No file uploaded" });
    }
    return res.json({ message: "File uploaded successfully", file: req.file });
  } catch (error) {
    next(error);
  }
});

app.use("/api/v1/chatbot", ChatBotRoute);

app.get("/", (req, res) => {
  res.send("Server is running");
});

// Global error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ message: "Something went wrong", error: err.message });
});

// Start server
const port = process.env.PORT || 8800;
app.listen(port, () => {
  console.log(`Server is listening on http://localhost:${port}`);
});
