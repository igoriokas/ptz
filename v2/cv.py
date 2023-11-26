import cv2

def play_rtsp_stream(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame")
            break

        cv2.imshow("RTSP Player", frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # rtsp_url = "https://rtsp.stream/videos/movie.mp4"
    rtsp_url = "https://rtsp.stream/videos/pattern.mp4"
    play_rtsp_stream(rtsp_url)