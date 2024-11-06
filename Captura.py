import os
import shutil  # Para remover a pasta 'capturas'
import time

import cv2
import numpy as np


def capture():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a câmera")
        return

    bits_validos = [0] * 8  # Lista para armazenar os bits capturados
    p = 0
    tempo_bit = [0] * 4  # Controle de temporização dos bits
    i = 0
    detectou_verde = False
    frame_count = 0  # Contador para frames dentro de um tempo de bit
    transmission_ended = False  # Flag para o fim da transmissão
    capture_session = 1  # Contador para as sessões de captura

    # Remove a pasta "capturas" se já existir, para evitar erros
    base_dir = "capturas"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    # Cria uma nova pasta para esta sessão de captura
    session_dir = os.path.join(base_dir, f"session_{capture_session}")
    os.makedirs(session_dir)

    while True:
        ret, frame = cap.read()

        if not ret:
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

        # Detecta o início do sinal verde
        if center_green > 0 and not detectou_verde:
            detectou_verde = True
            print("Tela verde detectada! Iniciando leitura de bits.")
            time.sleep(1)

        if detectou_verde and not transmission_ended:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)

            cv2.imshow('Frame Original', frame)
            cv2.imshow('Frame Binário', binary_frame)

            # Captura o frame atual para o tempo de bit atual
            center = binary_frame[h // 2, w // 2]

            # Define a pasta bit_0 ou bit_1 com base no valor do bit central
            bit_value = 1 if center != 0 else 0
            bit_dir = os.path.join(session_dir, f"bit_{bit_value}")

            # Cria o diretório do bit (bit_0 ou bit_1) se ele não existir
            if not os.path.exists(bit_dir):
                os.makedirs(bit_dir)

            # Salva o frame no diretório apropriado
            frame_filename = f"frame_{frame_count + 1}.png"
            cv2.imwrite(os.path.join(bit_dir, frame_filename), binary_frame)
            print(f"Frame salvo em {bit_dir}/{frame_filename} para o tempo de bit {i + 1}")

            frame_count += 1  # Incrementa o contador de frames

            # Verifica se capturamos 4 frames
            if frame_count == 4:
                frame_count = 0
                capture_session += 1  # Incrementa o contador da sessão para a próxima
                session_dir = os.path.join(base_dir, f"session_{capture_session}")
                os.makedirs(session_dir)  # Cria uma nova pasta para a próxima sessão de captura

            # Armazena o valor do bit central
            if i < 4:
                tempo_bit[i] = bit_value
                i += 1
                print(f"Tempo de bit capturado: {tempo_bit}")
            else:
                # Verifica a sequência de sincronização [1, 0, 0, 1]
                if tempo_bit == [1, 0, 0, 1]:
                    bits_validos[p] = bit_value
                    print(f"Bit válido capturado: {bits_validos[p]}")
                    p += 1

                    if p == 8:
                        print(f"Bits válidos capturados: {bits_validos}")
                        transmission_ended = True  # Marca o fim da transmissão

                # Reseta os valores para o próximo tempo de bit
                i = 0
                tempo_bit = [0] * 4

        if cv2.waitKey(1) & 0xFF == 27:  # Pressione "Esc" para encerrar
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    comeco = int(input("Digite 1 para começar \n"))
    if comeco == 1:
        capture()
