import time
import os
import sys
from datetime import datetime
from plyer import notification
import json

class PomodoroTimer:
    def __init__(self):
        self.config_file = "pomodoro_config.json"
        self.log_file = "pomodoro_log.txt"
        self.load_config()
        self.total_focus_time = 0
        self.completed_sessions = 0
        
    def load_config(self):
        """Load or create configuration."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except:
            config = {
                "focus": 25,
                "short_break": 5,
                "long_break": 15,
                "sessions_before_long": 4,
                "sound_enabled": True
            }
            self.save_config(config)
        
        self.focus = config["focus"]
        self.short_break = config["short_break"]
        self.long_break = config["long_break"]
        self.sessions_before_long = config["sessions_before_long"]
        self.sound_enabled = config["sound_enabled"]
    
    def save_config(self, config):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def clear_screen(self):
        """Clear terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")
    
    def show_notification(self, title, message):
        """Show desktop notification and play sound."""
        notification.notify(
            title=title,
            message=message,
            app_icon=None,
            timeout=5
        )
        if self.sound_enabled:
            print('\a')  # System beep
    
    def log_session(self, session_type, duration):
        """Log completed sessions."""
        with open(self.log_file, 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {session_type}: {duration} min\n")
    
    def display_progress(self, total_seconds, current_seconds, label, session_num=None):
        """Display timer with progress bar."""
        mins, secs = divmod(current_seconds, 60)
        progress = (total_seconds - current_seconds) / total_seconds
        bar_length = 30
        filled = int(bar_length * progress)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        # Build display
        display = f"\r{label} "
        if session_num:
            display += f"[Session {session_num}] "
        display += f"{mins:02d}:{secs:02d} [{bar}] {int(progress*100)}%"
        
        print(display, end="", flush=True)
    
    def countdown(self, minutes, label, session_num=None):
        """Enhanced countdown timer with progress bar."""
        total_seconds = minutes * 60
        seconds = total_seconds
        
        print(f"\n🚀 Starting: {label} ({minutes} minutes)")
        print("-" * 50)
        
        try:
            while seconds:
                self.display_progress(total_seconds, seconds, label, session_num)
                time.sleep(1)
                seconds -= 1
            
            # Completion
            print(f"\n✅ {label} completed!")
            self.show_notification("Pomodoro Timer", f"{label} finished! ⏰")
            self.log_session(label, minutes)
            
            if "Focus" in label:
                self.total_focus_time += minutes
                self.completed_sessions += 1
                
        except KeyboardInterrupt:
            print("\n\n⏸️  Timer paused. Press Enter to resume or 'q' to quit...")
            choice = input().lower()
            if choice == 'q':
                self.show_stats()
                sys.exit(0)
            else:
                # Resume countdown
                self.countdown(seconds // 60, label + " (Resumed)", session_num)
    
    def run_session(self):
        """Run a complete Pomodoro cycle."""
        self.clear_screen()
        self.display_header()
        
        session = 1
        while True:
            # Focus session
            self.countdown(self.focus, "🎯 Focus Time", session)
            
            # Determine break type
            if session % self.sessions_before_long == 0:
                self.countdown(self.long_break, "☕ Long Break")
                print("\n" + "="*50)
                print(f"🎊 Cycle completed! {session} sessions done!")
                print("="*50)
            else:
                self.countdown(self.short_break, "☕ Short Break")
            
            # Ask to continue
            print(f"\n📊 Progress: {session} sessions | {self.total_focus_time} min focused")
            choice = input("\n▶️  Continue? (Enter/n/stats): ").lower()
            
            if choice == 'n':
                break
            elif choice == 'stats':
                self.show_stats()
                input("\nPress Enter to continue...")
            
            session += 1
            self.clear_screen()
            self.display_header()
    
    def display_header(self):
        """Display application header."""
        print("="*50)
        print("🍅 POMODORO TIMER PRO 🍅".center(50))
        print("="*50)
        print(f"Focus: {self.focus}min | Break: {self.short_break}min | Long: {self.long_break}min")
        print("="*50)
    
    def show_stats(self):
        """Display session statistics."""
        print("\n" + "="*50)
        print("📈 SESSION STATISTICS")
        print("="*50)
        print(f"✅ Completed Sessions: {self.completed_sessions}")
        print(f"⏱️  Total Focus Time: {self.total_focus_time} minutes")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Show today's log
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                today = datetime.now().strftime('%Y-%m-%d')
                today_sessions = [l for l in lines if today in l]
                if today_sessions:
                    print(f"\n📝 Today's Sessions ({len(today_sessions)}):")
                    for session in today_sessions[-5:]:
                        print(f"   {session.strip()}")
        except:
            pass
        print("="*50)
    
    def settings_menu(self):
        """Configure timer settings."""
        self.clear_screen()
        print("⚙️  SETTINGS")
        print("-"*50)
        print(f"1. Focus Duration: {self.focus} min")
        print(f"2. Short Break: {self.short_break} min")
        print(f"3. Long Break: {self.long_break} min")
        print(f"4. Sessions before long break: {self.sessions_before_long}")
        print(f"5. Sound: {'ON' if self.sound_enabled else 'OFF'}")
        print("0. Back to main menu")
        
        choice = input("\nSelect option to change: ")
        
        if choice == '1':
            self.focus = int(input("New focus duration (min): ") or self.focus)
        elif choice == '2':
            self.short_break = int(input("New short break (min): ") or self.short_break)
        elif choice == '3':
            self.long_break = int(input("New long break (min): ") or self.long_break)
        elif choice == '4':
            self.sessions_before_long = int(input("Sessions before long break: ") or self.sessions_before_long)
        elif choice == '5':
            self.sound_enabled = not self.sound_enabled
        
        if choice in ['1', '2', '3', '4', '5']:
            self.save_config({
                "focus": self.focus,
                "short_break": self.short_break,
                "long_break": self.long_break,
                "sessions_before_long": self.sessions_before_long,
                "sound_enabled": self.sound_enabled
            })
            print("✅ Settings saved!")
            time.sleep(1)
    
    def main_menu(self):
        """Display main menu."""
        while True:
            self.clear_screen()
            self.display_header()
            
            print("\n📋 MAIN MENU:")
            print("1. 🚀 Start Pomodoro Session")
            print("2. ⏱️  Quick Timer (custom duration)")
            print("3. ⚙️  Settings")
            print("4. 📊 View Statistics")
            print("5. 📖 How to Use")
            print("0. 🚪 Exit")
            
            choice = input("\nSelect option: ")
            
            if choice == '1':
                self.run_session()
            elif choice == '2':
                mins = int(input("\nEnter duration (minutes): ") or 5)
                label = input("Label (optional): ") or "Custom Timer"
                self.countdown(mins, f"⏰ {label}")
                input("\nPress Enter to continue...")
            elif choice == '3':
                self.settings_menu()
            elif choice == '4':
                self.show_stats()
                input("\nPress Enter to continue...")
            elif choice == '5':
                self.show_help()
                input("\nPress Enter to continue...")
            elif choice == '0':
                self.show_stats()
                print("\n👋 Thanks for using Pomodoro Timer! Stay productive!")
                break
            else:
                print("Invalid option!")
                time.sleep(1)
    
    def show_help(self):
        """Display help information."""
        print("\n" + "="*50)
        print("📖 HOW TO USE POMODORO TIMER")
        print("="*50)
        print("""
The Pomodoro Technique:
1. Work focused for 25 minutes (1 Pomodoro)
2. Take a 5-minute short break
3. After 4 Pomodoros, take a 15-minute long break

Features:
• Customizable timer durations
• Progress tracking with visual progress bar
• Desktop notifications
• Session logging
• Pause/Resume functionality (Ctrl+C)
• Statistics tracking

Tips for Success:
✓ Eliminate distractions during focus time
✓ Actually rest during breaks (no work!)
✓ Stay hydrated
✓ Adjust timings to suit your workflow
        """)
        print("="*50)

def main():
    """Main entry point."""
    try:
        timer = PomodoroTimer()
        timer.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Stay productive!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please install required packages: pip install plyer")

if __name__ == "__main__":
    main()
