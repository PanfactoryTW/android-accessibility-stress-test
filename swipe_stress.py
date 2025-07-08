import subprocess
import time
import threading
import datetime
import os

# === 設定區 ===
KEYCODE = 61
ITERATIONS = 50
SLEEP_SECONDS = 0.2
LOG_DURATION = 15  # 錄多久 logcat（秒）
LOG_TAG = "TalkBack"  # 可改成 Accessibility 或其他
LOG_DIR = "logs"

# === 工具函數 ===
def send_keyevent(keycode: int):
    result = subprocess.run(
        ["adb", "shell", "input", "keyevent", str(keycode)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"Failed to send keyevent {keycode}"

def start_logcat_dump(log_file: str, keyword: str = LOG_TAG, duration: int = LOG_DURATION):
    def dump():
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, log_file), "w") as f:
            p = subprocess.Popen(
                ["adb", "logcat", "-v", "time", "-s", keyword],
                stdout=f,
                stderr=subprocess.STDOUT
            )
            time.sleep(duration)
            p.terminate()
    thread = threading.Thread(target=dump)
    thread.start()
    return thread

# === pytest 主測試 ===
def test_keyevent61_with_log():
    """TalkBack 壓測：keyevent 61 連打 + Log 收集"""

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"talkback_log_{timestamp}.txt"
    log_thread = start_logcat_dump(log_filename)

    for i in range(ITERATIONS):
        send_keyevent(KEYCODE)
        time.sleep(SLEEP_SECONDS)

    log_thread.join()

    assert os.path.exists(os.path.join(LOG_DIR, log_filename)), "Log file was not created."
