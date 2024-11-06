from math import sqrt
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

    h, w, _ = frame.shape
    center = frame[h // 2, w // 2]

    while not isRed(center):
        ret, frame = cap.read()

        if not ret:
            print("Erro ao capturar o frame")
            return

        h, w, _ = frame.shape
        center = frame[h // 2, w // 2]

    while True:
        time.sleep(1)
        frame_capture, frame = cap.read()

        if not frame_capture:
            print("Erro ao capturar o frame")
            break

        # Converte o frame para escala de cinza
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar um threshold para converter em preto e branco
        _, binary_frame = cv2.threshold(gray_frame, 225, 255, cv2.THRESH_BINARY)

        # Mostrar o frame original e o frame binarizado
        #cv2.imshow('Frame Original', frame)
        #cv2.imshow('Frame Binario', binary_frame)

        # Pra pegar o valor que está no centro da imagem
        h, w = binary_frame.shape
        center = binary_frame[h // 2, w // 2]

        if i < 4:
            # Armazenar os valores de tempo de bit na lista
            tempo_bit[i] = 1 if center != 0 else 0
            i += 1
            print(f"tempo de bit capturado: {list(tempo_bit)}")
        else:
            # Verificação da condição para capturar o bit
            if tempo_bit == [1, 0, 0, 1]:
                bits_validos[p] = 1 if center != 0 else 0
                print(f"Bit válido capturado: {bits_validos[p]}") # Mostra o bit válido capturado da rodada
                p += 1
                if p == 8: # Verifica se capturou os 8 bits válidos
                    print(f"Bits válido capturado: {list(bits_validos)}")
                    break

            # Resetar o índice e a lista
            i = 0
            tempo_bit = [0, 0, 0, 0]

        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture()
