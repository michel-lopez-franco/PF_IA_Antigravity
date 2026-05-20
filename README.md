# Curso de Probabilidad y Estadística Aplicada: De 0 a Pro en Filtros Bayesianos y de Partículas

Este repositorio contiene un curso de nivel profesional diseñado para llevar a estudiantes de ingeniería, robótica y ciencia de datos desde los conceptos fundamentales de la probabilidad y estadística hasta el dominio práctico y avanzado de la estimación de estados mediante **Filtros Bayesianos** y **Filtros de Partículas**.

---

## 🗺️ Mapa de Ruta del Curso (Curriculum)

El curso está organizado de manera modular y secuencial. Cada módulo cuenta con una sólida base teórica en formato Markdown (`.md`) con explicaciones matemáticas rigurosas y fórmulas en LaTeX, complementada por una libreta interactiva en Jupyter Notebook (`.ipynb`) implementada desde cero con simulaciones interactivas utilizando Python.

```text
PF_IA_Antigravity/
├── README.md                           # 📖 Guía principal del curso
├── 01-fundamentos-probabilidad/        # 🧮 MÓDULO 1: Fundamentos Estadísticos
│   ├── Teoria_Probabilidad.md          # Variable aleatoria, covarianza, campana de Gauss, Teorema de Bayes
│   └── Practica_Fundamentos.ipynb      # Interactividad Bayesiana y multiplicación de Gaussianas 1D/2D
├── 02-estimacion-filtro-bayes/         # ⏱️ MÓDULO 2: Estimación de Estados Recursiva
│   ├── Teoria_Filtro_Bayes.md          # Supuesto de Markov, Chapman-Kolmogorov, actualización del sensor
│   └── Practica_Filtro_Bayes.ipynb     # Grid Localization (Localización por Rejilla en pasillo 1D circular)
├── 03-filtros-kalman/                  # 📐 MÓDULO 3: Filtros Lineales y Gaussianos
│   ├── Teoria_Kalman.md                # Filtro de Kalman Lineal (KF), Extendido (EKF) y Unscented (UKF)
│   └── Practica_Kalman.ipynb           # Tracking 2D de proyectil y comparación EKF vs UKF en radar no lineal
├── 04-filtro-particulas/               # 🌪️ MÓDULO 4: Filtros No-Gaussianos y No-Lineales
│   ├── Teoria_Particulas.md            # Monte Carlo, Importance Sampling, remuestreo sistemático
│   └── Practica_Particulas.ipynb       # Simulación 2D de localización de robot con landmarks (MCL de 1000 partículas)
└── 05-pro-avanzado/                     # 🚀 MÓDULO 5: Nivel Pro & Proyectos
    ├── Teoria_Temas_Avanzados.md       # Filtros Rao-Blackwellizados (FastSLAM), KLD-Sampling, Robot Secuestrado
    └── Practica_Proye_Integrador.ipynb # CAPSTONE PROJECT: Localización y recuperación ante secuestro en laberinto 2D
```

---

## 🛠️ Instalación de Dependencias y Requisitos

Para poder ejecutar las libretas interactivas en tu máquina local, necesitarás tener instalado **Python 3.10+** y los siguientes paquetes científicos.

### 1. Clonar el repositorio
Abre una terminal y colócate en la ruta del espacio de trabajo:
```bash
cd /home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity
```

### 2. Crear y activar un entorno virtual (Recomendado)
```bash
python3 -m venv env_filtros
source env_filtros/activate
```

### 3. Instalar librerías clave
Instala las librerías matemáticas y de visualización necesarias mediante `pip`:
```bash
pip install --upgrade pip
pip install numpy scipy matplotlib ipywidgets jupyter
```

### 4. Lanzar Jupyter Lab/Notebook
Para visualizar y ejecutar las prácticas interactivas con deslizadores (`ipywidgets`):
```bash
jupyter notebook
```

---

## 📚 Enlaces Rápidos a los Materiales del Curso

