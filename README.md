Propuesta Inicial de Proyecto

Carrera: Ing. Mecatrónica
Materia: Programación Superior
Periodo: Segundo Parcial / Proyecto Final
Estudiante(s): Christian Bony Negrete Pedraza
Fecha de entrega: 2025-10-13


---

1. Datos Generales del Proyecto

Campo	Descripción

Nombre del proyecto:	ElectroVision Pro – Identificador inteligente de componentes y resistencias
Tipo de aplicación:	☑ Escritorio ☐ Web ☐ Móvil ☐ Otro: __________
Lenguaje / entorno de desarrollo:	Python 3.11 (TensorFlow 2.14, NumPy 1.26.4, OpenCV, Tkinter, Pillow, Pandas, scikit-learn).
Repositorio Git (opcional):	(agregar enlace cuando se cree)
Uso de Inteligencia Artificial:	☑ Sí — Redes neuronales propias (clasificación de componentes y lectura de resistencias por bandas).


Cómo y dónde se aplica la IA:
Se entrenarán dos modelos propios:

1. CNN-Componentes (clasificación multiclase) para reconocer: Módulo Relé 2 canales, 7404, Diodo Zener, 7805.


2. ResistorNet (clasificación multi-cabeza) para leer bandas de color (4/5 bandas) en una caja cerrada con iluminación controlada y calcular valor+tol. Ambos se integran en la app de escritorio para inferencia en tiempo real con webcam.




---

2. Descripción del Proyecto

Aplicación de escritorio que, con una webcam física montada en una caja de iluminación (fondo mate, luz LED difusa estable), realiza dos tareas:

Reconocimiento de componentes: la CNN-Componentes identifica en vivo el elemento frente a la cámara y muestra una ficha (imagen de referencia y enlace a datasheet).

Lectura de resistencias: la ResistorNet detecta 4/5 bandas, infiere dígitos, multiplicador y tolerancia, y muestra el valor equivalente (Ω/kΩ/MΩ) y la tolerancia.


Se desarrollará el pipeline completo: adquisición de datos, etiquetado, aumento, entrenamiento, validación, exportación del modelo y despliegue en la GUI.

Objetivos principales

1. Construir datasets propios (componentes y resistencias) en la caja cerrada, con estándares de captura.


2. Entrenar CNN-Componentes (clasificación multiclase) y ResistorNet (multi-cabeza para 4/5 bandas).


3. Integrar ambos modelos en una GUI (Tkinter) con overlay en tiempo real.


4. Medir y reportar métricas (accuracy/F1, exactitud del valor de resistencia ± tolerancia).


5. Empaquetar inferencia (SavedModel/TFLite) y documentar reproducibilidad.




---

3. Diseño Técnico y Aplicación de POO

3.1 Arquitectura por capas

Capa de Captura: CameraStream (OpenCV), fija resolución, controla balance de blancos/exposición.

Capa de Modelos: ModelStrategy (ABC) define interfaz común; implementaciones concretas:

CNNComponentClassifier (Keras)

ResistorNetClassifier (Keras, multi-output)


Capa de Datos: DatasetProvider (ABC) y derivados (ComponentDataset, ResistorDataset) para lectura, partición (train/val/test), augmentations.

Capa de Entrenamiento: Trainer (ABC); concretos ClassificationTrainer y MultiHeadTrainer.

Capa de Post-proceso: Postprocessor (ABC); concretos ComponentPost, ResistorDecoder (convierte logits a dígitos/multiplicador/tolerancia y valor en Ω).

Capa de Presentación (GUI): MainWindow (Tkinter) orquesta modos (Componentes/Resistencias), muestra resultados y botones (datasheet, reintentar).


3.2 Principios POO (cómo se aplican)

Encapsulamiento

Cada responsabilidad vive en su clase: cámara, dataset, modelo, entrenamiento, post-proceso y GUI.

Atributos internos (_model, _optimizer, _augmenter) permanecen privados; la GUI solo llama a métodos públicos (predict, load, start, stop).


Uso de constructores

__init__(…) recibe configuración declarativa (rutas, tamaños de entrada, clases, ROI de la caja).

Se validan tipos/valores y se cargan pesos si weights_path ≠ None.


Herencia

ModelStrategy → clases hijas (CNNComponentClassifier, ResistorNetClassifier) comparten firma load(), predict(frame); variaciones se implementan en los hijos.

Trainer → ClassificationTrainer y MultiHeadTrainer comparten ciclo de entrenamiento (fit/validate/save) y difieren en la construcción de pérdidas y métricas.


Polimorfismo

La GUI no sabe si usa CNNComponentClassifier o ResistorNetClassifier; solo invoca strategy.predict(frame) y renderiza el resultado.

Permite cambiar de modelo (o versión) sin tocar el resto del código.


Interfaces / Clases abstractas (abc.ABC)

ModelStrategy(ABC): contrato común (load, predict, input_size) → garantiza intercambiabilidad.

