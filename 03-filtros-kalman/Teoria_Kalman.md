# Módulo 3: Filtros de Kalman (Lineal, Extendido y Unscented)

Cuando el espacio de estados de nuestro Filtro de Bayes es **continuo** y podemos suponer que la incertidumbre es **Gaussiana**, el Filtro de Bayes Recursivo puede resolverse de forma analítica exacta y extremadamente eficiente. Esta familia de estimadores se conoce como **Filtros de Kalman**.

---

## 1. El Filtro de Kalman Lineal (KF)

El **Filtro de Kalman Lineal** asume que las transiciones de estado del sistema y los modelos de sensor son **transformaciones lineales** de las variables de estado, y que todos los ruidos de proceso y de medición siguen distribuciones Gaussianas de media cero.

### Representación del Estado
La creencia $\text{bel}(x_t)$ se representa completamente por:
*   La media $\mathbf{x}_t \in \mathbb{R}^n$ (nuestra mejor estimación del estado).
*   La matriz de covarianza $\mathbf{P}_t \in \mathbb{R}^{n \times n}$ (nuestra incertidumbre).

### Las Ecuaciones del Sistema Lineal
El estado y las mediciones se modelan como:
$$\mathbf{x}_t = \mathbf{F}_t \mathbf{x}_{t-1} + \mathbf{B}_t \mathbf{u}_t + \mathbf{w}_t$$
$$\mathbf{z}_t = \mathbf{H}_t \mathbf{x}_t + \mathbf{v}_t$$

Donde:
*   $\mathbf{F}_t$: Matriz de transición de estado (física del sistema).
*   $\mathbf{B}_t$: Matriz de entrada de control.
*   $\mathbf{H}_t$: Matriz de medición (cómo se relaciona el estado con la lectura física).
*   $\mathbf{w}_t \sim \mathcal{N}(0, \mathbf{Q}_t)$: Ruido de proceso (incertidumbre del modelo, ej. ráfagas de viento).
*   $\mathbf{v}_t \sim \mathcal{N}(0, \mathbf{R}_t)$: Ruido de medición (ruido propio del sensor).

---

### Ecuaciones del Filtro de Kalman (Algoritmo Completo)

En cada paso temporal, el Filtro de Kalman ejecuta un ciclo cerrado de dos fases:

#### 1. Fase de Predicción (Propagar el Estado)
Proyectamos la estimación de estado y su incertidumbre hacia adelante en el tiempo:
$$\overline{\mathbf{x}}_t = \mathbf{F}_t \mathbf{x}_{t-1} + \mathbf{B}_t \mathbf{u}_t$$
$$\overline{\mathbf{P}}_t = \mathbf{F}_t \mathbf{P}_{t-1} \mathbf{F}_t^T + \mathbf{Q}_t$$

> [!TIP]
> Observa cómo sumamos $\mathbf{Q}_t$. Si el robot se mueve sin medir, nuestra incertidumbre $\overline{\mathbf{P}}_t$ crece invariablemente.

#### 2. Fase de Corrección / Actualización (Fusión del Sensor)
Ajustamos nuestra estimación basándonos en la nueva medición $\mathbf{z}_t$:

*   **Innovación o Residuo ($\mathbf{y}_t$):** La diferencia entre la medición real y la que esperábamos medir.
    $$\mathbf{y}_t = \mathbf{z}_t - \mathbf{H}_t \overline{\mathbf{x}}_t$$
*   **Covarianza de la Innovación ($\mathbf{S}_t$):** La incertidumbre combinada del sensor y de nuestra predicción.
    $$\mathbf{S}_t = \mathbf{H}_t \overline{\mathbf{P}}_t \mathbf{H}_t^T + \mathbf{R}_t$$
*   **Ganancia de Kalman ($\mathbf{K}_t$):** El peso óptimo que asignamos a la medición.
    $$\mathbf{K}_t = \overline{\mathbf{P}}_t \mathbf{H}_t^T \mathbf{S}_t^{-1}$$
*   **Actualización del Estado posterior ($\mathbf{x}_t$):**
    $$\mathbf{x}_t = \overline{\mathbf{x}}_t + \mathbf{K}_t \mathbf{y}_t$$
*   **Actualización de la Covarianza posterior ($\mathbf{P}_t$):**
    $$\mathbf{P}_t = (\mathbf{I} - \mathbf{K}_t \mathbf{H}_t) \overline{\mathbf{P}}_t$$

---

## 2. El Filtro de Kalman Extendido (EKF)

En el mundo real, los sistemas casi nunca son lineales. Por ejemplo, un robot diferencial utiliza trigonometría para su cinemática (funciones $\sin\theta$, $\cos\theta$). Para estos casos no lineales, el KF lineal falla porque la transformación de una gaussiana a través de una función no lineal **deja de ser gaussiana**.

```
Distribución Gaussiana ---> [ Función Lineal ] ------> Distribución Gaussiana (KF)
Distribución Gaussiana ---> [ Función No-Lineal ] ---> Distribución NO Gaussiana ⚠️
```

El **Filtro de Kalman Extendido (EKF)** soluciona esto linealizando localmente la no linealidad mediante una **aproximación de Taylor de primer orden** en el punto de la estimación actual.

### Ecuaciones de Sistema No Lineales
$$\mathbf{x}_t = g(\mathbf{x}_{t-1}, \mathbf{u}_t) + \mathbf{w}_t$$
$$\mathbf{z}_t = h(\mathbf{x}_t) + \mathbf{v}_t$$

