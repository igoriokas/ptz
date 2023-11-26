import cv2
import tkinter as tk
from PIL import Image, ImageTk

class VideoApp:
    def __init__(self, window, window_title, video_source):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = cv2.VideoCapture(video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = tk.Button(window, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(padx=10, pady=10)

        self.update()
        self.window.mainloop()

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(30, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the VideoApp class
root = tk.Tk()
rtsp_url = "rtsp://rtspstream:539a545d904d92acfa6869e549fa763e@zephyr.rtsp.stream/movie"
rtsp_url = "rtsp://192.168.0.101:554/ch0.liv"
rtsp_url = "rtsp://192.168.0.100/ProfileToken_1_1"
app = VideoApp(root, "Video App", video_source=rtsp_url)
