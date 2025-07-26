from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CreationHandler(FileSystemEventHandler):
    def on_created(seld, event):
        print(f"File created")
        with open("new_files.txt", "a") as file:
            file.write(event.src_path)
        return super().on_created(event)


def start():
    path = "C:/Users/ilan7/Downloads/"
    observer = Observer()
    handler = CreationHandler()
    observer.schedule(handler, path, recursive=True)
    observer.start()