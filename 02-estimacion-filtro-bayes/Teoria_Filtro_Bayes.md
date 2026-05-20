# Módulo 2: Estimación de Estados y el Filtro de Bayes Recursivo

En el Módulo 1 vimos el Teorema de Bayes para una sola medición. Sin embargo, en el mundo real (como un robot moviéndose de manera continua), recibimos un **flujo constante de mediciones y realizamos acciones de control de manera secuencial**.

¿Cómo actualizamos nuestras creencias continuamente a lo largo del tiempo? La respuesta es el **Filtro de Bayes Recursivo**.

---

## 1. El Problema de la Estimación de Estados

El objetivo de la **Estimación de Estados** es inferir variables latentes (no observables directamente, como la posición exacta $(x, y, \theta)$ de un coche autónomo en un mapa) a partir de datos observados e imprecisos.

### Elementos Básicos del Sistema Dinámico
Definimos los siguientes términos en el tiempo $t$:

1.  **El Estado ($x_t$):**
    El vector de variables reales que describen el sistema en el instante $t$.
    *Ejemplo:* $x_t = [x, y, \dot{x}, \dot{y}]^T$ (posición y velocidad en 2D).
2.  **La Acción de Control ($u_t$):**
    La información sobre los comandos enviados a los actuadores o el cambio dinámico del sistema entre $t-1$ y $t$.
    *Ejemplo:* $u_t = [v, \omega]^T$ (velocidad lineal y velocidad angular comandadas).
3.  **La Medición ($z_t$):**
    Los datos obtenidos por los sensores en el instante $t$.
    *Ejemplo:* $z_t = [d_1, d_2]^T$ (distancias a dos balizas conocidas).

### Flujo de Información Temporal
A lo largo de la ejecución, acumulamos una historia de mediciones y controles:
$$d_{1:t} = \{ u_1, z_1, u_2, z_2, \dots, u_t, z_t \}$$

Nuestro objetivo es calcular la **creencia posterior** (denotada en la literatura como $\text{bel}(x_t)$) en el instante $t$:
$$\text{bel}(x_t) = p(x_t \mid z_{1:t}, u_{1:t})$$

También definimos la **creencia a priori** o predicción ($\overline{\text{bel}}(x_t)$) antes de incorporar la última medición $z_t$:
$$\overline{\text{bel}}(x_t) = p(x_t \mid z_{1:t-1}, u_{1:t})$$

---

## 2. La Suposición de Markov

Para hacer que el cálculo de $\text{bel}(x_t)$ sea computacionalmente viable en tiempo real, no podemos arrastrar toda la historia de datos $d_{1:t}$ que crece indefinidamente. Aquí entra la **Suposición de Markov**:

> [!IMPORTANT]
> **La Suposición de Markov** establece que el estado actual $x_t$ contiene **toda la información necesaria** sobre el pasado. Si conocemos el estado anterior $x_{t-1}$ y la acción de control actual $u_t$, el pasado completo ($x_{0:t-2}, z_{1:t-1}, u_{1:t-1}$) no aporta información adicional sobre el estado futuro $x_t$.
>
> Matemáticamente:
> 1.  **Transición de Estado:** $p(x_t \mid x_{t-1}, x_{0:t-2}, z_{1:t-1}, u_{1:t}) = p(x_t \mid x_{t-1}, u_t)$
> 2.  **Independencia del Sensor:** $p(z_t \mid x_t, x_{0:t-1}, z_{1:t-1}, u_{1:t}) = p(z_t \mid x_t)$

---

## 3. Derivación del Filtro de Bayes Recursivo

Bajo la suposición de Markov, podemos derivar la ecuación recursiva del Filtro de Bayes en dos pasos lógicos esenciales.

### Paso 1: Predicción (Actualización por Ley de Movimiento)
Queremos calcular la creencia a priori $\overline{\text{bel}}(x_t) = p(x_t \mid z_{1:t-1}, u_{1:t})$. 

Aplicando la **Ley de Probabilidad Total** (marginalizando sobre el estado anterior $x_{t-1}$):
$$p(x_t \mid z_{1:t-1}, u_{1:t}) = \int p(x_t, x_{t-1} \mid z_{1:t-1}, u_{1:t}) \, dx_{t-1}$$

Usando la regla del producto:
$$p(x_t, x_{t-1} \mid z_{1:t-1}, u_{1:t}) = p(x_t \mid x_{t-1}, z_{1:t-1}, u_{1:t}) \, p(x_{t-1} \mid z_{1:t-1}, u_{1:t})$$

Aplicando la suposición de Markov en el primer término ($p(x_t \mid x_{t-1}, u_t)$) y notando que $u_t$ no influye en la creencia del estado anterior $x_{t-1}$ en el segundo término:
$$\overline{\text{bel}}(x_t) = \int \underbrace{p(x_t \mid x_{t-1}, u_t)}_{\text{Modelo de Movimiento}} \, \underbrace{\text{bel}(x_{t-1})}_{\text{Posterior Anterior}} \, dx_{t-1}$$

> [!NOTE]
> Este paso propaga la creencia del robot a través del tiempo usando el modelo dinámico física del sistema. Dado que el movimiento tiene ruido, este paso típicamente **incrementa la incertidumbre** (la distribución de probabilidad se ensancha).

