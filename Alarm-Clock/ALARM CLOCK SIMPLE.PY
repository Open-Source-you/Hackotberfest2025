import time
import datetime
import winsound  # For Windows sound playback; on Linux/Mac, use other libraries like playsound

# Function to play alarm sound
def play_alarm():
    frequency = 2500  # Set Frequency in Hertz
    duration = 1000   # Set Duration in milliseconds
    winsound.Beep(frequency, duration)

# Function to set the alarm
def set_alarm(alarm_time):
    print(f"Alarm is set for {alarm_time}")
    while True:
        # Get current time in HH:MM format
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            print("Wake up! Alarm ringing!")
            play_alarm()
            break
        time.sleep(10)  # Sleep 10 seconds before checking again

# Example usage
if __name__ == "__main__":
    # User sets alarm time in HH:MM 24-hour format
    alarm_time_input = input("Enter alarm time (HH:MM): ")
    set_alarm(alarm_time_input)
