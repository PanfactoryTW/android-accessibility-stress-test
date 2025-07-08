import os
import time
import subprocess

def send_keyevent(keycode: int):
    result = subprocess.run(
        ["adb", "shell", "input", "keyevent", str(keycode)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"Failed to send keyevent {keycode}"

def test_talkback_keyevent61_loop():
    """壓測：連續送出 keyevent 61（TAB）並確保無錯誤"""
    num_iterations = 50  # 你可依需求調大
    for i in range(num_iterations):
        send_keyevent(61)  # KEYCODE_TAB
        time.sleep(0.2)