### 🧮 [Módulo 1: Fundamentos de Probabilidad](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/01-fundamentos-probabilidad/Teoria_Probabilidad.md)
*   **Contenido Teórico:** Variables aleatorias continuas/discretas, esperanza, covarianza, matrices de covarianza, distribuciones Gaussianas multivariadas y Teorema de Bayes en profundidad.
*   **Práctica:** [Practica_Fundamentos.ipynb](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/01-fundamentos-probabilidad/Practica_Fundamentos.ipynb) (Simuladores interactivos de contorno de Gaussiana 2D, Teorema de Bayes en barras y Fusión de Gaussianas).

### ⏱️ [Módulo 2: Estimación de Estados y Filtro de Bayes](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/02-estimacion-filtro-bayes/Teoria_Filtro_Bayes.md)
*   **Contenido Teórico:** Definición formal del problema de estimación, suposición de Markov, derivación de predicción y corrección y la plantilla conceptual del Filtro de Bayes.
*   **Práctica:** [Practica_Filtro_Bayes.ipynb](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/02-estimacion-filtro-bayes/Practica_Filtro_Bayes.ipynb) (Implementación desde cero de un localizador 1D Grid en un pasillo circular ruidoso con puertas).

### 📐 [Módulo 3: Filtros de Kalman (KF, EKF, UKF)](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/03-filtros-kalman/Teoria_Kalman.md)
*   **Contenido Teórico:** Derivación analítica del Filtro de Kalman Lineal. Linealización de primer orden y Jacobianos para el EKF. Puntos Sigma y Transformación Unscented para el UKF.
*   **Práctica:** [Practica_Kalman.ipynb](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/03-filtros-kalman/Practica_Kalman.ipynb) (Seguimiento 2D de proyectiles y comparación directa del error y convergencia de EKF vs UKF en radar no lineal).

### 🌪️ [Módulo 4: Filtros de Partículas (SIR)](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/04-filtro-particulas/Teoria_Particulas.md)
*   **Contenido Teórico:** Concepto de Monte Carlo, Muestreo por Importancia (Importance Sampling), el problema del empobrecimiento y el número efectivo de partículas, y la rueda de remuestreo sistemático.
*   **Práctica:** [Practica_Particulas.ipynb](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/04-filtro-particulas/Practica_Particulas.ipynb) (Localización Global de un Robot en una arena con balizas de landmarks utilizando una nube de 1000 partículas interactivas).

### 🚀 [Módulo 5: Nivel Avanzado y Proyecto Integrador](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/05-pro-avanzado/Teoria_Temas_Avanzados.md)
*   **Contenido Teórico:** Reducción de la dimensionalidad con Filtros de Partículas Rao-Blackwellizados (FastSLAM), muestreo adaptativo inteligente con KLD-Sampling, y MCL adaptativo para mitigar secuestros.
*   **Práctica (Proyecto Integrador):** [Practica_Proye_Integrador.ipynb](file:///home/michel/Documents/CUCEI_2026A/2_PF/PF_IA_Antigravity/05-pro-avanzado/Practica_Proye_Integrador.ipynb) (Programación de un robot diferencial ruidoso con LIDAR y colisiones físicas en un laberinto. Simulación de secuestro y relocalización adaptativa en tiempo real).

---

## ⚡ Filosofía del Código de este Curso
1.  **Caja Negra Prohibida:** Ninguno de los algoritmos del curso utiliza librerías de estimación externas prefabricadas (como `filterpy`). Todas las ecuaciones y filtros (KF, EKF, UKF, SIR PF) están programados desde cero usando operaciones de matrices puras en `NumPy`. Esto garantiza que entiendas la matemática exacta detrás de cada línea de código.
2.  **Interactividad como Prioridad:** Se hace un uso intensivo de animaciones en tiempo real y componentes interactivos para facilitar el aprendizaje intuitivo y el análisis de la sensibilidad de los parámetros (p. ej., variando el ruido de proceso/medición con deslizadores).
3.  **Estilo Premium y Limpio:** Todo el código sigue los estándares de calidad de Python, con nombres descriptivos de variables y comentarios pedagógicos exhaustivos.
