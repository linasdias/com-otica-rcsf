import cv2
import numpy as np
import time  # Biblioteca para adicionar a pausa

def capture():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a câmera")
        return

    bits_validos = [0, 0, 0, 0, 0, 0, 0, 0]
    p = 0
    tempo_bit = [0, 0, 0, 0]
    i = 0
    detectou_verde = False

    while True:
        cv2.waitKey(1000)
        frame_capture, frame = cap.read()

        if not frame_capture:
            print("Erro ao capturar o frame")
            break

        # Converte o frame para o espaço de cor HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define os intervalos para a cor verde em HSV
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])

        # Cria uma máscara para a cor verde
        green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        cv2.imshow('Máscara Verde', green_mask)

        # Verifica se a cor verde está presente no centro da imagem
        h, w = green_mask.shape
        center_green = green_mask[h // 2, w // 2]

        if center_green > 0 and not detectou_verde:
            detectou_verde = True
            print("Tela verde detectada! Iniciando leitura de bits.")
            time.sleep(1)  # Pausa de 1 segundo para garantir que o primeiro bit seja mostrado

        if detectou_verde:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)

            cv2.imshow('Frame Original', frame)
            cv2.imshow('Frame Binario', binary_frame)

            center = binary_frame[h // 2, w // 2]

            if i < 4:
                tempo_bit[i] = 1 if center != 0 else 0
                i += 1
                print(f"tempo de bit capturado: {list(tempo_bit)}")
            else:
                if tempo_bit == [1, 0, 0, 1]:
                    bits_validos[p] = 1 if center != 0 else 0
                    print(f"Bit válido capturado: {bits_validos[p]}")
                    p += 1
                    if p == 8:
                        print(f"Bits válidos capturados: {list(bits_validos)}")
                        break
                i = 0
                tempo_bit = [0, 0, 0, 0]

        #if cv2.waitKey(1000) & 0xFF == 27:
           # break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    comeco = int(input("Digite 1 para começar \n"))
    if comeco == 1:
        capture()
