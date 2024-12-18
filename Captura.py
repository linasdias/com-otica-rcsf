from math import sqrt
from ultralytics import YOLO
import cv2
import time

def isRed(bgr_color)->bool:
    blue, green, red = bgr_color
    # Define um limiar para considerar uma cor como "vermelha"
    return red > 200 and red > blue and red > green

def isGreen(bgr_color)->bool:
    blue, green, red = bgr_color
    # Define um limiar para considerar uma cor como "vermelha"
    return green > 200 and green > blue and green > red

def isBlack(bgr_color, threshold=30):
    blue, green, red = bgr_color
    return blue < threshold and green < threshold and red < threshold

def isWhite(bgr_color, threshold=225):
    blue, green, red = bgr_color
    return blue > threshold and green > threshold and red > threshold

def capture():
    model = YOLO("screen.pt")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a câmera")
        return
    

    bits_validos = [0, 0, 0, 0, 0, 0, 0, 0] # Inicializa a lista para armazenar os bits válidos
    p = 0
    tempo_bit = [0, 0, 0, 0]  # Inicializa a lista para armazenar os bits do tempo de bit, coloquei so 4 mas pode aumentar e se aumentar tem q aumentar na condição na linha 37
    i = 0

    ret, frame = cap.read()

    if not ret:
        print("Erro ao capturar o frame")
        return
    
    classification = 0

    for result in model.predict(frame):
        for color in result.boxes.cls.to("cpu").numpy().astype(int):
            classification = color

    while result.names[classification] != "Red Screen":
        ret, frame = cap.read()

        if not ret:
            print("Erro ao capturar o frame")
            return
        
        for result in model.predict(frame):
            for color in result.boxes.cls.to("cpu").numpy().astype(int):
                classification = color

    print("Iniciando a captura dos bits")

    while True:
        time.sleep(1)
        frame_capture, frame = cap.read()

        if not frame_capture:
            print("Erro ao capturar o frame")
            break

        for result in model.predict(frame):
            for color in result.boxes.cls.to("cpu").numpy().astype(int):
                classification = color

        if result.names[classification] == "White":
            bits_validos[p] = 1
            print("1")
            p += 1
        elif result.names[classification] == "Green Screen":
            bits_validos[p] = 0
            print("0")
            p += 1

        if p == 8:
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture()
