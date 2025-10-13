Propuesta Inicial de Proyecto

Carrera: Ing. Mecatronica
Materia: Programacion Superior
Periodo: Segundo Parcial / Proyecto Final
Estudiante(s): Christian Bony Negrete Pedraza
Fecha de entrega: 2025-10-13


---

1. Datos Generales del Proyecto

Campo	Descripción

Nombre del proyecto:	ElectroVision Pro – Inventario Cloud (POO)
Tipo de aplicación:	☑ Escritorio ☐ Web ☐ Móvil ☐ Otro: __________
Lenguaje / entorno de desarrollo:	Python 3.11 (Tkinter, OpenCV, TensorFlow, Pandas, OpenPyXL, gspread, google-auth, python-dotenv)
Repositorio Git (opcional):	(agregar enlace cuando se cree)
Uso de Inteligencia Artificial:	☑ Sí (el proyecto completo usa CNN propias; en Programación II solo se implementa el módulo de inventario en la nube con POO)


Si usas IA, explica brevemente cómo y en qué etapa contribuye:

> Las CNN de reconocimiento de componentes y resistencias ya están integradas. En Programación II me enfoco exclusivamente en la capa de inventario en la nube (POO), sin modificar ni reentrenar los modelos. Puedo apoyarme en IA para generar esqueletos de clases/boilerplate, que adapto y comprendo.




---

2. Descripción del Proyecto

Resumen breve

Módulo de inventario compartido para ElectroVision Pro diseñado con POO. La GUI de la app actual (que reconoce componentes y lee resistencias) actualizará cantidades mediante un Repositorio que escribe/lee en Google Sheets (fuente de verdad) con Excel local como respaldo. Además, se añade exportación a JSON. Todo se hace con contratos e implementaciones intercambiables para facilitar mantenimiento y pruebas.

Objetivos principales

1. Implementar InventoryRepository (orquestador) y StorageStrategy (contrato) con GoogleSheetsStore y LocalExcelStore.


2. Integrar la GUI: botones +1/−1/Set y Exportar JSON usando solo el repositorio.


3. Asegurar funcionamiento robusto: latencia ≤ 3 s/operación, consistencia de datos y fallback local.




---

3. Diseño Técnico y Aplicación de POO

Principios de POO aplicados

Marca los que planeas usar:

[x] Encapsulamiento (atributos privados y métodos públicos)

[x] Uso de constructores

[x] Herencia

[x] Polimorfismo

[x] Interfaces o clases abstractas


Clases estimadas

Cantidad inicial de clases: 5

Ejemplo de posibles clases:

StorageStrategy (ABC) – contrato de almacenamiento

GoogleSheetsStore – implementación cloud

LocalExcelStore – implementación Excel local (fallback)

InventoryRepository – orquesta backend y exporta JSON

Wiring/Config – ensambla repositorio desde variables .env



Persistencia de datos

[x] Archivos locales (Excel como respaldo, JSON exportado)

[ ] Base de datos

[x] En memoria (temporal en ejecución)

[x] Otro: Google Sheets (cloud) via API



---

4. Funcionalidades Principales

Nº	Nombre de la funcionalidad	Descripción breve	Estado actual

1	Repositorio de Inventario	InventoryRepository expone get_qty/set_qty/add_qty/fetch_all/export_json	☐ Planeada ☑ En desarrollo
2	Estrategia Google Sheets	GoogleSheetsStore como fuente de verdad (CRUD y updated_at)	☐ Planeada ☑ En desarrollo
3	Fallback Excel local	LocalExcelStore (Pandas/OpenPyXL) para operar sin red	☐ Planeada ☑ En desarrollo
4	Integración GUI	Botones +1/−1/Set y Exportar JSON usando solo el repositorio	☐ Planeada ☑ En desarrollo
5	Configuración por .env	IDs de hoja y credenciales de Service Account (dotenv)	☐ Planeada ☑ En desarrollo


> (Se pueden agregar pruebas unitarias del repositorio como funcionalidad adicional.)




---

5. Compromiso del Estudiante

Declaro que:

Entiendo los criterios de evaluación establecidos en las rúbricas.

Presentaré una demostración funcional del módulo de inventario en la nube integrado a la GUI existente.

Defenderé el código implementado y explicaré las clases y métodos principales (Repository, Strategy e integración).

Si usé herramientas de IA, comprendo su funcionamiento y adapté el código al contexto del proyecto.


Firma (nombre completo): __________________________


---

6. Validación del Docente (completa el profesor)

Campo	Detalle

Visto bueno del docente:	☐ Aprobado para desarrollar ☐ Requiere ajustes ☐ Rechazado
Comentarios / Observaciones:	
Firma docente:	
Fecha de revisión:	



---

> Instrucciones para entrega:

Completa todas las secciones antes de tu presentación inicial.

No borres las casillas ni el formato para garantizar uniformidad del curso.

El docente revisará y aprobará esta propuesta antes del desarrollo completo.




