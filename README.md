# Oreedoo Kara Fehun Auto Tapper Script

A Python script to automate tapping for the kara felhun in the Oreedoo Application

## Prerequisites

1. ADB (Android Debug Bridge) installed on your computer
2. USB debugging enabled on your Android device
3. Python 3.x installed on your computer

## Setup Instructions

### 1. Install ADB

#### For Mac (using Homebrew):
```
brew install android-platform-tools
```

If you don't have Homebrew:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### For Windows:
Download the Android SDK Platform Tools from Google's developer website and add it to your PATH.

### 2. Enable USB Debugging on your Android Device

1. Go to Settings > About Phone
2. Tap on "Build Number" 7 times to enable Developer Options
3. Go back to Settings > System > Developer Options
4. Enable "USB Debugging"

### 3. Connect your Device

1. Connect your Android device to your computer via USB
2. When prompted on your device, allow USB debugging
3. Verify the connection by running:
```
adb devices
```

You should see your device listed.

## Using the Auto Tapper

The script will automatically tap on the watermelon (or wherever you specify) at a rapid rate.

### Basic Usage

```
python kara-felhun.py
```

This will tap in the center of your screen by default.

### Advanced Options

```
python kara-felhun.py --x 500 --y 800 --interval 0.005 --jitter 15 --duration 3600
```

Parameters:
- `--x` and `--y`: Screen coordinates to tap (default: center of screen)
- `--interval`: Time between taps in seconds (lower = faster, default: 0.01)
- `--jitter`: Random pixel variation to avoid detection (default: 10)
- `--duration`: How long to run in seconds (default: unlimited until Ctrl+C)

### Finding the Exact Watermelon Coordinates

Based on your screenshot, the watermelon appears to be in the middle of the screen, so the default center position should work well. If you need to adjust:

1. Take a screenshot of your game
2. Use an image editing tool to find the pixel coordinates of the watermelon
3. Use those coordinates with the `--x` and `--y` options

## Tips for Maximum Tapping Rate

1. Use a low interval value (e.g., `--interval 0.005`) for faster tapping
2. Keep your phone connected to power during long tapping sessions
3. Make sure your USB connection is stable
4. Close other apps on your phone to reduce lag

## Stopping the Script

Press `Ctrl+C` in the terminal/command prompt to stop the script.

## Troubleshooting

- **No devices detected**: Make sure USB debugging is enabled and your device is properly connected
- **Tapping in wrong location**: Use `--x` and `--y` to specify the exact watermelon coordinates
- **Slow tapping rate**: Try reducing the interval value or closing background apps
- **"ADB not found" error**: Make sure ADB is installed and added to your PATH


## Example Commands:

python3 kara-felhun.py --interval 0.005 --jitter 3 --karaa

python3 kara-felhun.py --interval 0.006 --jitter 5 --karaa

python3 kara-felhun.py --interval 0.006 --jitter 5 --karaa

# Kara-felhun
