# 🚢 Generador de Validación SIFAS Naval

![CONFIANZA23](skills/Logo_CONFIANZA23.png)

## 📝 Descripción
Herramienta de escritorio basada en web (Streamlit) diseñada para la generación de datos sintéticos de validación para el sistema **SIFAS Naval**. Permite a los analistas crear conjuntos de datos de buques basados en la plantilla oficial `Format.txt`, personalizando el número de registros y el rango de identificadores.

## 🚀 Características
- **Identidad Corporativa**: Interfaz oscura profesional siguiendo los estándares de **CONFIANZA23**.
- **Generación Realista**: Datos marítimos coherentes (nombres, banderas, coordenadas de mar abierto).
- **Multiformato**: Exportación inmediata a **CSV, Markdown, XML, JSON y TXT**.
- **Observabilidad**: Registro de logs detallado con `loguru` para depuración profesional.
- **Validación en Tiempo Real**: Visualización de métricas antes de exportar.

## 🛠️ Instalación

1.  Clona o descarga este repositorio.
2.  Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Uso

Ejecuta la aplicación rápidamente con:
```bash
build.cmd
```
O de forma manual:
```bash
streamlit run app.py
```

### Pasos:
1.  En la **barra lateral**, ajusta el número de buques deseado.
2.  Define el rango de IDs de inicio y fin.
3.  Haz clic en **"Generar Datos"**.
4.  Revisa los datos en la tabla principal y los logs en `debug.log`.
5.  Usa los botones de **"Exportar Resultados"** para descargar los datos.

## 📂 Estructura del Proyecto
- `app.py`: Lógica principal de la aplicación con logging integrado.
- `build.cmd`: Script de automatización para Windows.
- `Format.txt`: Plantilla base para la estructura de datos del buque.
- `requirements.txt`: Lista de dependencias de Python traducida.
- `skills_new/`: Estándares corporativos actualizados.

---
Desarrollado por **CONFIANZA23 Inteligencia y Seguridad, S.L.**
