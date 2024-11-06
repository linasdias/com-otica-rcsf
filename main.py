import time

import cv2
import numpy as np


# Função para detectar a intensidade dos pixels em pontos centrais da imagem
def detect_intensity(frame):
    height, width = frame.shape

    # Definir pontos centrais para verificar as intensidades
    points = [
        (height // 2, width // 2),           # Centro
        (height // 2, width // 4),           # Centro Lateral Esquerdo
        (height // 2, (3 * width) // 4),     # Centro Lateral Direito
    ]

    detected_intensity = []
    for point in points:
        y, x = point
        pixel_intensity = frame[y, x]  # Obter valor de intensidade (escala de cinza)
        detected_intensity.append(pixel_intensity)

    return detected_intensity

# Função principal para capturar e decodificar a transmissão de bits
def capture_bits_from_camera(bit_time=1, threshold_start=128, threshold_end=220):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a câmera")
        return

    message = ""
    transmitting = False
    start_time = None  # Para controlar o tempo de transmissão

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Erro ao capturar o frame")
            break

        # Converte o frame para escala de cinza
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar a intensidade dos pixels em pontos centrais da imagem
        detected_intensity = detect_intensity(gray_frame)

        # Exibir as intensidades detectadas no console
        print(f"Intensidades detectadas: {detected_intensity}")

        # Pegar a intensidade central
        center_pixel_intensity = detected_intensity[0]

        # Condições para controle de transmissão
        if center_pixel_intensity < threshold_start and not transmitting:
            print("Iniciando transmissão...")
            transmitting = True
            start_time = time.time()  # Inicia o tempo de captura

        elif center_pixel_intensity > threshold_end and transmitting:
            print("Transmissão finalizada!")
            print(f"Mensagem decodificada: {message}")
            break

        elif transmitting:
            # Verificar se o tempo de bit foi atingido
            elapsed_time = time.time() - start_time
            if elapsed_time >= bit_time:
                # Captura do bit baseado na intensidade do pixel central
                if center_pixel_intensity < threshold_start:
                    bit = '0'
                else:
                    bit = '1'

                message += bit
                print(f"Bit capturado: {bit}")

                # Reiniciar o temporizador para o próximo bit
                start_time = time.time()

        # Exibir o frame em escala de cinza
        cv2.imshow('Transmissão', gray_frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Pressione 'ESC' para sair
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_bits_from_camera()
