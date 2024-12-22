import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Log dosyasının yolu
log_file_path = '/home/kali/bsm/logs/changes.json'

# Değişikliklerin kaydedileceği fonksiyon
def log_changes(event):
    change_details = {
        "event_type": event.event_type,
        "src_path": event.src_path,
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    }

    # JSON dosyasını okuma
    try:
        with open(log_file_path, 'r') as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []  # Eğer dosya yoksa veya boşsa, yeni bir liste başlat

    # Yeni değişikliği mevcut kayıtlara ekleme
    logs.append(change_details)

    # Güncellenmiş logları dosyaya yazma
    with open(log_file_path, 'w') as file:
        json.dump(logs, file, indent=4)

# Dosya sistemindeki değişiklikleri izleyen event handler
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        log_changes(event)

    def on_created(self, event):
        log_changes(event)

    def on_deleted(self, event):
        log_changes(event)

# İzlemek istediğimiz dizini belirleyelim
path_to_watch = '/home/kali/bsm/test'

# Observer başlatma
observer = Observer()
observer.schedule(ChangeHandler(), path=path_to_watch, recursive=True)

# Observer'ı çalıştır
observer.start()

try:
    while True:
        time.sleep(1)  # Döngü sürekli çalışacak
except KeyboardInterrupt:
    observer.stop()
observer.join()
