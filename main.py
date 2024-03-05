import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, ImageSequenceClip
import random

def process_video(video_path, start_time:float, end_time:float):
    # Process the video from start_time to end_time
    clip = VideoFileClip(video_path)

    startFrame = int(start_time*clip.fps)
    endFrame = int(end_time*clip.fps)
    allFrames = [f for f in clip.iter_frames()]
    resultFrames = allFrames[:startFrame]

    walkFrames = allFrames[startFrame:endFrame]

    n = 0
    maxIter = 1000
    fwdProb = 0.5
    for _ in range(maxIter):
        if random.random() < fwdProb:
            n += 1
        else:
            n -= 1

        if n < 0:
            n = 0
        if n >= len(walkFrames):
            break

        resultFrames.append(walkFrames[n])

    resultFrames += allFrames[endFrame:]

    processed_clip = ImageSequenceClip(resultFrames, fps=clip.fps)
    output_path = "processed_video.mp4"
    processed_clip.write_videofile(output_path, codec='libx264', fps=clip.fps)

    # Notify the user that processing is complete
    result_label.config(text="Video processing complete!")

def select_video():
    # Open file dialog to select a video file
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    if video_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, video_path)


def process_button_clicked():
    # Get video path, start time, and end time
    video_path = video_entry.get()
    start_time = float(start_time_entry.get())
    end_time = float(end_time_entry.get())

    # Process the video
    process_video(video_path, start_time, end_time)


# Create the main application window
root = tk.Tk()
root.title("Video Processing")

# Video selection
video_label = tk.Label(root, text="Select Video:")
video_label.grid(row=0, column=0)

video_entry = tk.Entry(root, width=50)
video_entry.grid(row=0, column=1)

select_button = tk.Button(root, text="Browse", command=select_video)
select_button.grid(row=0, column=2)

# Start time entry
start_time_label = tk.Label(root, text="Start Time (seconds):")
start_time_label.grid(row=1, column=0)

start_time_entry = tk.Entry(root, width=20)
start_time_entry.grid(row=1, column=1)

# End time entry
end_time_label = tk.Label(root, text="End Time (seconds):")
end_time_label.grid(row=2, column=0)

end_time_entry = tk.Entry(root, width=20)
end_time_entry.grid(row=2, column=1)

# Process button
process_button = tk.Button(root, text="Process Video", command=process_button_clicked)
process_button.grid(row=3, column=1)

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=1)

root.mainloop()
