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
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    rtsp_url = "rtsp://rtspstream:539a545d904d92acfa6869e549fa763e@zephyr.rtsp.stream/movie"
    # rtsp_url = "rtsp://rtspstream:0895ec46a37d8c2db24f39a286a2f22e@zephyr.rtsp.stream/pattern"
    play_rtsp_stream(rtsp_url)
