import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import threading
import shlex

rtsp_url = "rtsp://10.30.30.11/ProfileToken_1_1"

cap = cv2.VideoCapture(rtsp_url)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f'{width}x{height} {fps}fps')
cap.release()
ffmpeg_cmd = shlex.split(f'ffmpeg -nostdin -probesize 32 -flags low_delay -fflags nobuffer -rtsp_transport tcp -i {rtsp_url} -vf fps=25 -pix_fmt bgr24 -an -vcodec rawvideo -f rawvideo -preset ultrafast -tune zerolatency -')

class VideoApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Launch a subprocess to provide video frames
        self.subprocess_cmd = ffmpeg_cmd
        self.subprocess = subprocess.Popen(self.subprocess_cmd, stdout=subprocess.PIPE)

        # Create a canvas for displaying frames
        self.canvas = tk.Canvas(window, width=width, height=height)  # Set dimensions accordingly
        self.canvas.pack()

        # Button to close the application
        self.close_button = tk.Button(window, text="Close", command=self.close_app)
        self.close_button.pack()

        # Create a thread to read and display frames
        self.thread = threading.Thread(target=self.show_frame)
        self.thread.daemon = True  # Close thread when the main program exits
        self.thread.start()

    def show_frame(self):
        while True:
            # Read a frame from subprocess stdout
            raw_frame = self.subprocess.stdout.read(width * height * 3)  # Adjust dimensions accordingly

            if not raw_frame:
                break  # Break the loop if there are no more frames

            # Convert the byte data to a NumPy array
            frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height, width, 3))  # Adjust dimensions accordingly

            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to ImageTk format
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the canvas with the new frame
            self.canvas.img = img_tk  # Keep a reference to avoid garbage collection
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

            # Update the Tkinter window
            self.window.update_idletasks()
            self.window.update()

    def close_app(self):
        # Terminate the subprocess and close the Tkinter window
        self.subprocess.terminate()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root, "Tkinter Video App")
    root.mainloop()
