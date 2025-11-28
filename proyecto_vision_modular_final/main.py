'''
La aplicación principal que integra todos los módulos para el sistema de inventario con visión 
por computadora.
    1.-Carga la configuración desde settings.py.
    2.-Inicializa la cámara, el modelo, el preprocesador, el repositorio de inventario y la UI 
    de detalle.
    3.-Crea el motor de inferencia y el controlador de la aplicación.
    4.-Arranca el bucle principal de la aplicación, manejando errores globales para evitar 
    fallos silenciosos.      
'''

from tkinter import Tk

from config.settings import (
    SAVEDMODEL_DIR,
    EXCEL_PATH,
    CAM_INDEX,
    FRAME_W,
    FRAME_H,
    INPUT_SIZE,
    THRESHOLD,
    NO_OBJECT_CLASS,
    CONFIRM_FRAMES,
    ensure_paths,
)
from core.inference.inference_engine import InferenceEngine, load_labels
from core.preprocessing.Tm_preprocessor import TMPreprocessor
from infrastructure.camera.opencv_camera import OpenCVCamera
from infrastructure.model.Tm_saved_model import TMSavedModel
from infrastructure.repo.excel_inventory_repo import ExcelInventoryRepo
from ui.tk_detail_ui import TkDetailUI
from app.controller import AppController


def main() -> None:
    try:
        ensure_paths()

        root = Tk()
        root.withdraw()

        camera = OpenCVCamera(index=CAM_INDEX, width=FRAME_W, height=FRAME_H)
        model = TMSavedModel(SAVEDMODEL_DIR)
        preprocessor = TMPreprocessor(INPUT_SIZE)
        repo = ExcelInventoryRepo(EXCEL_PATH)
        detail_ui = TkDetailUI(root=root, repo=repo)

        class_names = load_labels(SAVEDMODEL_DIR)
        engine = InferenceEngine(
            preprocessor=preprocessor,
            model=model,
            class_names=class_names,
        )

        valid_classes = set(class_names[:4])

        controller = AppController(
            camera=camera,
            engine=engine,
            ui=detail_ui,
            class_names=class_names,
            valid_classes=valid_classes,
            no_object_class=NO_OBJECT_CLASS,
            threshold=THRESHOLD,
            confirm_frames=CONFIRM_FRAMES,
        )

        controller.run(root)

    except Exception as e:
        print(f"[ERROR] Ha ocurrido un error en la aplicación principal: {e}")


if __name__ == "__main__":
    main()
