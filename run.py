import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.run_script()

    def run_script(self):
        if self.process:
            self.process.kill()
        print("🚀 Running script...\n")
        self.process = subprocess.Popen(self.command, shell=True)

    def on_modified(self, event):
        if event.src_path.endswith("main.py"):
            print(f"📁 Detected change in: {event.src_path}")
            self.run_script()

if __name__ == "__main__":
    path = "."
    event_handler = ReloadHandler("python3 main.py")
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print("🧿 Watching for changes in main.py...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
