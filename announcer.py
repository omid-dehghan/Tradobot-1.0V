import datetime
import csv
import os

class Announcer:

    logs = {
        "infos": 0,
        "warns": 0,
        "errors": 0,
        "logs": 0,
        "signals": 0}
    
    announcer_lid = 0
    announcer_num = 0

    def __init__(self, printing:bool = True, save_to_file: bool = False, file_name: str = "logs.csv"):
        self.printing = printing
        self.save_to_file = save_to_file
        self.file_name = file_name
        
        if self.save_to_file and not os.path.exists(self.file_name):
            with open(self.file_name, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["LID", "number","timestamp", "level", "message"])

    def _write(self, id, level: str, message: str):
        self.announcer_num += 1
        self.announcer_lid = f"{id}{self.logs[level.lower() + 's']}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{self.announcer_lid}] [{self.announcer_num}] [{timestamp}] [{level}] {message}"
        
        if self.printing:
            print(formatted)

        if self.save_to_file:
            with open(self.file_name, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([self.announcer_lid, self.announcer_num, timestamp, level, message])

    def info(self, message: str):
        self.logs['infos'] += 1
        self._write(100, "INFO", message)

    def warn(self, message: str):
        self.logs['warns'] += 1
        self._write(200, "WARN", message)

    def error(self, message: str):
        self.logs['errors'] += 1
        self._write(300, "ERROR", message)

    def log(self, message: str):
        self.logs['logs'] += 1
        self._write(400, "LOG", message)

    def signal(self, message: str):
        self.logs['signals'] += 1
        self._write(500, "SIGNAL", message)