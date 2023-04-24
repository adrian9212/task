import os
import sys
import time
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MonitorFolder(FileSystemEventHandler):
    
    #on_created function will be called when a file is created or copied in the source folder
    def on_created(self, event):
         print(event.src_path, event.event_type)
         logging.info(event.event_type + ' at ' + event.src_path)

    def on_deleted(self, event):
        print(event.src_path, event.event_type)
        logging.info(event.event_type + ' at ' + event.src_path)

if __name__ == "__main__":
    src_path = sys.argv[1]
    repl_path = sys.argv[2]
    sync_interval = sys.argv[3]

    logging.basicConfig(filename='changes.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

    event_handler=MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)")
    starttime = time.time()
    observer.start()
    try:
        while(True):
           time.sleep(3)
           if time.time() >= starttime + float(sync_interval):
               starttime = starttime + float(sync_interval)
               f1 = os.listdir(src_path)
               f2 = os.listdir(repl_path)
               for fname in f2:
                   if fname not in f1:
                       os.remove(os.path.join(repl_path, fname))
               for fname in f1:
                   if fname not in f2:
                       shutil.copy2(os.path.join(src_path,fname), repl_path)
               f1 = os.listdir(src_path)
               f2 = os.listdir(repl_path)
    except KeyboardInterrupt:
            observer.stop()
            observer.join()
