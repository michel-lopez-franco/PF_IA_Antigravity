# Módulo 4: Filtros de Partículas (Sequential Importance Resampling - SIR)

En los módulos anteriores vimos los Filtros de Kalman, que asumen que la incertidumbre es Gaussiana y los modelos son continuos. Pero, ¿qué pasa si el robot se encuentra en un laberinto donde la creencia es multimodal (múltiples picos de probabilidad, ej: *"puedo estar en la habitación A o en la B que son idénticas"*), o si hay fuertes no linealidades y el ruido no es Gaussiano?

Para estos casos complejos, el **Filtro de Partículas (o Monte Carlo Localization)** es el estándar de oro de la robótica moderna.

---

## 1. Métodos Monte Carlo y Muestreo por Importancia

El Filtro de Partículas es un **método no paramétrico**, lo que significa que no asume ninguna forma matemática predefinida (como una Gaussiana) para representar la creencia. En su lugar, aproxima cualquier distribución de probabilidad continua mediante un conjunto de muestras discretas llamadas **Partículas**.

### Representación por Partículas
La creencia $\text{bel}(x_t)$ se representa mediante un conjunto $\mathcal{X}_t$ de $M$ partículas:
$$\mathcal{X}_t = \{ \langle x_t^{[1]}, w_t^{[1]} \rangle, \langle x_t^{[2]}, w_t^{[2]} \rangle, \dots, \langle x_t^{[M]}, w_t^{[M]} \rangle \}$$

Donde:
*   $x_t^{[i]}$: Es una hipótesis del estado real (ej. una posición hipotética del robot).
*   $w_t^{[i]}$: Es el peso de importancia (la probabilidad o verosimilitud de que esa hipótesis sea la real).

```
         Aproximación de PDF compleja mediante partículas:

PDF Real:     _/\_     _/\_             (Distribución Multimodal)
             /    \   /    \
Partículas:  ||||||   ||||||            (Mayor densidad de muestras = Mayor probabilidad)
```

---

### Muestreo por Importancia (Importance Sampling)
Supongamos que queremos obtener muestras de una distribución **objetivo** $f(x)$ (el posterior real), pero es extremadamente difícil de calcular analíticamente o muestrear directamente. Sin embargo, sí podemos evaluar y muestrear de una distribución de **propuesta** $g(x)$ (el modelo de movimiento).

Para compensar la diferencia entre muestrear de $g(x)$ en lugar de $f(x)$, asignamos a cada muestra un **peso de importancia**:
$$w(x) = \frac{f(x)}{g(x)}$$

Al promediar nuestras muestras ponderadas por $w(x)$, aproximamos de forma exacta la distribución objetivo $f(x)$.

---

## 2. El Algoritmo Bootstrap Particle Filter (SIR)

El algoritmo clásico de Filtro de Partículas se compone de cuatro pasos cíclicos esenciales:

### Paso 1: Inicialización
Generamos $M$ partículas al azar a partir de la creencia inicial $p(x_0)$. Si no sabemos dónde está el robot (localización global), las distribuimos de manera uniforme por todo el mapa. Todas las partículas comienzan con un peso uniforme $w_0^{[i]} = \frac{1}{M}$.

### Paso 2: Predicción (Propagación)
Para cada partícula $i = 1, \dots, M$, propagamos su estado hacia el futuro aplicando el modelo dinámico del sistema y añadiendo ruido de proceso.
$$x_t^{[i]} \sim p(x_t \mid x_{t-1}^{[i]}, u_t)$$

> [!NOTE]
> Cada partícula "simula" el movimiento de forma independiente. Si el robot gira a la derecha, todas las partículas se desplazan y giran a la derecha con un pequeño error aleatorio individual.

### Paso 3: Actualización (Cálculo de Pesos)
Cuando el sensor toma la medición real $z_t$, evaluamos qué tan compatible es la medición con lo que cada partícula *debería* ver en su respectiva posición hipotética. El peso de importancia se actualiza como la **verosimilitud (Likelihood)**:
$$w_t^{[i]} \propto p(z_t \mid x_t^{[i]})$$

Luego, **normalizamos** todos los pesos para que sumen 1:
$$\tilde{w}_t^{[i]} = \frac{w_t^{[i]}}{\sum_{j=1}^M w_t^{[j]}}$$

