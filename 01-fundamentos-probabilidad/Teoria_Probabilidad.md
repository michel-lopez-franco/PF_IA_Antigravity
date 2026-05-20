# Módulo 1: Fundamentos de Probabilidad y Estadística para Filtros Bayesianos

La estimación de estados en robótica y sistemas dinámicos consiste fundamentalmente en **gestionar la incertidumbre**. Los sensores son ruidosos, los actuadores son imprecisos y los modelos del mundo real son aproximaciones. Para navegar por este mundo imperfecto, la **probabilidad y la estadística** son nuestras herramientas más potentes.

En este módulo, sentaremos las bases matemáticas indispensables que sustentan los Filtros de Kalman y los Filtros de Partículas.

---

## 1. Variables Aleatorias y Funciones de Densidad

Una **Variable Aleatoria (V.A.)** $X$ es una cantidad cuyo valor está sujeto a variaciones debido al azar o a la falta de información perfecta. Puede ser:
- **Discreta:** Toma valores en un conjunto contable (ej. el resultado de lanzar un dado, o si un sensor de obstáculos detecta un obstáculo o no $[0, 1]$).
- **Continua:** Toma valores en un rango continuo (ej. la posición exacta de un robot $x \in \mathbb{R}$, o su velocidad).

### Función de Densidad de Probabilidad (PDF)
Para una V.A. continua $X$, no podemos hablar de la probabilidad de que tome un valor exacto (ya que $P(X = x) = 0$). En su lugar, definimos la **Función de Densidad de Probabilidad (PDF)**, denotada como $p(x)$, la cual describe la verosimilitud relativa de que la variable tome cierto valor.

Propiedades fundamentales de una PDF:
1. $p(x) \ge 0$ para todo $x$.
2. El área total bajo la curva es igual a 1:
   $$\int_{-\infty}^{\infty} p(x) \, dx = 1$$
3. La probabilidad de que $X$ se encuentre en el intervalo $[a, b]$ está dada por la integral:
   $$P(a \le X \le b) = \int_{a}^{b} p(x) \, dx$$

---

## 2. Estadísticos Clave: Media, Varianza y Covarianza

Para caracterizar una distribución de probabilidad sin necesidad de conocer toda su forma, utilizamos medidas estadísticas clave.

### Esperanza Matemática (Media)
La esperanza $\mathbb{E}[X]$ o media $\mu$ es el valor promedio esperado de la V.A. tras infinitas repeticiones del experimento.
- **Para el caso continuo:**
  $$\mu = \mathbb{E}[X] = \int_{-\infty}^{\infty} x \, p(x) \, dx$$

### Varianza ($\sigma^2$) y Desviación Estándar ($\sigma$)
La varianza mide qué tan dispersos están los valores de la V.A. alrededor de su media.
$$\sigma^2 = \text{Var}(X) = \mathbb{E}[(X - \mu)^2] = \int_{-\infty}^{\infty} (x - \mu)^2 \, p(x) \, dx$$
La **desviación estándar** $\sigma = \sqrt{\text{Var}(X)}$ está en las mismas unidades que la variable original.

### Covarianza y Matriz de Covarianza
Cuando trabajamos con múltiples variables (como la posición en $x$ e $y$ de un robot), necesitamos medir cómo varían conjuntamente.

La **covarianza** entre dos variables aleatorias $X$ e $Y$ se define como:
$$\text{Cov}(X, Y) = \mathbb{E}[(X - \mu_X)(Y - \mu_Y)]$$

Si definimos un vector aleatorio multidimensional $\mathbf{x} = [X_1, X_2, \dots, X_n]^T \in \mathbb{R}^n$, su **Matriz de Covarianza** $\mathbf{\Sigma}$ (Sigma mayúscula) es una matriz simétrica de tamaño $n \times n$ donde:
$$\mathbf{\Sigma} = \mathbb{E}[(\mathbf{x} - \boldsymbol{\mu})(\mathbf{x} - \boldsymbol{\mu})^T]$$

