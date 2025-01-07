import cv2
import mediapipe as mp
import socket
import json
import math

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

used_landmark = [15, 16, 27, 28]

# Capturar video desde la cámara web
cap = cv2.VideoCapture("video.mp4")
image = cv2.imread("uppose.png", cv2.IMREAD_COLOR)
first_root_saved = 0
first_root_post = {
        'x': 0,
        'y': 0,
        'z': 0
}

UDP_IP = "127.0.0.1"
UDP_PORT = 10001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_to_ue(str_data):
    encoded = str_data.encode('utf-8')
    sock.sendto(encoded, (UDP_IP, UDP_PORT))
send_to_ue("Prueba enviando udp")

def calculate_body_rotation(left_shoulder, right_shoulder):
    # Coordenadas de los hombros
    x1, y1 = left_shoulder
    x2, y2 = right_shoulder

    # Calcular el ángulo de rotación (en radianes)
    angle_rad = math.atan2(y2 - y1, x2 - x1)

    # Convertir el ángulo a grados
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def convert_to_feet_centered(world_landmarks, scale_factor, height, width):
    global first_root_saved
    # Obtener puntos necesarios
    hip_left = world_landmarks[23]
    hip_right = world_landmarks[24]
    foot_left = world_landmarks[27]
    foot_right = world_landmarks[28]
    
    shoulder_left = world_landmarks[12]
    shoulder_right = world_landmarks[11]

    rot = calculate_body_rotation((shoulder_left.x, shoulder_left.y), (shoulder_right.x, shoulder_right.y))
    print(rot)

    altura_real = 170
    # Calcular el centro de los pies

    if first_root_saved == 0:
        first_root_post['x'] = ((foot_left.x + foot_right.x) / 2) * width
        first_root_post['y'] = ((foot_left.y + foot_right.y) / 2) * height
        first_root_post['z'] = (foot_left.z + foot_right.z) / 2
        first_root_saved = 1

    center_feet = first_root_post

    root_bone_center = {
        'x': ((hip_left.x + hip_right.x) / 2) * width,
        'y': ((hip_left.y + hip_right.y) / 2) * height,
        'z': (hip_left.z + hip_right.z) / 2
    }

    head_y = -(world_landmarks[0].y * height - center_feet['y'])
    distancia_real = altura_real/head_y

    # Convertir cada landmark
    converted_landmarks = []
    for landmark in world_landmarks:
        x_relative = (landmark.x * width - center_feet['x']) * scale_factor * (distancia_real * 1.2)
        y_relative = -(landmark.y * height - center_feet['y']) * scale_factor * distancia_real
        z_relative = (landmark.z - center_feet['z']) * scale_factor
        converted_landmarks.append({'x': x_relative, 'y': y_relative, 'z': z_relative})

    x_relative = (root_bone_center['x'] - center_feet['x']) * scale_factor * (distancia_real * 1.2)
    y_relative = -(root_bone_center['y'] - center_feet['y']) * scale_factor * distancia_real
    z_relative = (root_bone_center['z'] - center_feet['z']) * scale_factor
   

    converted_landmarks.append({'x': x_relative, 'y': y_relative-85, 'z': z_relative})

    return converted_landmarks, rot

while cap.isOpened():
    # Leer fotograma de la cámara
    ret, frame = cap.read()
    if not ret:
        break
    height, width, _ = frame.shape
    # Convertir la imagen a RGB

    # Procesar la imagen y obtener los resultados
    results = pose.process(frame)
    
    # Dibujar la pose estimada en el fotograma original
    if results.pose_landmarks:
        world_landmarks, rot = convert_to_feet_centered(results.pose_landmarks.landmark, 1, height, width)
        str_to_send = ""
        for i in used_landmark:
            head_landmark = world_landmarks[i]
            landmark_str = str(round(head_landmark["x"], 2)) +";"+ str((round(head_landmark["z"], 2)))+ ";" + str(round(head_landmark["y"], 2))
            str_to_send += landmark_str + "$"
        #str_to_send = str_to_send[:-1]
        head_landmark = world_landmarks[-1]
        #print(head_landmark)
        landmark_str = str(round(head_landmark["x"], 2)) +";"+ str((round(head_landmark["z"], 2)))+ ";" + str(round(head_landmark["y"], 2))
        str_to_send += landmark_str + "$" + str(rot)
        send_to_ue(str_to_send) 
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Mostrar el fotograma
    cv2.imshow("Pose Estimation", frame)

    # Detener con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #break #solo 1 frame

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()

#x 112.2    77
#y -174.8   -8
#z -37.4    143
