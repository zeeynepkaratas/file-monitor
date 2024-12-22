import pyinotify
import json
import os

# İzlenecek dizin ve log dosyası
watch_directory = "/home/kali/bsm/test"
log_file = "/home/kali/bsm/logs/changes.json"

# Log dosyasının ve dizinin varlığını kontrol et
os.makedirs(os.path.dirname(log_file), exist_ok=True)
if not os.path.exists(log_file):
    with open(log_file, 'w') as file:
        file.write("[]")  # JSON formatında boş bir liste

# JSON formatında loglama fonksiyonu
def log_change(event_type, file_name):
    change = {
        "event": event_type,
        "file": file_name
    }
    with open(log_file, 'a') as file:
        json.dump(change, file)
        file.write("\n")

# Olay işleyici sınıfı
class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        log_change("created", event.pathname)

    def process_IN_DELETE(self, event):
        log_change("deleted", event.pathname)

    def process_IN_MODIFY(self, event):
        log_change("modified", event.pathname)

# Watchdog kurulumu
wm = pyinotify.WatchManager()
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wm.add_watch(watch_directory, pyinotify.ALL_EVENTS)

print(f"Takip ediliyor: {watch_directory}")
notifier.loop()

