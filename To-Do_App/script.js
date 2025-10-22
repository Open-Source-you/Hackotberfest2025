const taskInput = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');
const taskList = document.getElementById('taskList');

// Add task function
addBtn.addEventListener('click', () => {
    const taskText = taskInput.value.trim();
    if(taskText === "") return;

    const li = document.createElement('li');
    li.textContent = taskText;

    // Toggle completed class on click
    li.addEventListener('click', () => {
        li.classList.toggle('completed');
    });

    // Remove task on double click
    li.addEventListener('dblclick', () => {
        li.remove();
    });

    taskList.appendChild(li);
    taskInput.value = '';
});