---

### Paso 2: Corrección / Actualización (Actualización por Sensor)
Queremos incorporar la nueva medición $z_t$ para obtener el posterior completo $\text{bel}(x_t) = p(x_t \mid z_{1:t}, u_{1:t})$.

Aplicando el **Teorema de Bayes** tomando $z_t$ como la nueva evidencia:
$$p(x_t \mid z_t, z_{1:t-1}, u_{1:t}) = \frac{p(z_t \mid x_t, z_{1:t-1}, u_{1:t}) \, p(x_t \mid z_{1:t-1}, u_{1:t})}{p(z_t \mid z_{1:t-1}, u_{1:t})}$$

Aplicando la suposición de Markov en la verosimilitud ($p(z_t \mid x_t)$):
$$\text{bel}(x_t) = \eta \, \underbrace{p(z_t \mid x_t)}_{\text{Modelo de Medida}} \, \underbrace{\overline{\text{bel}}(x_t)}_{\text{Creencia Predicha}}$$

Donde $\eta$ es el factor de normalización:
$$\eta = \frac{1}{p(z_t \mid z_{1:t-1}, u_{1:t})} = \frac{1}{\int p(z_t \mid x_t) \, \overline{\text{bel}}(x_t) \, dx_t}$$

> [!NOTE]
> Este paso utiliza la información del sensor para "corregir" la predicción del movimiento. Debido a que incorporamos nueva información observable, este paso típicamente **reduce la incertidumbre** (la distribución de probabilidad se vuelve más estrecha y concentrada).

---

## 4. Algoritmo General del Filtro de Bayes

El Filtro de Bayes es una plantilla conceptual abstracta. Se ejecuta recursivamente en cada ciclo:

```text
Algoritmo Filtro_Bayes_Recursivo( bel(x_{t-1}), u_t, z_t ):
    Para todos los estados x_t:
        // 1. Paso de Predicción (Chapman-Kolmogorov)
        bel_bar(x_t) = ∫ p(x_t | x_{t-1}, u_t) * bel(x_{t-1}) dx_{t-1}
        
        // 2. Paso de Corrección (Bayes)
        bel(x_t) = η * p(z_t | x_t) * bel_bar(x_t)
        
    retornar bel(x_t)
```

### Tipos de Filtros Derivados de esta Plantilla

Dependiendo de cómo representemos matemáticamente la distribución $\text{bel}(x)$, obtenemos diferentes filtros prácticos:

| Representación de la Creencia | Modelo de Transición/Medida | Filtro Resultante |
| :--- | :--- | :--- |
| **Grid Discreto** (Histograma) | No paramétrico arbitrario | **Filtro de Bayes Discreto** |
| **Campana Gaussiana** ($\mu, \mathbf{\Sigma}$) | Lineal + Ruido Gaussiano | **Filtro de Kalman (KF)** |
| **Campana Gaussiana** ($\mu, \mathbf{\Sigma}$) | No lineal linealizado localmente | **Extended Kalman (EKF)** |
| **Campana Gaussiana** ($\mu, \mathbf{\Sigma}$) | No lineal muestreado por puntos Sigma | **Unscented Kalman (UKF)** |
| **Nube de Partículas** (Muestras) | No paramétrico arbitrario | **Filtro de Partículas (PF)** |

---

## 5. Modelos en la Robótica Probabilística

Para implementar el Filtro de Bayes, necesitamos definir matemáticamente el modelo de movimiento ($p(x_t \mid x_{t-1}, u_t)$) y el modelo de medición ($p(z_t \mid x_t)$).

### Modelo de Movimiento Probabilístico
Describe cómo se desplaza físicamente el sistema.
En 1D, un modelo muy simple con control de velocidad $u_t = v_t$ y ruido de proceso Gaussiano $\epsilon_t \sim \mathcal{N}(0, \sigma_{\text{mov}}^2)$ se escribe como:
$$x_t = x_{t-1} + v_t \, \Delta t + \epsilon_t$$
Su densidad probabilística de transición es:
$$p(x_t \mid x_{t-1}, u_t) = \frac{1}{\sqrt{2\pi\sigma_{\text{mov}}^2}} \exp\left( -\frac{(x_t - (x_{t-1} + v_t\Delta t))^2}{2\sigma_{\text{mov}}^2} \right)$$

### Modelo de Medición Probabilístico
Describe la física y el ruido del sensor.
Si el sensor mide la distancia directa a una baliza situada en la coordenada fija $L$, con ruido de medición Gaussiano $\delta_t \sim \mathcal{N}(0, \sigma_{\text{sen}}^2)$:
$$z_t = |x_t - L| + \delta_t$$
La verosimilitud de la medición es:
$$p(z_t \mid x_t) = \frac{1}{\sqrt{2\pi\sigma_{\text{sen}}^2}} \exp\left( -\frac{(z_t - |x_t - L|)^2}{2\sigma_{\text{sen}}^2} \right)$$

---

En la **Práctica 2 (`Practica_Filtro_Bayes.ipynb`)**, programaremos un **Filtro de Bayes Discreto (Localización por Rejilla o Grid Localization)** desde cero en 1D. Veremos cómo un robot puede localizarse en un pasillo largo combinando un odómetro ruidoso con lecturas imprecisas del sensor al cruzar puertas.
