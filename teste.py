from ultralytics import YOLO
import cv2

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Couldn't open the camera.")
        return
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Couldn't capture the frame.")
            return

        model = YOLO("screen.pt")
        results = model.predict(frame)
        for result in results:
            x0, y0, w, h = result.boxes.xywh.to("cpu").numpy().astype(int)
            print(result.boxes.xywh.to("cpu").numpy().astype(int))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break




if __name__ == "__main__":
    main()