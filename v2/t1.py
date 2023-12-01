import cv2

def play_rtsp_stream(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_DSHOW)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame")
            break

        cv2.imshow("RTSP Player", frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # rtsp_url = "rtsp://10.30.30.12:554/ch0.liv"
    rtsp_url = "rtsp://10.30.30.11/ProfileToken_1_1"
    play_rtsp_stream(rtsp_url)