DatasetProvider(ABC): prepare(), iter_train(), iter_val() → datasets homogéneos para cualquier trainer.

Trainer(ABC): train(), evaluate(), save_best() → ciclo estándar con callbacks.

Postprocessor(ABC): decode(raw_outputs) → separa la lógica de negocio (valor Ω y tolerancia) de la red.


Composición (principio adicional)

MainWindow compone CameraStream + ModelStrategy + Postprocessor para construir la experiencia de usuario.




---

4. Modelado de las Redes

4.1 CNN-Componentes (clasificación)

Entrada: 224×224×3 (RGB normalizado).

Arquitectura: CNN ligera (p. ej., EfficientNet-B0 o MobileNetV2 pequeña) + Dense final con 4 clases.

Pérdida: CategoricalCrossentropy; métricas: Accuracy, F1 macro.

Aumentos: recorte suave, brillo/contraste±, ligera rotación (±5°), mixup opcional.

Salida: clase top-1 + confianza.


4.2 ResistorNet (multi-cabeza para 4/5 bandas)

Entrada: ROI 256×96×3 (resistencia horizontal en caja).

Backbone: CNN pequeña compartida.

Cabezas (softmax):

Head-D1, Head-D2, Head-D3 (dígitos 0–9; D3 puede ir vacío en 4 bandas con clase “none”)

Head-MUL (multiplicador: negro…blanco, oro, plata)

Head-TOL (tolerancia: oro, plata, brown, red, green, blue, violet, gray, none)


Pérdida total: suma ponderada de las pérdidas de cada cabeza.

Post-proceso: ResistorDecoder arma el valor en Ω y la tolerancia, valida coherencia 4/5 bandas.

Métricas: F1 macro por cabeza + Exactitud de valor (acierto del valor real dentro de la tolerancia nominal).



---

5. Flujo de Datos y Entrenamiento

Etapa	Detalle

Adquisición	Capturas en la caja (720p) con trípode y luz fija (temperatura estable).
Etiquetado	ComponentDataset: clase por imagen. ResistorDataset: etiquetas por cabeza (D1, D2, D3/none, MUL, TOL).
Partición	70/15/15 (train/val/test) estratificada.
Aumentos	Fotométricos leves; evitar alterar colores de bandas (controlado).
Entrenamiento	Early stopping, ReduceLROnPlateau, batch norm y dropout.
Validación	Accuracy/F1; matriz de confusión; para resistencias: % de acierto exacto y % dentro de tolerancia.
Exportación	SavedModel y/o TFLite para inferencia.
Reproducibilidad	Scripts train_components.py, train_resistor.py, export_model.py.



---

6. Funcionalidades Principales

Nº	Funcionalidad	Descripción	Estado

1	Captura de webcam	OpenCV 640×480, control de exposición/ WB fijo.	☐ Planeada
2	Modo Componentes	Inferencia con CNN-Componentes, overlay y ficha con datasheet.	☐ Planeada
3	Modo Resistencias	ROI en caja; inferencia ResistorNet; valor y tolerancia.	☐ Planeada
4	Anti-ruido	Debounce por N frames + umbrales de confianza.	☐ Planeada
5	GUI (Tkinter)	Ventana principal; selector de modo; panel de resultados.	☐ Planeada
6	Métricas en app	Mostrar confidencia, conteos, tiempos de inferencia.	☐ Planeada
7	Exportación/Deploy	Carga de SavedModel/TFLite, compatibilidad Windows.	☐ Planeada



---

7. Métricas, Criterios de Aceptación y Pruebas

Componentes: Accuracy ≥ 90% y F1 macro ≥ 0.90 en set de prueba.

Resistencias:

F1 macro por cabeza ≥ 0.90;

Exactitud de valor (exact match) ≥ 85%;

Dentro de tolerancia (valor medido vs. nominal) ≥ 95%.


Rendimiento: ≥ 15 FPS en inferencia en laptop estándar.

Robustez: Pruebas cruzadas cambiando ligeramente altura/posición dentro del ROI.



---

8. Recursos y Riesgos

HW: Webcam 720p/1080p, caja de iluminación, PC Windows con CPU i5/Ryzen y 8–16 GB RAM.

Riesgos: Variabilidad de color en bandas, sombras, tolerancias de fabricación, sobreajuste.

Mitigación: Iluminación estable, augmentations moderados, validación cruzada, calibración de cámara.



---

9. Compromiso del Estudiante

Desarrollaré e integraré redes neuronales propias y la GUI con POO.

Presentaré demo funcional con métricas y reproducibilidad.

Defenderé el diseño (clases abstractas, herencia/polimorfismo) en la evaluación.


Firma: __________________________


---

11. Validación del Docente (completa el profesor)

Campo	Detalle

Visto bueno del docente:	☐ Aprobado ☐ Requiere ajustes ☐ Rechazado
Comentarios / Observaciones:	
Firma docente:	
Fecha de revisión:	



---
