# Glosario — Curso de Filtros Bayesianos

Referencia de términos en inglés con sus definiciones en español
y notación matemática usada en todos los módulos.

## Términos en inglés

| Término (EN) | Definición (ES) | Módulo de primera aparición |
|---|---|---|
| prior | Distribución de probabilidad que representa el conocimiento antes de observar datos | M1 |
| posterior | Distribución actualizada tras incorporar una observación via el Teorema de Bayes | M1 |
| likelihood | Función de verosimilitud: P(observación \| estado); mide qué tan probable es la observación dado el estado | M1 |
| belief | Estado de conocimiento probabilístico actual sobre el sistema; distribución sobre estados posibles | M2 |
| predict | Paso de predicción del ciclo filtro: propaga la distribución un paso de tiempo hacia adelante | M2 |
| update | Paso de actualización: incorpora la observación más reciente para corregir la predicción | M2 |
| Kalman gain | Ganancia de Kalman K: peso óptimo que balancea predicción vs. observación en el filtro de Kalman | M3a |
| innovation | Innovación: diferencia entre la observación real y la observación predicha (z − H·x̂⁻) | M3a |
| sigma points | Puntos sigma: conjunto determinista de 2n+1 muestras que captura la media y covarianza de una distribución | M3c |
| ESS | Tamaño efectivo de muestra (Effective Sample Size): medida de degeneración del filtro de partículas; ESS = 1/Σwᵢ² | M4 |
| SIR | Muestreo por importancia con remuestreo (Sequential Importance Resampling): variante del filtro de partículas | M4 |
| RMSE | Raíz del error cuadrático medio (Root Mean Squared Error): métrica de precisión de estimación | Todos |
| NEES | Error cuadrático normalizado (Normalized Estimation Error Squared): métrica de consistencia de covarianza | M3a |

## Notación matemática

| Símbolo | Significado |
|---------|-------------|
| x̂ₖ | Estado estimado en el tiempo k |
| Pₖ | Covarianza del error de estimación en el tiempo k |
| x̂ₖ⁻ | Estado predicho (pre-actualización) en el tiempo k |
| Pₖ⁻ | Covarianza predicha (pre-actualización) en el tiempo k |
| zₖ | Observación en el tiempo k |
| F | Matriz de transición de estado (modelo lineal) |
| H | Matriz de observación (modelo lineal) |
| Q | Covarianza del ruido de proceso |
| R | Covarianza del ruido de medición |
| K | Ganancia de Kalman |
| f(·) | Función de transición de estado (modelo no lineal) |
| h(·) | Función de observación (modelo no lineal) |
| Jf | Jacobiano de f respecto al estado |
| Jh | Jacobiano de h respecto al estado |
| wᵢ | Peso de la partícula i en el filtro de partículas |
| N | Número de partículas (filtro de partículas) o número de estados (Bayes discreto) |
| α, β, κ | Parámetros del UKF: dispersión, distribución prior, escala secundaria |
