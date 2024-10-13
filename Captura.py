import cv2

def capture():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a câmera")
        return

    while True:
        frame_capture, frame = cap.read()

        if not frame_capture:
            print("Erro ao capturar o frame")
            break

        # Converte o frame para escala de cinza
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar um threshold para converter em preto e branco
        _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)

        # Mostrar o frame original e o frame binarizado
        cv2.imshow('Frame Original', frame)
        cv2.imshow('Frame Binario', binary_frame)

        
        # Pra pegar o valor que está no centro da imagem
        h, w = binary_frame.shape
        center = binary_frame[h // 2, w // 2]

        
        if center == 0: 
            bit = 0
        else:
            bit = 1

        print(f"Bit capturado: {bit}")

    
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture()