> [!TIP]
> Las partículas que están cerca de la posición real del robot obtendrán lecturas simuladas similares a las reales, por lo que su peso aumentará. Las partículas alejadas obtendrán un peso extremadamente bajo o nulo.

---

### Paso 4: Remuestreo (Resampling)

#### El Fenómeno del Empobrecimiento (Degeneracy)
Tras unos pocos pasos del filtro sin remuestreo, casi todas las partículas se moverán a regiones de baja probabilidad y sus pesos normalizados serán casi $0$, mientras que una única partícula acumulará el $99.9\%$ del peso total. El recurso computacional se desperdicia simulando partículas inútiles.

Para medir esto de forma cuantitativa, calculamos el **Número Efectivo de Partículas ($N_{\text{eff}}$)**:
$$N_{\text{eff}} = \frac{1}{\sum_{i=1}^M (w_t^{[i]})^2}$$

Si $N_{\text{eff}} < N_{\text{umbral}}$ (típicamente $\frac{M}{2}$), realizamos un **Remuestreo**.

```
Antes de Resampling:   * (w=0.01)    * (w=0.01)    * (w=0.96)    * (w=0.02)
                                                      |
Resampling (Copia):                                 / | \
                                                   /  |  \
Después de Resampling: * (w=0.25)    * (w=0.25)    * (w=0.25)    * (w=0.25)
```

#### ¿Qué hace el Remuestreo?
1.  Selecciona con reemplazo $M$ nuevas partículas del conjunto actual de forma probabilística: **las partículas con alto peso tienen alta probabilidad de ser duplicadas**, mientras que las de bajo peso se descartan.
2.  Reinicia todos los pesos a $w_t^{[i]} = \frac{1}{M}$.

---

## 3. Algoritmos de Remuestreo (Resampling)

Existen varios algoritmos para remuestrear de manera eficiente. El más utilizado en robótica por su baja varianza y velocidad lineal $\mathcal{O}(M)$ es el **Remuestreo Sistemático (o Stochastic Universal Sampling)**.

### Algoritmo de la Rueda de Remuestreo (Resampling Wheel)
Una analogía visual muy intuitiva consiste en crear una ruleta circular donde el tamaño del sector asignado a cada partícula es proporcional a su peso. 

```text
         Rueda de Remuestreo (Sistemático)
         
                  Partícula 3 (w = 0.60)
                     /===========\
                    /             \
 Partícula 2 (0.15) |      *      | Partícula 4 (0.15)
                    \             /
                     \===========/
                  Partícula 1 (w = 0.10)
```

En lugar de lanzar la ruleta $M$ veces de forma independiente (lo que introduce alta varianza y es $\mathcal{O}(M \log M)$), el **Remuestreo Sistemático** dibuja $M$ flechas espaciadas exactamente a una distancia regular de $\frac{1}{M}$ a lo largo del círculo, y gira la rueda una única vez al azar con un desplazamiento inicial $r \in [0, \frac{1}{M}]$.

Esto garantiza que incluso las partículas con pesos pequeños tengan una representación justa y reduce drásticamente el ruido de muestreo numérico.

---

### Ecuaciones y Flujo del Algoritmo SIR Completo

```text
Algoritmo Filtro_Particulas_SIR( X_{t-1}, u_t, z_t ):
    X_bar_t = Ø
    X_t = Ø
    
    // 1. Muestreo y propagación
    Para i = 1 hasta M:
        x_t^{[i]} ~ p(x_t | x_{t-1}^{[i]}, u_t)
        w_t^{[i]} = p(z_t | x_t^{[i]})
        X_bar_t = X_bar_t U { < x_t^{[i]}, w_t^{[i]} > }
        
    // 2. Normalización de pesos
    Normalizar pesos en X_bar_t para que sumen 1
    
    // 3. Remuestreo Condicional
    Si N_eff < M / 2:
        X_t = Remuestreo_Sistematico( X_bar_t )
    Sino:
        X_t = X_bar_t
        
    retornar X_t
```

---

En la **Práctica 4 (`Practica_Particulas.ipynb`)**, implementaremos un simulador 2D interactivo completo. Crearemos un robot móvil ruidoso en un entorno con múltiples balizas (Landmarks), lanzaremos una nube de 1000 partículas distribuidas de forma uniforme (Localización Global) y programaremos la predicción cinemática, el cálculo de pesos y la **Rueda de Remuestreo Sistemático** desde cero. ¡Verás a las partículas agruparse y rodear al robot real en tiempo real!
