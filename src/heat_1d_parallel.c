// Simulacion de la difusión de calor en una barra unidimensional en manera paralela y por diferencias finitas

// Importar librerías necesarias
#include <stdio.h>
#include <stdlib.h>
#include <omp.h> 
#include <math.h>

// Parámetros de la simulación
#define N 1000               // Número de puntos en la barra
#define L 1.0                // Longitud de la barra (metros)
#define T_TOTAL 0.1          // Tiempo total de simulación (segundos)
#define ALPHA 0.0001         // Coeficiente de difusión térmica (m²/s)
#define CENTER_WIDTH 100      // Ancho de la zona caliente inicial
#define THREADS 4            // Número de hilos para OpenMP

int main() {
    // Configuración de parámetros numéricos
    const double dx = L / (N - 1);
    const double dt = (dx * dx) / (4 * ALPHA);  // Más conservador para estabilidad
    const int steps = (int)(T_TOTAL / dt);
    const double factor = ALPHA * dt / (dx * dx);

    // Configurar número de hilos
    omp_set_num_threads(THREADS);

    // Memoria para temperaturas
    double* u = (double*)malloc(N * sizeof(double));
    double* u_new = (double*)malloc(N * sizeof(double));

    // Inicialización: todo frío
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        u[i] = 0.0;
    }

    // Condición inicial: bloque caliente en el centro
    int bloque_inicio = N / 3;
    int bloque_fin = 2 * N / 3;
    for (int i = bloque_inicio; i < bloque_fin; i++) {
        u[i] = 100.0;
    }

    // Archivo para guardar resultados
    FILE *output = fopen("heat_results.csv", "w");
    fprintf(output, "time,position,temperature\n");

    double start_time = omp_get_wtime();

    // Bucle principal de simulación
    for (int n = 0; n < steps; n++) {
        // Condiciones de frontera fijas (0°C en extremos)
        u_new[0] = 0.0;
        u_new[N-1] = 0.0;

        // Cálculo paralelo de nuevas temperaturas
        #pragma omp parallel for
        for (int i = 1; i < N-1; i++) {
            u_new[i] = u[i] + factor * (u[i-1] - 2*u[i] + u[i+1]);
        }

        // Actualización paralela
        #pragma omp parallel for
        for (int i = 0; i < N; i++) {
            u[i] = u_new[i];
        }

        // Guardar datos cada 100 pasos (opcional para animaciones)
        if (n % 100 == 0) {
            for (int i = 0; i < N; i++) {
                fprintf(output, "%f,%f,%f\n", n*dt, i*dx, u[i]);
            }
        }
    }

    double end_time = omp_get_wtime();

    // Resultados finales
    printf("Simulación completada:\n");
    printf("- Pasos temporales: %d\n", steps);
    printf("- Tiempo de ejecución: %.4f segundos\n", end_time - start_time);
    printf("- Datos guardados en heat_results.csv\n");

    // Liberar memoria
    free(u);
    free(u_new);
    fclose(output);

    return 0;
}