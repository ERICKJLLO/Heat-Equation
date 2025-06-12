# Ecuación de Calor 2D

La ecuación de calor en dos dimensiones es:

\[
\frac{\partial u}{\partial t} = \alpha \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)
\]

donde:
- \( u(x, y, t) \): temperatura en la posición \( (x, y) \) y tiempo \( t \)
- \( \alpha \): difusividad térmica (m²/s)

## Condiciones de frontera

Condiciones de Dirichlet (bordes a 0°C):

\[
u(0, y, t) = u(L, y, t) = u(x, 0, t) = u(x, L, t) = 0
\]

## Condición inicial

Bloque caliente en el centro:

\[
u(x, y, 0) = 
\begin{cases}
100, & x \in [L/3, 2L/3],\ y \in [L/3, 2L/3] \\
0,   & \text{en otro caso}
\end{cases}
\]

## Discretización numérica

Diferencias finitas explícitas:

- Mallado: \( x_i = i \Delta x \), \( y_j = j \Delta y \)
- Tiempo: \( t^n = n \Delta t \)

La actualización es:

\[
u_{i,j}^{n+1} = u_{i,j}^n + \lambda \left( u_{i-1,j}^n + u_{i+1,j}^n + u_{i,j-1}^n + u_{i,j+1}^n - 4u_{i,j}^n \right)
\]
donde \( \lambda = \alpha \frac{\Delta t}{(\Delta x)^2} \).

Condición de estabilidad: \( \Delta t \leq \frac{(\Delta x)^2}{4\alpha} \).

---
