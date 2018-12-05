# Tracking y estimación de movimiento de vehiculos
- Requerimientos
  - Sistema Operativo desarrollado: Windows
  - Lenguaje : Python v3.6.7
  - Librerias requeridas:
    - Pillow : v5.3.0
    - OpenCV : opencv-contrib v3.3.1
- Pasos de ejecución
  - Ejecución: $ python tracking.py 
  - Seleccionar con el Mouse el área de seguimiento.
  - Presionar Enter
- Características y restricciones del algoritmo
  - Cámara: La cámara se encuentra ubicada a una distancia que podemos considerar constante, se encuentra ubicada a 9.5 metros de  altura. Esa orientada para tomar una vista lateral. A continuación se detalla las caracteristicas de la camara utilizada:
    - Distancia focal: 3.9
    - Distancia Cámara - Objeto de seguimiento: 13.435
    - Campo de visión: 69 grados
    - Velocidad de fotogramas: 25 fps
    - Resolución: 1920 x 1080 px
  - Algoritmos de seguimiento:  Se utiliza el algoritmo de Lucas Kanade (LK) que estima el desplazamiento de un punto. El algoritmo selecciona un número determinado de puntos, los cuales son filtrados, tomando en consideración solo los que estan dentro del área de seguimiento.
- Operaciones generales
  1 Aperturar el video.
  2 Iniciar los parámetros y constantes de rectificación de medidas de distancia para la esala de cálculo.
  3 Definir la región de seguimiento del objeto.
  4 Seleccionar el frame x y frame x+1
  5 Seleccionar los puntos de seguimiento.
  6 Seleccionar los puntos correspondientes.
  7 Determinar los vectores de velocidad de cada punto.
  8 Computar la velocidad promedio de los puntos seleccionados.
  9 Mostrar la velocidad calculada.
  10 Ir al paso 4.
