# Ecuación de Calor 1D

La ecuación de calor en una dimensión describe la evolución temporal de la temperatura \( u(x, t) \) en una barra de longitud \( L \):

\[
\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}
\]

donde:
- \( u(x, t) \): temperatura en la posición \( x \) y tiempo \( t \)
- \( \alpha \): difusividad térmica (m²/s)

## Condiciones de frontera

Se usan condiciones de frontera de Dirichlet (temperatura fija en los extremos):

\[
u(0, t) = 0, \quad u(L, t) = 0
\]

## Condición inicial

La barra inicia fría salvo un bloque central caliente:

\[
u(x, 0) = 
\begin{cases}
100, & x \in [L/3, 2L/3] \\
0,   & \text{en otro caso}
\end{cases}
\]

## Discretización numérica

Se utiliza el método de diferencias finitas explícito:

- Espacio: \( x_i = i \cdot \Delta x \), \( i = 0, 1, ..., N-1 \)
- Tiempo: \( t^n = n \cdot \Delta t \)

La actualización es:

\[
u_i^{n+1} = u_i^n + \lambda (u_{i-1}^n - 2u_i^n + u_{i+1}^n)
\]
donde \( \lambda = \alpha \frac{\Delta t}{(\Delta x)^2} \).

La condición de estabilidad es \( \Delta t \leq \frac{(\Delta x)^2}{2\alpha} \).

---