$$\mathbf{\Sigma} = \begin{bmatrix} 
\text{Var}(X_1) & \text{Cov}(X_1, X_2) & \dots & \text{Cov}(X_1, X_n) \\
\text{Cov}(X_2, X_1) & \text{Var}(X_2) & \dots & \text{Cov}(X_2, X_n) \\
\vdots & \vdots & \ddots & \vdots \\
\text{Cov}(X_n, X_1) & \text{Cov}(X_n, X_2) & \dots & \text{Var}(X_n)
\end{bmatrix}$$

> [!NOTE]
> - Los elementos en la diagonal principal representan las varianzas individuales de cada dimensión.
> - Los elementos fuera de la diagonal representan la correlación entre variables. Si $\text{Cov}(X_i, X_j) > 0$, tienden a aumentar juntas; si es $< 0$, una aumenta mientras la otra disminuye.

---

## 3. La Distribución Gaussiana (Normal)

La distribución Gaussiana es la piedra angular de los **Filtros de Kalman**. Debido al Teorema del Límite Central, el ruido en la naturaleza (incluyendo el de los sensores) a menudo se modela de forma excelente mediante gaussianas.

### Gaussiana Univariada ($X \sim \mathcal{N}(\mu, \sigma^2)$)
Su PDF está definida por:
$$p(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$$

*   $\mu$ controla el centro de la campana.
*   $\sigma$ controla el ancho.

```
          * *
        *     *      <- Campana de Gauss
       *  |    *
      *   |     *
    --*---|-----*--
          μ
```

### Gaussiana Multivariada ($\mathbf{x} \sim \mathcal{N}(\boldsymbol{\mu}, \mathbf{\Sigma})$)
Para un vector aleatorio en $\mathbb{R}^n$, la densidad de probabilidad conjunta está dada por:
$$p(\mathbf{x}) = \frac{1}{\sqrt{(2\pi)^n |\mathbf{\Sigma}|}} \exp\left( -\frac{1}{2} (\mathbf{x} - \boldsymbol{\mu})^T \mathbf{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu}) \right)$$

Donde $|\mathbf{\Sigma}|$ es el determinante de la matriz de covarianza, y $\mathbf{\Sigma}^{-1}$ es su inversa.

```
       Visualización Contorno 2D (Elipses de Incertidumbre)

         Y ^      . - - - .
           |    /           \
           |   |      *      |  <- Centro en μ = [μ_x, μ_y]^T
           |    \   (μ_x,μ_y) /
           |      ` - - - '
           +-------------------> X
