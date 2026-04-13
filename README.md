# NexusTask CLI

NexusTask is a powerful, lightweight CLI tool for project and task management. It allows you to organize your work, track priorities, and export reports directly from your terminal.

## Features

- **Project-based organization**: Keep related tasks together.
- **Priority & Status Tracking**: Use Low, Medium, High, or Critical priorities.
- **Automated Backups**: Your data is backed up before every save.
- **Markdown Export**: Generate beautiful task reports.
- **Filtering**: Filter tasks by project, priority, or status.

## Installation

No dependencies required beyond Python 3.7+.

```bash
git clone https://github.com/YosefSafi/Random.git
cd NexusTask
```

## Usage

### Add a task
```bash
python main.py add "Fix memory leak" --project "Core" --priority "CRITICAL" --due "2026-05-01"
```

### List tasks
```bash
python main.py list
python main.py list --project "Core"
```

### Update status
```bash
python main.py update <ID> DONE
```

### Export report
```bash
python main.py export report.md
```

## Data Storage
Data is stored in `tasks.json` in the root directory. Automated backups are stored in the `backups/` folder.
