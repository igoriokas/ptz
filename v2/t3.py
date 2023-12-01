import cv2
import numpy as np
import subprocess as sp
import shlex


rtsp_url = "rtsp://10.30.30.12:554/ch0.liv"
width=1920
height=1080

# rtsp_url = "rtsp://10.30.30.11/ProfileToken_1_1"
# width = 960
# height = 576

fps = 25

# https://stackoverflow.com/questions/71746326/obtaining-frames-from-ip-camera-with-low-latency
# https://stackoverflow.com/questions/60462840/ffmpeg-delay-in-decoding-h264
# ffmpeg -nostdin -probesize 32 -flags low_delay -fflags nobuffer -rtsp_flags listen -rtsp_transport tcp -stimeout 1000000 -an -i {rtsp_stream0} -pix_fmt bgr24 -an -vcodec rawvideo -f rawvideo pipe:
ffmpeg_cmd = shlex.split(f'ffmpeg -nostdin -probesize 32 -flags low_delay -fflags nobuffer -rtsp_transport tcp -i {rtsp_url} -vf fps=25 -pix_fmt bgr24 -an -vcodec rawvideo -f rawvideo -')
ffmpeg_cmd = shlex.split(f'ffmpeg -nostdin -probesize 32 -flags low_delay -fflags nobuffer -rtsp_transport tcp -i {rtsp_url} -vf fps=25 -pix_fmt bgr24 -an -vcodec rawvideo -f rawvideo -preset ultrafast -tune zerolatency -')
process = sp.Popen(ffmpeg_cmd, stdout=sp.PIPE) #,stderr=sp.DEVNULL

while True:
    raw_frame = process.stdout.read(width*height*3)

    if len(raw_frame) != (width*height*3):
        print('Error reading frame!!!')  # Break the loop in case of an error (too few bytes were read).
        break

    # Transform the byte read into a numpy array, and reshape it to video frame dimensions
    frame = np.frombuffer(raw_frame, np.uint8)
    frame = frame.reshape((height, width, 3))
    cv2.imshow('frame', frame)

    key = cv2.waitKey(5)

    if key == 27:
        break
  
process.stdout.close()
process.wait()
cv2.destroyAllWindows()
