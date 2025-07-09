import subprocess
import time
import threading
import datetime
import os
from jinja2 import Template  # pip install jinja2

# === Configuration ===
KEYCODE = 61  # Simulate TAB key, commonly used for TalkBack focus
ITERATIONS = 50  # Number of repeated keyevents
SLEEP_SECONDS = 0.2  # Interval between keyevents
LOG_DURATION = 15  # How long to record logcat (in seconds)
LOG_TAG = "TalkBack"  # Can be replaced with "Accessibility"
LOG_DIR = "logs"
REPORT_DIR = "reports"
EXPECTED_KEYWORDS = ["Accessibility", "TalkBack", "focus"]

# === Utility Functions ===
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
        with open(os.path.join(LOG_DIR, log_file), "w", encoding="utf-8", errors="ignore") as f:
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

def generate_markdown_report(timestamp, iterations, result, logfile):
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_file = os.path.join(REPORT_DIR, f"report_{timestamp}.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# TalkBack Stress Test Report\n\n")
        f.write(f"- Test Time: {timestamp}\n")
        f.write(f"- Iterations: {iterations}\n")
        f.write(f"- Keyword Check: {'PASSED' if result else 'FAILED'}\n")
        f.write(f"- Log File: `{logfile}`\n")
    return report_file

def generate_html_report(timestamp, iterations, result, logfile):
    os.makedirs(REPORT_DIR, exist_ok=True)
    HTML_TEMPLATE = """
    <html>
    <head><title>TalkBack Stress Test Report</title></head>
    <body>
        <h1>TalkBack Stress Test Report</h1>
        <ul>
            <li><strong>Test Time:</strong> {{ timestamp }}</li>
            <li><strong>Iterations:</strong> {{ iterations }}</li>
            <li><strong>Keyword Check:</strong> {{ result }}</li>
            <li><strong>Log File:</strong> {{ logfile }}</li>
        </ul>
    </body>
    </html>
    """
    html_report = Template(HTML_TEMPLATE).render(
        timestamp=timestamp,
        iterations=iterations,
        result="PASSED" if result else "FAILED",
        logfile=logfile
    )
    html_path = os.path.join(REPORT_DIR, f"report_{timestamp}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_report)
    return html_path

# === Main Test Logic ===
def run_swipe_stress_test():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"talkback_log_{timestamp}.txt"
    log_thread = start_logcat_dump(log_filename)

    for i in range(ITERATIONS):
        send_keyevent(KEYCODE)
        time.sleep(SLEEP_SECONDS)

    log_thread.join()

    full_log_path = os.path.join(LOG_DIR, log_filename)
    assert os.path.exists(full_log_path), "Log file was not created."

    with open(full_log_path, "r", encoding="utf-8", errors="ignore") as f:
        log_content = f.read()

    found = any(keyword in log_content for keyword in EXPECTED_KEYWORDS)

    # Generate reports
    md_report = generate_markdown_report(timestamp, ITERATIONS, found, log_filename)
    html_report = generate_html_report(timestamp, ITERATIONS, found, log_filename)

    print("\n=== Test Completed ===")
    print(f"Log file: {full_log_path}")
    print(f"Markdown report: {md_report}")
    print(f"HTML report: {html_report}")
    print(f"Keyword check: {'✅ PASSED' if found else '❌ FAILED'}")

# === Entry Point ===
if __name__ == "__main__":
    run_swipe_stress_test()
