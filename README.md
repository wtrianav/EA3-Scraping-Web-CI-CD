# Evidencia de Aprendizaje 3: Optimización de Procesos de Desarrollo (CI/CD y Despliegue en la Nube)

## 1. Introducción
Este proyecto da continuidad a las Evidencias de Aprendizaje 1 y 2 del curso **Programación para Análisis de Datos** (Ingeniería de Software y Datos, Institución Universitaria Digital de Antioquia). Integra la extracción automatizada de datos (*web scraping*) del portal de comercio electrónico *Books to Scrape* con una aplicación web interactiva, pruebas unitarias automatizadas y un pipeline completo de Integración Continua y Despliegue Continuo (CI/CD) mediante **GitHub Actions** y **GitHub Pages**.

## 2. Estructura del Proyecto
```text
.
├── .github/
│   └── workflows/
│       └── ci_cd_deploy.yml   # Pipeline de CI/CD y despliegue en GitHub Pages
├── tests/
│   └── test_app.py            # Pruebas unitarias automatizadas con pytest
├── scraper.py                 # Módulo de extracción de datos (BeautifulSoup)
├── build_web.py               # Generador de la aplicación web (dist/index.html)
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación técnica del repositorio
```

## 3. Instalación
1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/wtrianav/EA3-Scraping-Web-CI-CD.git
   cd EA3-Scraping-Web-CI-CD
   ```
2. Crea y activa un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 4. Uso
- **Ejecutar pruebas unitarias:**
  ```bash
  pytest -v tests/test_app.py
  ```
- **Ejecutar el scraper y generar la aplicación web localmente:**
  ```bash
  python build_web.py
  ```
  Esto generará los archivos `libros.csv`, `libros.json` y la aplicación web en `dist/index.html`, la cual puedes abrir directamente en cualquier navegador.

## 5. Automatización (GitHub Actions)
El flujo de trabajo definido en `.github/workflows/ci_cd_deploy.yml` automatiza el ciclo de vida completo:
- **Disparadores (`on`):** Se ejecuta automáticamente ante cualquier `push` a `main` o `dev`, en `pull_request` hacia `main`, de forma programada diariamente a las 08:00 UTC (`cron`) y bajo demanda (`workflow_dispatch`).
- **Variables de entorno (`env`):** Configura `PYTHON_VERSION`, `TARGET_URL` y `MAX_ITEMS`.
- **Job `build-and-test` (CI):** Descarga el código, configura Python, instala dependencias, ejecuta las pruebas con `pytest`, corre `build_web.py` y almacena los datasets como artefactos descargables (`actions/upload-artifact@v4`).

## 6. Despliegue (GitHub Pages)
El despliegue continuo (CD) se ejecuta en el job `deploy` únicamente cuando los cambios llegan a la rama `main` y todas las pruebas unitarias han sido aprobadas:
1. El job `build-and-test` empaqueta la carpeta `./dist` usando `actions/upload-pages-artifact@v3`.
2. El job `deploy` publica automáticamente el sitio en el servicio de alojamiento en la nube **GitHub Pages** mediante `actions/deploy-pages@v4`.
3. **URL de producción:** `https://wtrianav.github.io/EA3-Scraping-Web-CI-CD/`
