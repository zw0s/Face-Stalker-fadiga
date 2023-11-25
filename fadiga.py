from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
from smbus2 import SMBus
import numpy as np
import playsound
import imutils
import time
import dlib
import cv2
import matplotlib.pyplot as plt


addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1


# Definir constantes
ALARME = "sonoalarm.wav"
WEBCAM = 0
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 40
CONTADOR = 0
ALARME_ON = False


def sound_alarm(path=ALARME):
    # Tocar som de alarme
    playsound.playsound(ALARME)


def get_nose_landmarks(shape):

    nose_landmark = shape.part(30)
    return nose_landmark.x, nose_landmark.y

# A CONTAGEM COMEÇA NO 0!!!!


def eye_aspect_ratio(eye):
    # Calcula a distancia euclidiana entre as landmarks dos olhos na vertical (x, y)
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Calcula a distancia euclidiana entre as landmark dos olhos na vertical (x, y)
    C = dist.euclidean(eye[0], eye[3])

    # Calcula a proporção do olho
    ear = (A + B) / (2.0 * C)

    return ear


# Dlib face detector
print("[INFO] carregando o preditor de landmark...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Pegar os índices do previsor, para olhos esquerdo e direito
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Inicializa o vídeo
print("[INFO] inicializando streaming de vídeo...")
vs = VideoStream(src=WEBCAM).start()
time.sleep(1.0)

# Desenhar um objeto do tipo figure
y = [None] * 100
x = np.arange(0, 100)
fig = plt.figure()
ax = fig.add_subplot(111)
li, = ax.plot(x, y)
plt.xlim([0, 100])
plt.ylim([0, 0.4])

# Loop sobre os frames do vídeo
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar faces (grayscale)
    faces = detector(gray, 0)

    # Loop nas detecções de faces
    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)
        nareba = predictor(gray, face)

        # Extrai coordenadas dos olhos e calcular a proporção de abertura
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # Proporção média para os dois olhos
        ear = (leftEAR + rightEAR) / 2.0

        # Desenha o contorno convexo dos olhos
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        nose_x, nose_y = get_nose_landmarks(nareba)
        cv2.circle(frame, (nose_x, nose_y), 5, (0, 255, 0), -1)
        print(f"Coordenadas do Nariz - X: {nose_x}, Y: {nose_y}")

        if (nose_x-270)>0 :
            bus.write_byte(addr, 0x2)
        elif (nose_x-230)<0 :
            bus.write_byte(addr, 0x1)
        elif (nose_y-190)>0 :
            bus.write_byte(addr, 0x3)
        elif (nose_y-150)>0 :
            bus.write_byte(addr, 0x4)
        else:
            bus.write_byte(addr, 0x0)

        # Salvar historico para plot
        y.pop(0)
        y.append(ear)

        # Atualizar canvas
        li.set_ydata(y)
        fig.canvas.draw()
        plt.pause(0.01)

        # Checar proporção x threshold(limite)
        if ear < EYE_AR_THRESH:
            CONTADOR += 1

            # Dentro dos critérios, soar o alarme
            if CONTADOR >= EYE_AR_CONSEC_FRAMES:
                # Ligar alarme
                if not ALARME_ON:
                    ALARME_ON = True
                    t = Thread(target=sound_alarm)
                    t.deamon = True
                    t.start()

                cv2.putText(frame, "[ALERTA] FADIGA!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Caso acima do limite, resetar o contador e desligar o alarme
        else:
            CONTADOR = 0
            ALARME_ON = False

            # Mostrar a proporção de abertura dos olhos
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Mostrar frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # Tecla para sair do script "q"
    if key == ord("q"):
        break

# Encerra
cv2.destroyAllWindows()
vs.stop()
