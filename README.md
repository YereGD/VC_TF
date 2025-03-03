# Trabajo de curso
## Control de Personajes en Tiempo Real Usando MediaPipe y Unreal Engine

## 🌟 Highlights
 - Control en tiempo real de un Maniquí usando IK y MediaPipe pose
   
![tfvc](https://github.com/user-attachments/assets/fb7a6284-231c-4946-a532-1b4ddea3107e)

 - Video de presentación

   https://drive.google.com/file/d/1Wul9qwGuyMQetGKhewn3Mw8z487GlX7E/view?usp=sharing
   
## ℹ️ Overview
Nuestra idea inicial era usar Yolo pose estimation, pero nos encontramos con un problema, no te daba las coordenadas 3D de los puntos de interés, entonces después de mirar varias opciones, nos quedamos con mediapipe, que sí nos daban las coordenadas 3D de los “landmarks”.

El script de python lo que hace principalmente es abrir un “video source”, ya sea un video en disco o la webcam en tiempo real, pasa cada frame por el modelo de mediapipe pose para detectar si hay una persona en el frame y calcular los “landmarks” del esqueleto.

Al principio pensábamos usar el siguiente esqueleto como modelo para pasarlo a un “rig” propio en UE y después hacer un retarget en tiempo real. Pero nos dimos cuenta que era demasiado complejo, entonces decidimos primeramente usar las posiciones de las manos, los pies y el rootbone (El centro de la cadera), esas posiciones se usarán como “Goal” para los IK de cada parte, y el rootbone se modificará la posición directamente.

![file](https://github.com/user-attachments/assets/22b17ed9-5ced-497c-9b5d-02cd8d8d706f)

Una vez tenga los landmarks, se convertirá las posiciones relativas normalizadas a una estimación de la realidad, usando la altura del maniquí y la altura de la persona que se graba, en este caso 173, pero ponemos 170 porque el landmark no está en la parte superior de la cabeza. También se estimará la rotación del personaje teniendo en cuenta la posición de los hombros.

Después se enviará mediante UDP por el puerto 10001, donde el proyecto de UE estará escuchando (Gracias al plugin https://github.com/getnamo/UDP-Unreal), recogerá los valores y se los enviará al blueprint “AnimGraph” del personaje, que permitirá modificar la pose final del personaje.

![image](https://github.com/user-attachments/assets/f45198c5-4866-4dc1-aed5-d5a6b19d2b92)


### ✍️ Authors
[Adonaí Hernández Bolaños](https://github.com/AdonaiHernandez)

[Yeremay García Déniz](https://github.com/YereGD)


## 🚀 Usage

1. Ejecutar el binario compilado de UE o el proyecto de UE [Release](https://github.com/YereGD/VC_TF/releases/tag/UE5)

2. Ejecutar el script de python "mediapipepose.py"

## ⬇️ Installation

Python 3.9.5

UE 5.5

instalar opencv

instalar mediapipe

En caso de ejecutar el fichero python y recibir un error ejecutar "pip install msvc-runtime"

Proyecto UE5: https://drive.google.com/file/d/14ZpiFySyOemnJM_IOFOxbUrNqS4MjHne/view?usp=drive_link
