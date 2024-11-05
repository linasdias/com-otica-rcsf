import cv2

# Definir o número máximo de dispositivos de câmera a testar
max_tested_cameras = 10

# Percorrer os índices e verificar se a câmera está disponível
for i in range(max_tested_cameras):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Câmera encontrada no índice {i}")
        cap.release()
    else:
        print(f"Nenhuma câmera no índice {i}")