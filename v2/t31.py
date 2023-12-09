import cv2
import numpy as np
import subprocess as sp
import shlex
import cvui

WINDOW_NAME = 'CVUI'
cvui.init(WINDOW_NAME)
count = 0

# rtsp_url = "rtsp://10.30.30.12:554/ch0.liv"
rtsp_url = "rtsp://10.30.30.11/ProfileToken_1_1"

cap = cv2.VideoCapture(rtsp_url)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f'{width}x{height} {fps}fps')
cap.release()

# https://stackoverflow.com/questions/71746326/obtaining-frames-from-ip-camera-with-low-latency
# https://stackoverflow.com/questions/60462840/ffmpeg-delay-in-decoding-h264
# ffmpeg -nostdin -probesize 32 -flags low_delay -fflags nobuffer -rtsp_flags listen -rtsp_transport tcp -stimeout 1000000 -an -i {rtsp_stream0} -pix_fmt bgr24 -an -vcodec rawvideo -f rawvideo pipe:
# ffmpeg_cmd = shlex.split(f'ffmpeg -nostdin -probesize 32 -flags low_delay -fflags nobuffer -rtsp_transport tcp -i {rtsp_url} -vf fps=25 -pix_fmt bgr24 -an -vcodec rawvideo -f rawvideo -')
ffmpeg_cmd = shlex.split(f'ffmpeg -nostdin -probesize 32 -flags low_delay -fflags nobuffer -rtsp_transport tcp -i {rtsp_url} -vf fps=25 -pix_fmt bgr24 -an -vcodec rawvideo -f rawvideo -preset ultrafast -tune zerolatency -')
process = sp.Popen(ffmpeg_cmd, stdout=sp.PIPE, stderr=sp.DEVNULL)

mykeys = {
    0: {'name': 'UP'},
    1: {'name': 'DOWN'},
    2: {'name': 'LEFT'},
    3: {'name': 'RIGHT'},
}

lastKey = None

while True:
    raw_frame = process.stdout.read(width*height*3)

    if len(raw_frame) != (width*height*3):
        print('Error reading frame!!!')  # Break the loop in case of an error (too few bytes were read).
        break

    # Transform the byte read into a numpy array, and reshape it to video frame dimensions
    frame = np.frombuffer(raw_frame, np.uint8)
    frame = frame.reshape((height, width, 3))

    if (cvui.button(frame, 110, 80, 150, 50, "CLICK")):
        count += 1

    # cvui.text(frame, 250, 80, f'counter {count}')
    cvui.printf(frame, 250, 90, 0.8, 0xff0000, "Button click count: %d", count);
    cvui.printf(frame, 50, 50, 0.8, 0xff0000, f'Last key: {lastKey} {mykeys.get(lastKey)}');
    cvui.imshow(WINDOW_NAME, frame)

    key = cv2.waitKey(10)
    if key >= 0:
        lastKey = key

    if key == ord('q'):
        break

  
process.stdout.close()
process.wait()
cv2.destroyAllWindows()
