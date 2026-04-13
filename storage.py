import json
import os
import shutil
from datetime import datetime
from typing import List
from models import Task

DATA_FILE = "tasks.json"
BACKUP_DIR = "backups"

class Storage:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        if not os.path.exists(self.data_file):
            self.save_tasks([])

    def save_tasks(self, tasks: List[Task]):
        data = [task.to_dict() for task in tasks]
        # Create backup before saving
        if os.path.exists(self.data_file):
            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2(self.data_file, os.path.join(BACKUP_DIR, f"tasks_{timestamp}.json.bak"))
            
            # Keep only last 5 backups
            backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith(".bak")])
            if len(backups) > 5:
                for b in backups[:-5]:
                    os.remove(os.path.join(BACKUP_DIR, b))

        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(d) for d in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
