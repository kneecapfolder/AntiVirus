from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import sleep
import threading

# Add all new files in the downloads folder to the new_files text file
class CreationHandler(FileSystemEventHandler):
    def on_created(seld, event):
        if not event.is_directory:
            print("File created: " + event.src_path)
            with open("new_files.txt", "a") as file:
                file.write(event.src_path + "\n")
        return super().on_created(event)


# Start the watchdog observer
def start():
    path = "C:/Users/ilan7/Downloads/"
    observer = Observer()
    handler = CreationHandler()
    observer.schedule(handler, path, recursive=True)
    observer.start()

# Get all the paths from the new_files.txt file
def get():
    paths = []
    with open("new_files.txt", "r") as file:
        paths = file.read().split("\n")

    # Clear the new files list
    with open("new_files.txt", "w") as file:
        file.close()
    
    return paths


scan_wait_thread = False
exit_event = threading.Event()

# Start the thread that runs the background scan
def start_thread(wait, scan_files):
    global scan_wait_thread
    
    if scan_wait_thread and scan_wait_thread.is_alive():
        exit_event.set()
        scan_wait_thread.join()

    scan_wait_thread = threading.Thread(target=scan, args=(wait, scan_files))
    scan_wait_thread.start()

# Scan the paths in the new_files.txt file
def scan(wait, scan_files):
    print("thread started")
    paths = [x for x in get() if x != ""]
    
    if (len(paths) > 0):
        scan_files(paths)

    time_left = wait

    while(time_left > 0):
        sleep(1)
        time_left -= 1
        if exit_event.is_set():
            print("auto scanning thread stopped")
            exit_event.clear()
            return
        
    print("thread finished")
    scan(wait, scan_files)