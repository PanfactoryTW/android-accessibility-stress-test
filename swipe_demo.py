import time

KEYCODE = 61
ITERATIONS = 20
SLEEP_SECONDS = 0.1

def send_keyevent_mock(keycode: int, index: int):
    print(f"[DEMO] Simulating keyevent {keycode} ({index + 1}/{ITERATIONS})")
    time.sleep(SLEEP_SECONDS)

def run_demo():
    print("=== Running Accessibility Stress Demo (Mock Mode) ===")
    for i in range(ITERATIONS):
        send_keyevent_mock(KEYCODE, i)

    print("\nNote: This is a dry run demo without device connection or log analysis.")
    print("For full test results, run `swipe_stress.py` with a connected device.")

if __name__ == "__main__":
    run_demo()
