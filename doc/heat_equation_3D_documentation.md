# Ecuación de Calor 3D

La ecuación de calor en tres dimensiones es:

\[
\frac{\partial u}{\partial t} = \alpha \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} + \frac{\partial^2 u}{\partial z^2} \right)
\]

donde:
- \( u(x, y, z, t) \): temperatura en la posición \( (x, y, z) \) y tiempo \( t \)
- \( \alpha \): difusividad térmica (m²/s)

## Condiciones de frontera

Condiciones de Dirichlet (bordes a 0°C):

\[
u(0, y, z, t) = u(L, y, z, t) = u(x, 0, z, t) = u(x, L, z, t) = u(x, y, 0, t) = u(x, y, L, t) = 0
\]

## Condición inicial

Bloque caliente en el centro:

\[
u(x, y, z, 0) = 
\begin{cases}
100, & x \in [L/3, 2L/3],\ y \in [L/3, 2L/3],\ z \in [L/3, 2L/3] \\
0,   & \text{en otro caso}
\end{cases}
\]

## Discretización numérica

Diferencias finitas explícitas:

- Mallado: \( x_i = i \Delta x \), \( y_j = j \Delta y \), \( z_k = k \Delta z \)
- Tiempo: \( t^n = n \Delta t \)

La actualización es:

\[
u_{i,j,k}^{n+1} = u_{i,j,k}^n + \lambda \left(
u_{i-1,j,k}^n + u_{i+1,j,k}^n +
u_{i,j-1,k}^n + u_{i,j+1,k}^n +
u_{i,j,k-1}^n + u_{i,j,k+1}^n - 6u_{i,j,k}^n
\right)
\]
donde \( \lambda = \alpha \frac{\Delta t}{(\Delta x)^2} \).

Condición de estabilidad: \( \Delta t \leq \frac{(\Delta x)^2}{6\alpha} \).

---
