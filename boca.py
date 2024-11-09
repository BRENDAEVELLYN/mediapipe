#importação do opencv-python
import cv2
import mediapipe as mp  # importação do mediapipe para usar o facemesh
import numpy as np  # função EAR
import time
import pygame

# Inicializa o mixer de áudio
pygame.mixer.init()

# Carrega o arquivo de som
pygame.mixer.music.load("car-horn-155026.mp3")

# pontos dos olhos
# olho esquerdo
p_olho_esq = [385, 380, 387, 373, 362, 263]

# olho direito
p_olho_dir = [160, 144, 158, 153, 33, 133]
p_olhos = p_olho_esq + p_olho_dir

# Pontos da boca
p_boca = [82, 87, 13, 14, 312, 317, 78, 308]

# Função que calcula o EAR
def calculo_ear(face, p_olho_dir, p_olho_esq):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_esq = face[p_olho_esq, :]
        face_dir = face[p_olho_dir, :]
        ear_esq = (np.linalg.norm(face_esq[0] - face_esq[1]) + np.linalg.norm(face_esq[2] - face_esq[3])) / (2 * np.linalg.norm(face_esq[4] - face_esq[5]))
        ear_dir = (np.linalg.norm(face_dir[0] - face_dir[1]) + np.linalg.norm(face_dir[2] - face_dir[3])) / (2 * np.linalg.norm(face_dir[4] - face_dir[5]))
    except:
        ear_esq = 0.0
        ear_dir = 0.0
    media_ear = (ear_esq + ear_dir) / 2
    return media_ear

# Função MAR
def calculo_mar(face, p_boca):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_boca = face[p_boca, :]
        mar = (np.linalg.norm(face_boca[0] - face_boca[1]) + np.linalg.norm(face_boca[2] - face_boca[3]) + np.linalg.norm(face_boca[4] - face_boca[5])) / (2 * np.linalg.norm(face_boca[6] - face_boca[7]))
    except:
        mar = 0.0
    return mar    

# Variáveis de limiar
ear_limiar = 0.27
mar_limiar = 0.1

# Variáveis de estado
dormindo = 0
cap = cv2.VideoCapture(0)

# Soluções do MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Captura de vídeo e detecção facial
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            print("Ignorando o frame vazio da câmera")
            continue
        comprimento, largura, _ = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        saida_facemesh = facemesh.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        try:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame, 
                    face_landmarks, 
                    mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(128, 128, 128), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(50, 100, 200), thickness=1, circle_radius=1)
                )
                
                face = face_landmarks.landmark
                for id_coord, coord_xyz in enumerate(face):
                    if id_coord in p_olhos:
                        coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, largura, comprimento)
                        cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)
                    if id_coord in p_boca:
                        coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, largura, comprimento)
                        cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)

                ear = calculo_ear(face, p_olho_dir, p_olho_esq)
                mar = calculo_mar(face, p_boca)

                cv2.rectangle(frame, (0, 1), (290, 140), (58, 58, 55), -1)
                cv2.putText(frame, f"EAR: {round(ear, 2)}", (1, 24), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
                cv2.putText(frame, f'MAR: {round(mar, 2)} { "abertos" if mar >= mar_limiar else "fechados"}', (1, 50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

                if ear < ear_limiar:                    
                    t_inicial = time.time() if dormindo == 0 else t_inicial
                    dormindo = 1
                if dormindo == 1 and ear >= ear_limiar:
                    dormindo = 0
                t_final = time.time()            
                tempo = (t_final - t_inicial) if dormindo == 1 else 0.0

                cv2.putText(frame, f"Tempo: {round(tempo, 3)}", (1, 80), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
                
                if tempo >= 1.5:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, "Muito tempo com olhos fechados!", (80, 435), cv2.FONT_HERSHEY_DUPLEX, 0.85, (58, 58, 55), 1)
                
                # Verificação do estado da boca aberta e toque do som
                if mar >= mar_limiar:
                    cv2.putText(frame, "Boca aberta", (1, 110), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()
                else:
                    pygame.mixer.music.stop()

        except:
            print("Algo deu errado")
        finally:
            print("Encerrando o processo")

        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF in [ord('c'), ord('C')]:
            break

cap.release()
cv2.destroyAllWindows()






cv2.destroyAllWindows()
