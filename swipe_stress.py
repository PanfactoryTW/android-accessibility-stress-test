import subprocess
import time
import threading
import datetime
import os
from jinja2 import Template  # pip install jinja2

# === Configuration ===
KEYCODE = 61  # Simulate TAB key, commonly used for TalkBack focus
ITERATIONS = 50
SLEEP_SECONDS = 0.2
LOG_DURATION = 15
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

def start_logcat_dump(log_file: str, duration: int = LOG_DURATION):
    def dump():
        os.makedirs(LOG_DIR, exist_ok=True)
        subprocess.run(["adb", "logcat", "-c"])  # 清除舊 log

        with open(os.path.join(LOG_DIR, log_file), "w", encoding="utf-8", errors="ignore") as f:
            p = subprocess.Popen(
                ["adb", "logcat", "-v", "time"],  # 不篩 tag，全抓
                stdout=f,
                stderr=subprocess.STDOUT
            )
            time.sleep(duration)
            p.terminate()
    thread = threading.Thread(target=dump)
    thread.start()
    return thread

def generate_markdown_report(timestamp, iterations, result, logfile, matched_lines):
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_file = os.path.join(REPORT_DIR, f"report_{timestamp}.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# TalkBack Stress Test Report\n\n")
        f.write(f"- Test Time: {timestamp}\n")
        f.write(f"- Iterations: {iterations}\n")
        f.write(f"- Keyword Check: {'PASSED' if result else 'FAILED'}\n")
        f.write(f"- Log File: `{logfile}`\n")
        f.write(f"\n## Matched Log Lines (Top 10)\n\n")
        for line in matched_lines[:10]:
            f.write(f"- {line}\n")
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

    for _ in range(ITERATIONS):
        send_keyevent(KEYCODE)
        time.sleep(SLEEP_SECONDS)

    log_thread.join()

    full_log_path = os.path.join(LOG_DIR, log_filename)
    assert os.path.exists(full_log_path), "Log file was not created."

    with open(full_log_path, "r", encoding="utf-8", errors="ignore") as f:
        log_content = f.read()

    matched_lines = [line for line in log_content.splitlines()
                     if any(keyword in line for keyword in EXPECTED_KEYWORDS)]

    found = len(matched_lines) > 0

    md_report = generate_markdown_report(timestamp, ITERATIONS, found, log_filename, matched_lines)
    html_report = generate_html_report(timestamp, ITERATIONS, found, log_filename)

    print("\n=== Test Completed ===")
    print(f"Log file: {full_log_path}")
    print(f"Markdown report: {md_report}")
    print(f"HTML report: {html_report}")
    print(f"Keyword check: {'✅ PASSED' if found else '❌ FAILED'}")
    print(f"Matched log lines: {len(matched_lines)}")

# === Entry Point ===
if __name__ == "__main__":
    run_swipe_stress_test()
