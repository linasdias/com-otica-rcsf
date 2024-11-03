import cv2
import numpy as np
from screeninfo import get_monitors
import time

def show_bits(bits):
    # Obtém a resolução da tela
    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height

    # Cria uma imagem de fundo preto
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Mostra a imagem com o temporizador de 5 segundos
    for i in range(5, 0, -1):
        countdown_image = image.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(countdown_image, str(i), (width // 2 - 50, height // 2), font, 10, (255, 255, 255), 10, cv2.LINE_AA)
        cv2.imshow('Bit Sequence', countdown_image)
        cv2.waitKey(1000)

    # Adiciona "1001" antes de cada bit na sequência
    bits_with_prefix = ''.join(["1001" + bit for bit in bits])

    for bit in bits_with_prefix:
        # Define a cor: preto (0) ou branco (1)
        color = (255, 255, 255) if bit == '1' else (0, 0, 0)

        # Cria uma imagem com a cor correspondente
        image = np.zeros((height, width, 3), dtype=np.uint8)
        image[:] = color

        # Adiciona o bit como texto na tela
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_color = (0, 0, 0) if bit == '1' else (255, 255, 255)
        cv2.putText(image, bit, (width // 2 - 50, height // 2), font, 10, text_color, 10, cv2.LINE_AA)

        # Mostra a imagem na tela
        cv2.imshow('Bit Sequence', image)

        # Aguarda 1 segundo
        cv2.waitKey(1000)

    cv2.destroyAllWindows()

# Solicita a sequência de bits do usuário
bits = input("Digite a sequência de bits: ")
print(bits)
show_bits(bits)
