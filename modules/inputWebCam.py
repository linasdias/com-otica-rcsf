import cv2

def inputWebCam():
    webcam = cv2.VideoCapture(0)
    if webcam.isOpened():
        print("Webcam is connected")
        ret, frame = webcam.read()
        while ret:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            ret, frame = webcam.read()
            cv2.imshow("Webcam", frame)
    else:
        print("Webcam is not connected")