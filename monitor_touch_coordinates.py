import subprocess
import re

def extract_coordinates(log_line):
    match = re.search(r'x=(\d+), y=(\d+)', log_line)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None

def monitor_taps():
    # Start the adb logcat command
    process = subprocess.Popen(["adb", "logcat"], stdout=subprocess.PIPE, text=True)

    # Read logcat output line by line
    while True:
        line = process.stdout.readline().strip()
        if "MotionEvent" in line:
            coords = extract_coordinates(line)
            if coords:
                print(f"Tapped at: x={coords[0]}, y={coords[1]}")

if __name__ == "__main__":
    monitor_taps()
