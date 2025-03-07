#!/usr/bin/env python3
"""
Watermelon Auto Tapper - Android Game Automation Script
This script uses ADB to automate tapping on a specific location on an Android device.
"""

import subprocess
import time
import random
import argparse
import os
import signal
import sys
import math
from datetime import datetime, timedelta

class AutoTapper:
    def __init__(self, x=None, y=None, tap_interval=0.008, jitter=10, multi_tap=True, total_taps=None):
        """
        Initialize the auto tapper.
        
        Args:
            x (int): X coordinate for tapping (defaults to middle of screen if None)
            y (int): Y coordinate for tapping (defaults to middle of screen if None)
            tap_interval (float): Time between taps in seconds (lower = faster)
            jitter (int): Random pixel variation to avoid detection
            multi_tap (bool): Whether to use optimized multi-location tapping
            total_taps (int): Total number of taps needed to reach the goal
        """
        self.x = x
        self.y = y
        self.tap_interval = tap_interval
        self.jitter = jitter
        self.multi_tap = multi_tap
        self.total_taps = total_taps
        self.running = False
        self.tap_count = 0
        self.start_time = None
        self.tap_locations = []
        self.current_location_index = 0
        self.screen_width = 0
        self.screen_height = 0
        
        # Get device resolution if coordinates not provided
        if x is None or y is None:
            self.get_screen_resolution()
    
    def get_screen_resolution(self):
        """Get the device screen resolution and set default tap position to center."""
        try:
            result = subprocess.check_output(
                ["adb", "shell", "wm", "size"], 
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Parse the resolution
            resolution = result.strip().split(": ")[1]
            width, height = map(int, resolution.split("x"))
            self.screen_width = width
            self.screen_height = height
            
            # Default to center if x or y not provided
            if self.x is None:
                self.x = width // 2
            if self.y is None:
                self.y = height // 2
            
                # Generate optimized tap positions if multi-tap is enabled
            if self.multi_tap:
                self.generate_tap_locations()
                
            # Override center point if we have explicit coordinates
            if self.x is not None and self.y is not None:
                # If we're in multi-tap mode, adjust all tap locations around the specified point
                if self.multi_tap and self.tap_locations:
                    base_x, base_y = self.x, self.y
                    radius = int(self.screen_height * 0.20)
                    
                    # Regenerate tap locations around the specified point
                    self.tap_locations = [
                        (base_x, base_y, 0.008),  # Center
                        (base_x, base_y - radius, 0.009),  # Top
                        (base_x + radius, base_y, 0.008),  # Right
                        (base_x, base_y + radius, 0.009),  # Bottom
                        (base_x - radius, base_y, 0.008),  # Left
                        (base_x + int(radius * 0.7), base_y + int(radius * 0.7), 0.007),  # Bottom-Right
                        (base_x + int(radius * 0.7), base_y - int(radius * 0.7), 0.007),  # Top-Right
                        (base_x - int(radius * 0.7), base_y + int(radius * 0.7), 0.007),  # Bottom-Left
                        (base_x - int(radius * 0.7), base_y - int(radius * 0.7), 0.007),  # Top-Left
                    ]
                
            print(f"Screen resolution: {width}x{height}")
            if not self.multi_tap:
                print(f"Tapping position: ({self.x}, {self.y})")
            else:
                print(f"Using optimized multi-location tapping with {len(self.tap_locations)} positions")
            
        except subprocess.CalledProcessError as e:
            print(f"Error getting screen resolution: {e}")
            print("Please connect your device via ADB first.")
            sys.exit(1)
    
    def add_jitter(self, coord):
        """Add random jitter to coordinates to avoid detection patterns."""
        return coord + random.randint(-self.jitter, self.jitter)
    
    def generate_tap_locations(self):
        """Generate optimized tap locations using a comprehensive pattern to cover the watermelon."""
        # Based on the screenshot, the watermelon is in the center-bottom portion
        # Calibrated coordinates for the game
        center_x = self.screen_width // 2
        # The watermelon appears to be about 60% down the screen based on the image
        center_y = int(self.screen_height * 0.6)
        
        # Calculate radius - the watermelon size is approximately 20% of screen height
        radius = int(self.screen_height * 0.20)
        
        # Generate positions in different parts of the watermelon using multiple patterns
        self.tap_locations = []
        
        # Center point (highest tap rate)
        self.tap_locations.append((center_x, center_y, 0.0055))  # Fastest in center
        
        # Inner ring - 8 points at 40% radius (fast tapping)
        inner_radius = radius * 0.4
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = center_x + int(inner_radius * math.cos(rad))
            y = center_y + int(inner_radius * math.sin(rad))
            self.tap_locations.append((x, y, 0.006))  # Fast inner ring
        
        # Middle ring - 12 points at 70% radius (medium speed)
        middle_radius = radius * 0.7
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x = center_x + int(middle_radius * math.cos(rad))
            y = center_y + int(middle_radius * math.sin(rad))
            self.tap_locations.append((x, y, 0.007))  # Medium speed middle ring
        
        # Outer ring - 16 points at 100% radius (slower but comprehensive coverage)
        for angle in range(0, 360, 22):
            rad = math.radians(angle)
            x = center_x + int(radius * math.cos(rad))
            y = center_y + int(radius * math.sin(rad))
            self.tap_locations.append((x, y, 0.008))  # Slower outer edge
        
        # Add 4 strategic points just inside the perimeter (85% radius in cardinal directions)
        # These help transition between outer and middle rings
        strategic_radius = radius * 0.85
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            x = center_x + int(strategic_radius * math.cos(rad))
            y = center_y + int(strategic_radius * math.sin(rad))
            self.tap_locations.append((x, y, 0.0065))  # Slightly faster strategic points
        
        # Add 4 random points within the watermelon for unpredictability
        for _ in range(4):
            # Random distance from center (between 10% and 90% of radius)
            random_radius = radius * (0.1 + 0.8 * random.random())
            # Random angle
            random_angle = random.uniform(0, 2 * math.pi)
            x = center_x + int(random_radius * math.cos(random_angle))
            y = center_y + int(random_radius * math.sin(random_angle))
            self.tap_locations.append((x, y, 0.007))  # Medium speed for random points
            
        # Shuffle the list to prevent predictable patterns
        random.shuffle(self.tap_locations)

    def get_next_tap_location(self):
        """Get the next tap location in the sequence."""
        if not self.multi_tap or not self.tap_locations:
            return self.x, self.y, self.tap_interval
        
        # Cycle through optimized locations
        location = self.tap_locations[self.current_location_index]
        self.current_location_index = (self.current_location_index + 1) % len(self.tap_locations)
        
        return location[0], location[1], location[2]
        
    def send_tap(self):
        """Send a single tap command to the device."""
        # Get next tap location and interval
        base_x, base_y, tap_rate = self.get_next_tap_location()
        
        # Add jitter to coordinates
        x = self.add_jitter(base_x)
        y = self.add_jitter(base_y)
        
        try:
            # Use shell tap command with more efficient parameters
            subprocess.run(
                ["adb", "shell", "input", "tap", str(x), str(y)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.tap_count += 1
            
            # Reduce stat display frequency to improve performance
            if self.tap_count % 200 == 0:
                self.display_stats()
                
        except subprocess.CalledProcessError:
            print("Error sending tap command.")
            
    def display_stats(self):
        """Display tapping statistics including estimated time to completion."""
        elapsed = time.time() - self.start_time
        taps_per_second = self.tap_count / elapsed if elapsed > 0 else 0
        
        # Print basic stats
        stats = f"Taps: {self.tap_count}, Rate: {taps_per_second:.2f} taps/sec"
        
        # Add time estimation if total_taps is provided
        if self.total_taps:
            remaining_taps = max(0, self.total_taps - self.tap_count)
            if taps_per_second > 0:
                seconds_remaining = remaining_taps / taps_per_second
                completion_time = datetime.now() + timedelta(seconds=seconds_remaining)
                
                # Format time remaining
                if seconds_remaining > 86400:  # More than a day
                    days = seconds_remaining // 86400
                    hours = (seconds_remaining % 86400) // 3600
                    time_str = f"{int(days)}d {int(hours)}h"
                elif seconds_remaining > 3600:  # More than an hour
                    hours = seconds_remaining // 3600
                    minutes = (seconds_remaining % 3600) // 60
                    time_str = f"{int(hours)}h {int(minutes)}m"
                else:  # Less than an hour
                    minutes = seconds_remaining // 60
                    seconds = seconds_remaining % 60
                    time_str = f"{int(minutes)}m {int(seconds)}s"
                
                stats += f", Remaining: {remaining_taps} taps"
                stats += f", Est. completion: {time_str} ({completion_time.strftime('%H:%M:%S')})"
        
        print(stats)
    
    def check_adb_connection(self):
        """Check if a device is connected via ADB."""
        try:
            result = subprocess.check_output(
                ["adb", "devices"], 
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            if "device" not in result or result.count("\n") <= 1:
                print("No devices connected via ADB. Please connect your device.")
                return False
            return True
            
        except subprocess.CalledProcessError:
            print("ADB not found. Please install ADB and add it to your PATH.")
            return False
    
    def start(self, duration=None):
        """Start the auto tapping process."""
        if not self.check_adb_connection():
            return
        
        self.running = True
        self.tap_count = 0
        self.start_time = time.time()
        end_time = None if duration is None else time.time() + duration
        
        if self.multi_tap:
            print(f"Starting optimized multi-location auto-tapper")
            print(f"Using {len(self.tap_locations)} strategic tap locations with variable rates")
        else:
            print(f"Starting auto-tapper at position ({self.x}, {self.y})")
            print(f"Tap interval: {self.tap_interval} seconds")
            
        if self.total_taps:
            print(f"Total taps needed: {self.total_taps}")
            
        print("Press Ctrl+C to stop...")
        
        try:
            while self.running:
                # Get next tap location and interval for this tap
                if self.multi_tap:
                    x, y, current_interval = self.get_next_tap_location()
                else:
                    current_interval = self.tap_interval
                
                # Send the tap
                self.send_tap()
                
                # Sleep for the current location's interval
                time.sleep(current_interval)
                
                # Check if we've reached the total taps (if specified)
                if self.total_taps and self.tap_count >= self.total_taps:
                    print(f"Successfully completed {self.total_taps} taps. Goal reached!")
                    break
                
                # Check if duration has elapsed
                if end_time and time.time() >= end_time:
                    print(f"Duration of {duration} seconds reached. Stopping.")
                    break
                    
        except KeyboardInterrupt:
            pass
        finally:
            elapsed = time.time() - self.start_time
            taps_per_second = self.tap_count / elapsed if elapsed > 0 else 0
            
            print("\nStopping auto-tapper...")
            print(f"Session summary:")
            print(f"Total taps: {self.tap_count}")
            if self.total_taps:
                completion_percentage = (self.tap_count / self.total_taps) * 100
                print(f"Progress: {completion_percentage:.1f}% complete")
            print(f"Time elapsed: {elapsed:.2f} seconds")
            print(f"Average rate: {taps_per_second:.2f} taps per second")
    
    def stop(self):
        """Stop the auto tapping process."""
        self.running = False

def main():
    parser = argparse.ArgumentParser(description="Auto Tapper for Android Games")
    parser.add_argument("--x", type=int, help="X coordinate for tapping (default: calibrated for Karaa Felhun)")
    parser.add_argument("--y", type=int, help="Y coordinate for tapping (default: calibrated for Karaa Felhun)")
    parser.add_argument("--interval", type=float, default=0.008, help="Time between taps in seconds (default: 0.008)")
    parser.add_argument("--jitter", type=int, default=8, help="Random pixel variation (default: 8)")
    parser.add_argument("--duration", type=int, help="Duration to run in seconds (default: unlimited)")
    parser.add_argument("--total-taps", type=int, help="Total taps needed to complete goal")
    parser.add_argument("--single-point", action="store_true", help="Use single point tapping instead of optimized multi-location tapping")
    parser.add_argument("--karaa", action="store_true", default=True, help="Use optimal settings for Karaa Felhun game (default: True)")
    
    args = parser.parse_args()
    
    # For Karaa Felhun game, use these calibrated coordinates if not overridden by user
    x_coord = args.x
    y_coord = args.y
    
    if args.karaa and not args.x and not args.y:
        # Get screen resolution to calculate optimal coordinates
        try:
            result = subprocess.check_output(
                ["adb", "shell", "wm", "size"], 
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Parse the resolution
            resolution = result.strip().split(": ")[1]
            width, height = map(int, resolution.split("x"))
            
            # Set optimal coordinates for the watermelon in Karaa Felhun
            x_coord = width // 2
            y_coord = int(height * 0.6)  # Watermelon is at approximately 60% from the top
            print(f"Using calibrated coordinates for Karaa Felhun: ({x_coord}, {y_coord})")
            
        except subprocess.CalledProcessError as e:
            print(f"Error getting screen resolution: {e}")
            print("Using default coordinates.")
    
    tapper = AutoTapper(
        x=x_coord, 
        y=y_coord, 
        tap_interval=args.interval,
        jitter=args.jitter,
        multi_tap=not args.single_point,
        total_taps=args.total_taps
    )
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        tapper.stop()
    
    signal.signal(signal.SIGINT, signal_handler)
    tapper.start(duration=args.duration)

if __name__ == "__main__":
    main()
