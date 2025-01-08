# Trabajo de curso
## Control de Personajes en Tiempo Real Usando MediaPipe y Unreal Engine

## 🌟 Highlights
 - Control en tiempo real de un Maniquí usando IK y MediaPipe pose
   
![tfvc](https://github.com/user-attachments/assets/fb7a6284-231c-4946-a532-1b4ddea3107e)
   
## ℹ️ Overview
Nuestra idea inicial era usar Yolo pose estimation, pero nos encontramos con un problema, no te daba las coordenadas 3D de los puntos de interés, entonces después de mirar varias opciones, nos quedamos con mediapipe, que sí nos daban las coordenadas 3D de los “landmarks”.

El script de python lo que hace principalmente es abrir un “video source”, ya sea un video en disco o la webcam en tiempo real, pasa cada frame por el modelo de mediapipe pose para detectar si hay una persona en el frame y calcular los “landmarks” del esqueleto.

Al principio pensábamos usar el siguiente esqueleto como modelo para pasarlo a un “rig” propio en UE y después hacer un retarget en tiempo real. Pero nos dimos cuenta que era demasiado complejo, entonces decidimos primeramente usar las posiciones de las manos, los pies y el rootbone (El centro de la cadera), esas posiciones se usarán como “Goal” para los IK de cada parte, y el rootbone se modificará la posición directamente.


Python 3.9.5
UE 5.5

instalar opencv

instalar mediapipe

En caso de ejecutar el fichero python y recibir un error ejecutar "pip install msvc-runtime"

Proyecto UE5: https://drive.google.com/file/d/14ZpiFySyOemnJM_IOFOxbUrNqS4MjHne/view?usp=drive_link

Ejecutar el binario compilado de UE5

Ejecutar mediapipepose.py
