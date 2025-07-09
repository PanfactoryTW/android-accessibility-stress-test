# Android Accessibility Stress Test

A Python script for stress testing Android accessibility services, especially TalkBack, using repeated ADB key events and log analysis.

## Overview

This tool simulates accessibility interactions by repeatedly sending `KEYCODE_TAB` events via ADB. It captures the full logcat output during the test, searches for relevant keywords (like "TalkBack", "Accessibility", "focus"), and generates both Markdown and HTML reports.

Originally built for long-session stress testing of accessibility frameworks under continuous input.

## Features

- Repeated `adb shell input keyevent` to simulate focus movement
- Captures complete logcat output without filtering by tag
- Keyword-based log analysis (configurable)
- Generates Markdown and HTML reports summarizing test results
- Automatically clears the previous logcat buffer before each run
- Minimal dependencies: only Python, ADB, and jinja2

## Requirements

- Python 3.6 or higher
- ADB installed and accessible from your PATH
- `pip install jinja2`

## Usage

Run the script directly:

```bash
python3 swipe_stress.py