```

---

## 4. Probabilidad Condicional, Conjunta y Marginalización

Para entender la estimación recursiva de estados, debemos dominar tres conceptos fundamentales de probabilidad conjunta:

### Probabilidad Conjunta
Describe la probabilidad de que múltiples eventos ocurran simultáneamente.
$$p(x, y) = P(X = x \text{ e } Y = y)$$

Si $X$ e $Y$ son **independientes**, entonces:
$$p(x, y) = p(x) p(y)$$

### Probabilidad Condicional
Es la probabilidad de que ocurra el evento $x$ dado que ya sabemos que ocurrió el evento $y$.
$$p(x \mid y) = \frac{p(x, y)}{p(y)}$$

De aquí se deriva la **Regla del Producto**:
$$p(x, y) = p(x \mid y) \, p(y) = p(y \mid x) \, p(x)$$

### Marginalización (Teorema de Probabilidad Total)
Si conocemos la distribución conjunta $p(x,y)$ y queremos aislar la distribución de una sola de las variables, "sumamos" o "integramos" sobre todos los valores posibles de la otra variable.
- **Caso continuo:**
  $$p(x) = \int_{-\infty}^{\infty} p(x, y) \, dy = \int_{-\infty}^{\infty} p(x \mid y) \, p(y) \, dy$$

> [!IMPORTANT]
> La marginalización es crucial en el paso de **Predicción** de los Filtros Bayesianos (Chapman-Kolmogorov), donde calculamos la probabilidad de estar en un nuevo estado integrando sobre todas las formas posibles de haber llegado desde el estado anterior.

---

## 5. El Teorema de Bayes: El Corazón de la Estimación

El **Teorema de Bayes** nos permite actualizar nuestras creencias sobre una hipótesis (ej. la ubicación de nuestro robot) basándonos en nuevas evidencias (ej. las lecturas de un sensor ruidoso).

Se deriva directamente de la regla del producto:
$$p(x \mid y) = \frac{p(y \mid x) \, p(x)}{p(y)}$$

### Interpretación para Estimación de Estados
En la práctica, sustituimos los términos por conceptos de nuestro sistema:
*   Sea $x$ el **estado** del sistema (ej. posición real del robot).
*   Sea $z$ la **medición** del sensor (ej. distancia detectada a un obstáculo).

El Teorema de Bayes se escribe como:
$$p(x \mid z) = \frac{p(z \mid x) \, p(x)}{p(z)}$$

Analicemos cada componente detalladamente:

1.  **$p(x)$ - El Prior (Creencia A Priori):**
    Representa nuestra creencia sobre el estado del sistema *antes* de incorporar la nueva medición $z$. Proviene generalmente del paso de predicción basado en nuestro modelo de movimiento física/dinámica del sistema.
2.  **$p(z \mid x)$ - La Verosimilitud (Likelihood):**
    Es el modelo de medición del sensor. Nos dice: "si la posición real del robot fuera exactamente $x$, ¿qué tan probable es que el sensor reporte la medición $z$?". Representa la física y el nivel de ruido del sensor.
3.  **$p(z)$ - La Probabilidad Marginal de la Medida (Normalizador):**
    Es una constante de normalización que asegura que la distribución resultante $p(x \mid z)$ sea una PDF válida (integre a 1). Se calcula usando la ley de probabilidad total:
    $$p(z) = \int p(z \mid x) \, p(x) \, dx$$
    Dado que $p(z)$ no depende directamente de $x$, a menudo la escribimos como una constante de escala $\eta$ o $\alpha$:
    $$p(x \mid z) = \eta \, p(z \mid x) \, p(x)$$
4.  **$p(x \mid z)$ - El Posterior (Creencia A Posteriori):**
    Nuestra creencia actualizada sobre el estado tras fusionar lo que sabíamos del movimiento (Prior) con lo que observamos de los sensores (Likelihood).

---

## ✍️ Ejercicio de Comprensión Mental
Imagina un robot móvil que se mueve en un pasillo 1D. El robot tiene un sensor de puertas.
*   **Prior $p(x)$:** Creemos que hay un $80\%$ de probabilidad de estar frente a una pared y $20\%$ frente a una puerta.
*   **Likelihood $p(z \mid x)$:** El sensor no es perfecto. Si estamos frente a una puerta, detecta "puerta" el $90\%$ de las veces. Si estamos frente a la pared, detecta erróneamente "puerta" (falso positivo) el $10\%$ de las veces.

Si el sensor de repente detecta **"puerta"**, ¿cuál es la probabilidad real de que estemos frente a una puerta?

*Aplica el Teorema de Bayes:*
*   Hypothesis: $x \in \{\text{Puerta}, \text{Pared}\}$
*   Medición: $z = \text{"Puerta"}$
*   $P(\text{Puerta}) = 0.20$, $P(\text{Pared}) = 0.80$ (Prior)
*   $P(z = \text{"Puerta"} \mid \text{Puerta}) = 0.90$ (Likelihood verdadero positivo)
*   $P(z = \text{"Puerta"} \mid \text{Pared}) = 0.10$ (Likelihood falso positivo)

1.  *Multiplicar Prior $\times$ Likelihood:*
    *   $\text{Puerta}: 0.20 \times 0.90 = 0.18$
    *   $\text{Pared}: 0.80 \times 0.10 = 0.08$
2.  *Calcular el normalizador $p(z)$:*
    *   $p(z) = 0.18 + 0.08 = 0.26$
3.  *Calcular el Posterior:*
    *   $P(\text{Puerta} \mid z = \text{"Puerta"}) = \frac{0.18}{0.26} \approx \mathbf{69.2\%}$

A pesar de que el sensor detectó una puerta y es $90\%$ preciso para las puertas, la probabilidad posterior de estar frente a una puerta es de solo $69.2\%$ debido al fuerte efecto del Prior (las paredes son mucho más comunes). Este es el poder del razonamiento Bayesiano.

---

En la **Práctica 1 (`Practica_Fundamentos.ipynb`)**, implementaremos este comportamiento de forma interactiva y visualizaremos la actualización bayesiana en tiempo real tanto para este caso discreto como para gaussianas continuas.
