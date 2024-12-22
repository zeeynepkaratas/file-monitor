import os
import json
import time
from inotify_simple import INotify, flags

# Değişikliklerin kaydedileceği log dosyasının yolu
log_file = "/home/kali/bsm/logs/changes.json"

# İzlemek istediğiniz dizin
watch_directory = "/home/kali/bsm/test"

# inotify nesnesi oluşturuluyor
inotify = INotify()
watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY
watch_descriptor = inotify.add_watch(watch_directory, watch_flags)

def log_event(action, path):
    event = {
        "action": action,
        "file_path": path,
        "timestamp": time.time()
    }
    write_to_log(event)

def write_to_log(event):
    try:
        with open(log_file, 'r+') as f:
            data = json.load(f)
            data.append(event)
            f.seek(0)
            json.dump(data, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(log_file, 'w') as f:
            json.dump([event], f, indent=4)

def start_watching():
    try:
        while True:
            # Dosya değişikliklerini kontrol et
            for event in inotify.read():
                for flag in flags.from_mask(event.mask):
                    if flag == flags.CREATE:
                        log_event("created", event.name)
                    elif flag == flags.DELETE:
                        log_event("deleted", event.name)
                    elif flag == flags.MODIFY:
                        log_event("modified", event.name)

            time.sleep(1)

    except KeyboardInterrupt:
        print("İzleme durduruldu.")

if __name__ == "__main__":
    start_watching()
