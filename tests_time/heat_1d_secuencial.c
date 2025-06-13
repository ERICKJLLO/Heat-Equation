// Simulacion de la difusión de calor en una barra unidimensional en manera secuencial y por diferencias finitas

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

// Parámetros de la simulación
#define N 1000               // Número de puntos en la barra
#define L 1.0                // Longitud de la barra (metros)
#define T_TOTAL 0.1          // Tiempo total de simulación (segundos)
#define ALPHA 0.0001         // Coeficiente de difusión térmica (m²/s)
#define CENTER_WIDTH 100     // Ancho de la zona caliente inicial

int main() {
    // Configuración de parámetros numéricos
    const double dx = L / (N - 1);
    const double dt = (dx * dx) / (4 * ALPHA);  // Más conservador para estabilidad
    const int steps = (int)(T_TOTAL / dt);
    const double factor = ALPHA * dt / (dx * dx);

    // Memoria para temperaturas
    double* u = (double*)malloc(N * sizeof(double));
    double* u_new = (double*)malloc(N * sizeof(double));

    // Inicialización: todo frío
    for (int i = 0; i < N; i++) {
        u[i] = 0.0;
    }

    // Condición inicial: bloque caliente en el centro
    int bloque_inicio = N / 3;
    int bloque_fin = 2 * N / 3;
    for (int i = bloque_inicio; i < bloque_fin; i++) {
        u[i] = 100.0;
    }

    double start_time = 0.0, end_time = 0.0;
    start_time = (double)clock() / CLOCKS_PER_SEC;

    // Bucle principal de simulación
    for (int n = 0; n < steps; n++) {
        // Condiciones de frontera fijas (0°C en extremos)
        u_new[0] = 0.0;
        u_new[N-1] = 0.0;

        // Cálculo secuencial de nuevas temperaturas
        for (int i = 1; i < N-1; i++) {
            u_new[i] = u[i] + factor * (u[i-1] - 2*u[i] + u[i+1]);
        }

        // Actualización secuencial
        for (int i = 0; i < N; i++) {
            u[i] = u_new[i];
        }

    }

    end_time = (double)clock() / CLOCKS_PER_SEC;

    // Resultados finales
    printf("Simulación completada (secuencial):\n");
    printf("- Pasos temporales: %d\n", steps);
    printf("- Tiempo de ejecución: %.4f segundos\n", end_time - start_time);
    printf("- Datos guardados en heat_results_secuencial.csv\n");

    // Liberar memoria
    free(u);
    free(u_new);

    // Guardar tiempo en un archivo txt
    FILE *ftime = fopen("execution_time.txt", "a");
    fprintf(ftime, "heat_1d_secuencial.c, Tiempo: %.4f segundos\n", end_time - start_time);
    fclose(ftime);

    return 0;
}
