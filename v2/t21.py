import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import subprocess as sp
import shlex

rtsp_url = "rtsp://10.30.30.12:554/ch0.liv"
width = 1920
height = 1080
fps = 25

ffmpeg_cmd = shlex.split(f'ffmpeg -nostdin -probesize 32 -flags low_delay -fflags nobuffer -rtsp_transport tcp -i {rtsp_url} -vf fps=25 -pix_fmt bgr24 -an -vcodec rawvideo -f rawvideo -preset ultrafast -tune zerolatency -')
process = sp.Popen(ffmpeg_cmd, stdout=sp.PIPE)

class VideoApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.vid = cv2.VideoCapture(rtsp_url)
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        self.vid.release()

        self.btn_snapshot = tk.Button(window, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(padx=10, pady=10)

        self.update()
        self.window.mainloop()

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def update(self):
        raw_frame = process.stdout.read(width * height * 3)
        if len(raw_frame) == (width*height*3):
            frame = np.frombuffer(raw_frame, np.uint8)
            frame = frame.reshape((height, width, 3))

            # Convert the OpenCV BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the NumPy array to a PhotoImage object
            photo = ImageTk.PhotoImage(Image.fromarray(rgb_frame))
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)

        self.window.after(30, self.update)

    def __del__(self):
        process.stdout.close()
        process.wait()
        root.destroy()

# Create a window and pass it to the VideoApp class
root = tk.Tk()
app = VideoApp(root, "Video App")
