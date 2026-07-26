import json
from pathlib import Path
from datetime import datetime


class HistoryLogger:

    def __init__(self):

        self.log_file = Path("logs/history.json")

        self.log_file.parent.mkdir(exist_ok=True)

        if not self.log_file.exists():

            with open(self.log_file, "w") as f:

                json.dump([], f)

    def log(self, action, filename):

        with open(self.log_file, "r") as f:

            history = json.load(f)

        history.append({

            "date": datetime.now().isoformat(),

            "action": action,

            "file": filename

        })

        with open(self.log_file, "w") as f:

            json.dump(history, f, indent=4)
