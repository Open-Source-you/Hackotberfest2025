import time
import winsound  # This is specific to Windows for sound; replace with another method for different OS.


def set_alarm(alarm_time):
    while True:
        current_time = time.strftime("%H:%M:%S")
        print(f"Current time: {current_time}", end="\r")
        if current_time == alarm_time:
            print("\nTime to wake up!");
            # Play a sound (only works on Windows)
            winsound.Beep(1000, 1000)  # Frequency (Hz), Duration (ms)
            break
        time.sleep(1)  # Check every second


def main():
    print("Welcome to the Alarm Clock!")
    alarm_time = input("Set the alarm time (HH:MM:SS, 24-hour format): ")

    # Validate input time format
    try:
        time.strptime(alarm_time, "%H:%M:%S")
    except ValueError:
        print("Incorrect time format. Please enter in HH:MM:SS format.")
        return

    print(f"Alarm set for {alarm_time}.")
    set_alarm(alarm_time)


if __name__ == "__main__":
    main()
