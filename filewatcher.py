import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

watch_dir = "/home/kali/bsm/test"
log_file = "/home/kali/bsm/logs/changes.json"

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        self.log_change(event)

    def on_created(self, event):
        if event.is_directory:
            return
        self.log_change(event)

    def on_deleted(self, event):
        if event.is_directory:
            return
        self.log_change(event)

    def log_change(self, event):
        change = {
            'event_type': event.event_type,
            'path': event.src_path,
            'timestamp': time.time()
        }

        try:
            with open(log_file, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(change)

        with open(log_file, 'w') as file:
            json.dump(data, file, indent=4)

if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
