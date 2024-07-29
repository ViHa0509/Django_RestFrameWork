import cv2
import pandas as pd

# screen_width, screen_height = infoObject.current_w, infoObject.current_h

screen_width = 1280
screen_height = 720

# Load the video using OpenCV
video_path = "traffic.mp4"
cap = cv2.VideoCapture(video_path)

# Get the total duration of the video in milliseconds
total_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS) * 1000

timestamps = []
paused = False
subtime = [0]
while cap.isOpened():
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize the frame to fit the screen
        frame = cv2.resize(frame, (screen_width, screen_height))
        
        # Get the current position in the video
        current_pos = cap.get(cv2.CAP_PROP_POS_MSEC)
        
        # Draw the duration bar
        bar_width = int((current_pos / total_duration) * screen_width)
        bar_height = 10
        cv2.rectangle(frame, (0, screen_height - bar_height), (bar_width, screen_height), (0, 255, 0), -1)
        
        # Display the current time
        time_text = f'{int(current_pos)} ms'
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255)
        thickness = 2
        cv2.putText(frame, time_text, (10, screen_height - bar_height - 10), font, font_scale, color, thickness)
        
        cv2.imshow('Video', frame)
    
    # Use cv2.waitKey() to capture key events
    key = cv2.waitKey(1) & 0xFF
    if key == 32:  # Space key has ASCII code 32
        paused = not paused
        if paused:
            # Get the current timestamp in milliseconds
            time = cap.get(cv2.CAP_PROP_POS_MSEC)
            subtime.append(time)
            if len(subtime) == 2:
                timestamps.append(list(subtime))
                subtime.pop(0)

    elif key == ord('q'):
        # Quit the video when 'q' is pressed
        break
cap.release()
cv2.destroyAllWindows()

# Save timestamps to an Excel file
# print(timestamps)
df = pd.DataFrame(timestamps, columns=["Start", "Stop"])
output_file = "video_timestamps.xlsx"
df.to_excel(output_file, index=False)
print(f"Timestamps saved to {output_file}")
  
print("timestamps:", timestamps)
