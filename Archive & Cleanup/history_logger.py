import json
from pathlib import Path
from datetime import datetime


class HistoryLogger:

    def __init__(self, log_file="SAFE_Data/logs/history.json"):

        self.log_file = Path(log_file)

        self.log_file.parent.mkdir(parents=True, exist_ok=True)

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
