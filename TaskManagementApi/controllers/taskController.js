const Task = require('../models/task');

const createTask = (req, res) => {
  const { title, description, userId } = req.body;

  Task.create(title, description, userId, (err, result) => {
    if (err) return res.status(500).json(err);
    res.status(201).json({ message: 'Task created successfully!' });
  });
};

const getTasks = (req, res) => {
  const userId = req.user.id; // Assume user ID is added to req by auth middleware

  Task.findAll(userId, (err, tasks) => {
    if (err) return res.status(500).json(err);
    res.json(tasks);
  });
};

// Add updateTask and deleteTask similarly

const updateTask = (req, res) => {
    const taskId = req.params.id; // Get the task ID from the request parameters
    const { title, description } = req.body; // Extract title and description from the request body

    // Validate if the taskId and required fields are provided
    if (!taskId) {
        return res.status(400).json({ message: "Task ID is required." });
    }

    Task.update(taskId, title, description, (err, result) => {
        if (err) return res.status(500).json(err);

        if (result.affectedRows === 0) {
            return res.status(404).json({ message: "Task not found." });
        }

        res.json({ message: "Task updated successfully!" });
    });
};

const deleteTasks = (req,res)=>{
    const taskId = req.user.id;

    Task.delete(taskId, (err, tasks) => {
        if(err) return res.status(500).json(err);
        res.json(tasks);
    });
}

module.exports = { createTask, getTasks,updateTasks,deleteTasks };
