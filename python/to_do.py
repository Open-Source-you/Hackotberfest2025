tasks = []

def show_tasks():
    if tasks:
        print("Your tasks:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")
    else:
        print("No tasks available.")

def add_task():
    task = input("Enter a task: ")
    tasks.append(task)
    print(f"Task '{task}' added.")

def remove_task():
    show_tasks()
    try:
        task_num = int(input("Enter task number to remove: ")) - 1
        removed_task = tasks.pop(task_num)
        print(f"Task '{removed_task}' removed.")
    except (IndexError, ValueError):
        print("Invalid task number.")

while True:
    print("\nOptions: 1. Show tasks 2. Add task 3. Remove task 4. Quit")
    choice = input("Choose an option: ")

    if choice == "1":
        show_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        remove_task()
    elif choice == "4":
        break
    else:
        print("Invalid option.")