Donde $g$ y $h$ son funciones no lineales arbitrarias.

### Linealización mediante Matrices Jacobianas
Para propagar la covarianza, linealizamos las funciones calculando sus derivadas parciales de primer orden, llamadas **Matrices Jacobianas**:

$$\mathbf{G}_t = \frac{\partial g(\mathbf{x}, \mathbf{u})}{\partial \mathbf{x}} \Bigg|_{\mathbf{x} = \mathbf{x}_{t-1}}$$
$$\mathbf{H}_t = \frac{\partial h(\mathbf{x})}{\partial \mathbf{x}} \Bigg|_{\mathbf{x} = \overline{\mathbf{x}}_t}$$

### Ecuaciones del Algoritmo EKF

#### Predicción:
$$\overline{\mathbf{x}}_t = g(\mathbf{x}_{t-1}, \mathbf{u}_t)$$
$$\overline{\mathbf{P}}_t = \mathbf{G}_t \mathbf{P}_{t-1} \mathbf{G}_t^T + \mathbf{Q}_t$$

#### Corrección:
$$\mathbf{y}_t = \mathbf{z}_t - h(\overline{\mathbf{x}}_t)$$
$$\mathbf{S}_t = \mathbf{H}_t \overline{\mathbf{P}}_t \mathbf{H}_t^T + \mathbf{R}_t$$
$$\mathbf{K}_t = \overline{\mathbf{P}}_t \mathbf{H}_t^T \mathbf{S}_t^{-1}$$
$$\mathbf{x}_t = \overline{\mathbf{x}}_t + \mathbf{K}_t \mathbf{y}_t$$
$$\mathbf{P}_t = (\mathbf{I} - \mathbf{K}_t \mathbf{H}_t) \overline{\mathbf{P}}_t$$

> [!WARNING]
> Si la no linealidad del sistema es muy fuerte o el intervalo de muestreo es grande, la linealización de primer orden del EKF introduce errores severos, lo que puede provocar que el filtro **diverja** catastróficamente.

---

## 3. El Filtro de Kalman Unscented (UKF)

El **Filtro de Kalman Unscented (UKF)** aborda el problema de la no linealidad de manera radicalmente distinta: en lugar de aproximar la función no lineal (linealizándola con Jacobianos), aproximamos la distribución de probabilidad misma.

> [!TIP]
> *"Es más fácil aproximar una distribución de probabilidad que aproximar una función no lineal arbitraria."* - Julier & Uhlmann.

El UKF utiliza la **Transformación Unscented**. Selecciona un conjunto pequeño y determinista de puntos de muestra, llamados **Puntos Sigma ($\mathcal{X}$)**, que capturan perfectamente la media y la covarianza de la gaussiana original.

```
       Puntos Sigma para aproximar la distribución de forma no lineal:
       
                * (Punto Sigma 1)
              /   \
             /     \
(Media) *---*-------*---* (Punto Sigma 2)
             \     /
              \   /
                * (Punto Sigma 3)
```

### El Proceso de la Transformación Unscented
1.  **Generación de Puntos Sigma ($2n + 1$ puntos):**
    Donde $n$ es la dimensión del estado. Los puntos se colocan en la media y a lo largo de las direcciones de los vectores propios de la matriz de covarianza:
    $$\mathcal{X}_0 = \mathbf{x}$$
    $$\mathcal{X}_i = \mathbf{x} + \left( \sqrt{(n + \lambda) \mathbf{P}} \right)_i \quad \text{para } i = 1, \dots, n$$
    $$\mathcal{X}_i = \mathbf{x} - \left( \sqrt{(n + \lambda) \mathbf{P}} \right)_{i-n} \quad \text{para } i = n+1, \dots, 2n$$
    *(Donde $\lambda$ es un parámetro de escala de dispersión).*
2.  **Propagación No Lineal:**
    Hacemos pasar cada punto sigma individual a través de la función no lineal *real* sin ninguna simplificación:
    $$\mathcal{Y}_i = f(\mathcal{X}_i)$$
3.  **Cálculo de la Nueva Media y Covarianza:**
    Calculamos la media predicha y la covarianza ponderando los puntos sigma resultantes. Esto proporciona una precisión de hasta **segundo orden en la expansión de Taylor** para la media y covarianza, superando drásticamente al EKF.

---

### Tabla Comparativa: EKF vs UKF

| Característica | Extended Kalman Filter (EKF) | Unscented Kalman Filter (UKF) |
| :--- | :--- | :--- |
| **Complejidad Matemática** | Requiere derivar matrices Jacobianas a mano o numéricamente. | No requiere derivadas. Es algebraico. |
| **Precisión de Linealización** | Primer orden de Taylor (menor precisión). | Segundo orden o superior (alta precisión). |
| **Carga Computacional** | Baja (muy rápida). | Moderada (requiere propagar $2n+1$ puntos). |
| **Robustez ante No Linealidades** | Sensible a la divergencia. | Altamente robusto y convergente. |

---

En la **Práctica 3 (`Practica_Kalman.ipynb`)**, programaremos desde cero un **Filtro de Kalman Lineal 2D** para el seguimiento de la trayectoria de un proyectil, e implementaremos y compararemos un **EKF** frente a un **UKF** para resolver el problema de la localización no lineal usando landmarks y rangos de sensores.
