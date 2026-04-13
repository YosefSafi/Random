import argparse
import sys
from models import Task, Priority, Status
from storage import Storage
from datetime import datetime

def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    
    print(f"{'ID':<10} | {'Title':<25} | {'Project':<15} | {'Priority':<10} | {'Status':<15} | {'Due Date'}")
    print("-" * 100)
    for task in tasks:
        due = task.due_date if task.due_date else "N/A"
        print(f"{task.id:<10} | {task.title[:25]:<25} | {task.project[:15]:<15} | {task.priority.value:<10} | {task.status.value:<15} | {due}")

def main():
    parser = argparse.ArgumentParser(description="NexusTask CLI - Advanced Project Management")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--desc", help="Task description", default="")
    add_parser.add_argument("--project", help="Project name", default="Default")
    add_parser.add_argument("--priority", choices=[p.value for p in Priority], default="MEDIUM")
    add_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--project", help="Filter by project")
    list_parser.add_argument("--priority", help="Filter by priority")
    list_parser.add_argument("--status", help="Filter by status")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update task status")
    update_parser.add_argument("id", help="Task ID")
    update_parser.add_argument("status", choices=[s.value for s in Status])

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", help="Task ID")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export tasks to Markdown")
    export_parser.add_argument("filename", help="Output markdown filename")

    args = parser.parse_args()
    storage = Storage()
    tasks = storage.load_tasks()

    if args.command == "add":
        new_task = Task(
            title=args.title,
            description=args.desc,
            project=args.project,
            priority=Priority(args.priority),
            due_date=args.due
        )
        tasks.append(new_task)
        storage.save_tasks(tasks)
        print(f"Task '{args.title}' added with ID: {new_task.id}")

    elif args.command == "list":
        filtered = tasks
        if args.project:
            filtered = [t for t in filtered if t.project.lower() == args.project.lower()]
        if args.priority:
            filtered = [t for t in filtered if t.priority.value.lower() == args.priority.lower()]
        if args.status:
            filtered = [t for t in filtered if t.status.value.lower() == args.status.lower()]
        display_tasks(filtered)

    elif args.command == "update":
        found = False
        for task in tasks:
            if task.id == args.id:
                task.status = Status(args.status)
                found = True
                break
        if found:
            storage.save_tasks(tasks)
            print(f"Updated task {args.id} status to {args.status}")
        else:
            print(f"Task with ID {args.id} not found.")

    elif args.command == "delete":
        new_tasks = [t for t in tasks if t.id != args.id]
        if len(new_tasks) < len(tasks):
            storage.save_tasks(new_tasks)
            print(f"Deleted task {args.id}")
        else:
            print(f"Task with ID {args.id} not found.")

    elif args.command == "export":
        with open(args.filename, 'w') as f:
            f.write("# NexusTask Export\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("| ID | Title | Project | Priority | Status | Due |\n")
            f.write("|---|---|---|---|---|---|\n")
            for task in tasks:
                due = task.due_date if task.due_date else "N/A"
                f.write(f"| {task.id} | {task.title} | {task.project} | {task.priority.value} | {task.status.value} | {due} |\n")
        print(f"Exported {len(tasks)} tasks to {args.filename}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
