# CONTROL DE SISTEMA // AUTO_SHUTDOWN

> **ESTADO:** OPERATIVO
> **VERSIÓN:** 1.0.0
> **TEMA:** HACKER / MATRIX DARK

## /DESCRIPCIÓN GENERAL
**AutoShutdown** es una aplicación para Windows diseñada para gestionar el apagado automático de tu PC de forma precisa y con estilo. Con una interfaz estética "Hacker", te permite programar el apagado mediante un temporizador regresivo o fijando una hora exacta.

## /CARACTERÍSTICAS
*   **[ EJECUTAR ]** Inicia la secuencia de apagado programada.
*   **[ MODOS ]**
    *   `>> CUENTA REGRESIVA`: Establece horas y minutos hasta el apagado.
    *   `>> HORA EXACTA`: Programa el apagado a una hora específica del reloj (formato 24h).
*   **[ ABORTAR ]** Cancela inmediatamente cualquier secuencia de apagado activa.
*   **[ SEGURIDAD ]** Sistema de alertas visuales y ventana emergente que se activa 60 segundos antes de la terminación para evitar apagados accidentales.
*   **[ PORTABLE ]** Archivo `.exe` único que no requiere instalación. Llévalo en tu USB.

## /INSTALACIÓN Y USO
### Opción 1: Ejecutable (Recomendado)
1.  Ve a la carpeta `dist/`.
2.  Haz doble clic en `AutoShutdown_Hacker.exe`.
3.  ¡Listo! No necesitas instalar nada más.

### Opción 2: Ejecutar código fuente (Para desarrolladores)
1.  **Clonar el repositorio:**
    ```bash
    git clone <url_del_repositorio>
    ```
2.  **Instalar dependencias:**
    Asegúrate de tener Python instalado y ejecuta:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Iniciar la aplicación:**
    ```bash
    python main.py
    ```

## /COMPILAR_EJECUTABLE
Si modificas el código y quieres generar tu propio `.exe`:
```bash
pyinstaller --noconfirm --onefile --windowed --name "AutoShutdown_Hacker" --hidden-import "customtkinter" --collect-all "customtkinter" "main.py"
```

## /TECNOLOGÍAS
*   **Python 3.x**: Lógica del núcleo.
*   **CustomTkinter**: Interfaz gráfica moderna y personalizable.
*   **PyInstaller**: Compilador para crear el ejecutable standalone.

---
*PRECAUCIÓN: EL APAGADO DEL SISTEMA ES FINAL. GUARDA TU TRABAJO ANTES DE ACTIVAR.*
author: Jeanpa
