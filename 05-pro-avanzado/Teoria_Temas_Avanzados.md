# Módulo 5: Temas Avanzados y Aplicaciones de Filtros Bayesianos (Nivel Pro)

¡Felicidades por llegar hasta aquí! Has dominado la teoría y la práctica de los Filtros de Kalman y los Filtros de Partículas estándar. En este módulo final, daremos el paso definitivo al **Nivel Pro**, explorando las optimizaciones avanzadas y las aplicaciones de vanguardia que se utilizan en la industria aeroespacial, la robótica de servicio y los vehículos autónomos.

---

## 1. Filtros de Partículas Rao-Blackwellizados (RBPF)

Uno de los principales problemas del Filtro de Partículas es la **Maldición de la Dimensionalidad**. A medida que aumenta el número de variables de estado que queremos estimar, el número de partículas requerido para cubrir el espacio crece de forma **exponencial**.

*Ejemplo:* Si localizamos un robot en 2D $(x, y)$, 200 partículas pueden bastar. Pero si queremos estimar la posición de la cabeza, el brazo, el torso y 50 landmarks del mapa simultáneamente, necesitaríamos millones de partículas, haciendo que el sistema sea impracticable en tiempo real.

> [!IMPORTANT]
> **Rao-Blackwellización** es una técnica estadística que reduce la dimensionalidad de un estimador Monte Carlo analizando qué partes del estado pueden resolverse analíticamente mediante filtros exactos (como el Filtro de Kalman).
>
> *"Marginamos analíticamente las variables que son lineales y gaussianas dado el resto de variables no lineales."*

### Aplicación en Robótica: El Concepto de FastSLAM
En el problema de SLAM (Localización y Mapeo Simultáneos), queremos estimar la posición del robot $\mathbf{s}_t$ y la posición de $N$ landmarks del mapa $\boldsymbol{\Theta} = \{\theta_1, \theta_2, \dots, \theta_N\}$. El estado total tiene dimensión $3 + 2N$.

FastSLAM (basado en RBPF) factoriza el posterior de la siguiente forma:
$$p(\mathbf{s}_{0:t}, \boldsymbol{\Theta} \mid \mathbf{z}_{1:t}, \mathbf{u}_{1:t}) = \underbrace{p(\mathbf{s}_{0:t} \mid \mathbf{z}_{1:t}, \mathbf{u}_{1:t})}_{\text{Filtro de Partículas para la Trayectoria}} \, \prod_{i=1}^N \underbrace{p(\theta_i \mid \mathbf{s}_{0:t}, \mathbf{z}_{1:t})}_{\text{EKF individuales para cada Landmark}}$$

*   **La trayectoria del robot** es altamente no lineal y no gaussiana $\rightarrow$ Se estima con un **Filtro de Partículas**.
*   **La posición de cada Landmark**, *dada la trayectoria del robot*, se convierte en un problema lineal e independiente $\rightarrow$ Se estima analíticamente con un **Filtro de Kalman Extendido (EKF)** individual de $2 \times 2$ por cada landmark.

¡Esto reduce la complejidad de $\mathcal{O}(N^3)$ a $\mathcal{O}(M \log N)$, permitiendo mapear entornos masivos en tiempo real!

---

## 2. Muestreo Adaptativo KLD-Sampling

En un Filtro de Partículas convencional, el número de partículas $M$ es fijo (ej. 1000 partículas). Esto representa un desperdicio masivo de procesador en dos situaciones opuestas:

1.  **Robot bien localizado:** Si la nube de partículas está sumamente compactada en una zona de $10\text{ cm}^2$, no tiene sentido evaluar 1000 hipótesis idénticas. Con 40 partículas tendríamos la misma precisión.
2.  **Secuestro del robot (Incertidumbre global):** Si el robot se desplaza repentinamente a un punto desconocido (o se enciende desde cero), 1000 partículas pueden ser insuficientes para cubrir un mapa de $200\text{ m}^2$, provocando que el filtro nunca converja.

> [!TIP]
> **KLD-Sampling (Kullback-Leibler Divergence Sampling)** es un algoritmo que **adapta dinámicamente el número de partículas $M_t$** en cada paso del bucle.
>
> Mide la distancia estadística (divergencia KL) entre la distribución continua real y la aproximación por histograma discreto de las partículas actuales.

```
Poco Localizado (M = 3000 partículas)       Muy Localizado (M = 80 partículas)
                                                       
   .   .  *  .   :                                    \  |  /
 .   *   .  *  .  *  .                                  *-*-*
   :   .  *  .   .                                    /  |  \
```

El algoritmo detiene la generación de partículas durante el remuestreo tan pronto como el error de aproximación cae por debajo de un umbral $\epsilon$:
$$M_t = \frac{k - 1}{2\epsilon} \left( 1 - \frac{2}{9(k - 1)} + z_{1-\delta} \sqrt{\frac{2}{9(k - 1)}} \right)^3$$

Donde $k$ es el número de celdas del histograma que contienen al menos una partícula, y $z_{1-\delta}$ es el cuantil de la distribución normal estándar.
*   **Si las partículas están dispersas** $\rightarrow$ ocupan muchas celdas diferentes $\rightarrow k$ es alto $\rightarrow M_t$ aumenta automáticamente.
*   **Si las partículas están agrupadas** $\rightarrow$ ocupan muy pocas celdas $\rightarrow k$ es bajo $\rightarrow M_t$ disminuye drásticamente, ahorrando hasta un $90\%$ de capacidad de cómputo.

---

## 3. El Problema del Secuestro del Robot (Kidnapped Robot)

Un reto clásico en robótica autónoma es el **Secuestro del Robot**: el robot está bien localizado y, de repente, un humano lo levanta y lo traslada a otra habitación sin avisarle.
*   **Filtro estándar:** Todas las partículas se encuentran agrupadas en la habitación antigua. Dado que el sensor ahora lee cosas completamente distintas, todas las partículas obtienen peso cero. El remuestreo simplemente duplicará copias de partículas erróneas. El filtro está atrapado y no puede recuperarse.

### Solución: Filtro de Partículas Adaptativo (MCL con Inyección de Ruido)
Para solucionar esto, en lugar de remuestrear el $100\%$ de las partículas a partir del conjunto anterior, inyectamos una pequeña proporción de **partículas totalmente nuevas generadas de forma aleatoria a partir del sensor (Likelihood)**.

Dos variables de suavizado exponencial miden la calidad del ajuste de las mediciones:
*   $w_{\text{slow}}$: Promedio a largo plazo de la verosimilitud de las mediciones.
*   $w_{\text{fast}}$: Promedio a corto plazo.

Si $w_{\text{fast}} \ll w_{\text{slow}}$, significa que las lecturas del sensor han empeorado drásticamente de forma súbita (¡el robot ha sido secuestrado!). En ese instante, calculamos la probabilidad de inyectar partículas aleatorias como:
$$P_{\text{random}} = \max\left( 0.0, 1.0 - \frac{w_{\text{fast}}}{w_{\text{slow}}} \right)$$

Esto permite que el robot se recupere del secuestro de forma casi inmediata en el siguiente ciclo.

---

En el **Proyecto Integrador Práctico (`Practica_Proye_Integrador.ipynb`)**, resolveremos el desafío definitivo: **Localización Global ante Obstáculos y Recuperación de Secuestros**. Programaremos un robot en un laberinto cerrado y complejo. El robot se moverá de forma autónoma, simularemos un secuestro físico a mitad de trayectoria, y programaremos el algoritmo adaptativo de inyección de partículas para observar cómo el robot se auto-localiza y recupera su rumbo de forma brillante.
