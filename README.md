# Propuesta Inicial de Proyecto 

**Carrera:** Ing. Mecatronica  
**Materia:** Programacion Superior  
**Periodo:** Segundo Parcial / Proyecto Final  
**Estudiante(s):** *Christian Bony Negrete*  
**Fecha de entrega:** *AAAA-MM-DD*  

---

## 1. Datos Generales del Proyecto

| Campo | Descripción |
|--------|-------------|
| **Nombre del proyecto:** | *SmartComponent: Identificación y registro automático de componentes electrónicos* |
| **Tipo de aplicación:** | [x] Escritorio ☐ Web ☐ Móvil ☐ Otro: __________ |
| **Lenguaje / entorno de desarrollo:** | *Python con Tkinter, OpenCV, TensorFlow y Pandas (VS Code)* |
| **Repositorio Git (opcional):** | *(pendiente de creación)* |
| **Uso de Inteligencia Artificial:** | ☐ No ☑ Sí (describir a continuación) |

**Si usas IA, explica brevemente cómo y en qué etapa contribuye:**  
> Se utiliza un modelo de **TensorFlow (entrenado con Teachable Machine)** para clasificar en tiempo real componentes electrónicos capturados por cámara (p. ej., módulo relé, 7404, diodo Zener, 7805). La IA se aplica en la etapa de **detección y clasificación**; luego, la app en **Tkinter** muestra imagen, enlace al datasheet y actualiza cantidades en **Excel**. ChatGPT se usó para **estructurar clases e interfaces POO**, y todo el código fue comprendido y adaptado al proyecto.

---

## 2. Descripción del Proyecto

### Resumen breve
SmartComponent es una aplicación de **escritorio** que reconoce automáticamente componentes electrónicos mediante **visión artificial** e **IA**. Con una **cámara web** y un modelo **TensorFlow**, identifica la pieza observada y, a través de una interfaz **Tkinter**, muestra su imagen de referencia, abre el **datasheet** y permite **gestionar inventario** (sumar/restar/unidades) almacenado en **Excel**. Está dirigido a **laboratorios de electrónica y estudiantes de mecatrónica**, reduciendo errores y acelerando la catalogación.

### Objetivos principales
1. Implementar un clasificador de componentes electrónicos con TensorFlow y OpenCV.  
2. Desarrollar una interfaz en Tkinter para visualizar resultados y abrir datasheets.  
3. Gestionar el inventario en Excel (lectura/escritura) de manera rápida y confiable.  

---

## 3. Diseño Técnico y Aplicación de POO

### Principios de POO aplicados
- [x] Encapsulamiento (atributos privados y métodos públicos)  
- [x] Uso de constructores  
- [x] Herencia  
- [x] Polimorfismo  
- [x] Interfaces o clases abstractas  

### Clases estimadas
- **Cantidad inicial de clases:** 8  
- **Ejemplo de posibles clases:**  
  - `AppConfig` (parámetros y rutas)  
  - `TMSavedModel` (carga/inferencia del modelo TensorFlow)  
  - `TMPreprocessor` (preprocesamiento de imágenes para la red)  
  - `OpenCVCamera` (captura de video)  
  - `ExcelInventoryRepo` (persistencia en Excel)  
  - `TkDetailUI` (interfaz de detalle con botones y datasheet)  
  - `Interfaces (ABC)` → `IModel`, `IPreprocessor`, `ICamera`, `IInventoryRepo`, `IDetailUI`  
  - `MainApp`/`app` (orquestador del flujo)

### Persistencia de datos
- [x] Archivos locales  
- [ ] Base de datos  
- [ ] En memoria (temporal)  
- [ ] Otro: __________

---

## 4. Funcionalidades Principales

| Nº | Nombre de la funcionalidad | Descripción breve | Estado actual |
|----|-----------------------------|-------------------|----------------|
| 1 | Captura de imagen | Obtiene frames de la cámara con OpenCV. | [x] Planeada ☐ En desarrollo |
| 2 | Clasificación con IA | Usa TensorFlow para identificar el componente en tiempo real. | [x] Planeada ☐ En desarrollo |
| 3 | Visualización en interfaz | Muestra nombre, confianza, imagen de referencia y botón de datasheet en Tkinter. | [x] Planeada ☐ En desarrollo |
| 4 | Gestión de inventario | Lee/escribe cantidades del componente en archivo Excel. | [x] Planeada ☐ En desarrollo |
| 5 | Actualización interactiva | Botones (+1, −1, añadir cantidad) y reanudación de lectura. | [x] Planeada ☐ En desarrollo |

---

## 5. Compromiso del Estudiante

Declaro que:
- Entiendo los criterios de evaluación establecidos en las rúbricas.
- Presentaré una demostración funcional del proyecto.
- Defenderé el código que yo mismo implementé y explicaré las clases y métodos principales.
- Si usé herramientas de IA, comprendo su funcionamiento y las adapté al contexto del proyecto.

**Firma (nombre completo):** Christian Bony Negrete __________________________  

---

## 6. Validación del Docente *(completa el profesor)*

| Campo | Detalle |
|--------|---------|
| **Visto bueno del docente:** | ☐ Aprobado para desarrollar ☐ Requiere ajustes ☐ Rechazado |
| **Comentarios / Observaciones:** |  |
| **Firma docente:** |  |
| **Fecha de revisión:** |  |

---

> **Instrucciones para entrega:**
>
> - Completa todas las secciones antes de tu presentación inicial.  
> - No borres las casillas ni el formato para garantizar uniformidad del curso.  
> - El docente revisará y aprobará esta propuesta antes del desarrollo completo.




