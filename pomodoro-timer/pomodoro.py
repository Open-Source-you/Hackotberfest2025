import os
import time

from plyer import notification


def show_notification(title, message):
    """Show desktop notification."""
    notification.notify(title=title, message=message, timeout=5)


def countdown(minutes, label):
    """Run countdown timer."""
    seconds = minutes * 60
    while seconds:
        mins, secs = divmod(seconds, 60)
        print(f"{label} - {mins:02d}:{secs:02d}", end="\r")
        time.sleep(1)
        seconds -= 1

    # ✅ Saat timer selesai
    print(f"\n✅ {label} done!\n")
    show_notification("Pomodoro Timer", f"{label} finished!")


def pomodoro_session(sessions=4, focus=25, rest=5):
    """Run full Pomodoro sessions."""
    for i in range(1, sessions + 1):
        print(f"🍅 Session {i}/{sessions} started!")
        countdown(focus, "⏱️ Focus")
        if i < sessions:
            countdown(rest, "💤 Break")
    print("🎉 All sessions completed! Great job 👏")
    show_notification("Pomodoro Timer", "🎉 All sessions completed!")


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("=== Pomodoro Timer CLI 🍅 ===")
    sessions = int(input("Enter number of sessions: ") or 4)
    pomodoro_session(sessions)
