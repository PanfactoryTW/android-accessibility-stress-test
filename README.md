# Android Accessibility Stress Test

A minimal ADB-based script for stress testing Android accessibility services through long-duration swipe simulations.

## Overview

This project simulates left/right swipe gestures on Android devices using ADB, targeting accessibility frameworks (e.g. screen readers) to verify their stability under continuous interaction.

Originally designed for a personal use case involving long-hour TalkBack stress testing.

## Features

- Runs swipe loops for a configurable duration
- Uses ADB shell commands (no dependencies beyond Python + ADB)
- Simple CLI interface for direction and duration
- Terminal output with basic timestamps

## Usage

```bash
python3 swipe_loop.py --direction left --duration 3600
