#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define NX 100         // Número de puntos en x
#define NY 100         // Número de puntos en y
#define L 1.0          // Longitud de la barra (m)
#define T_TOTAL 0.5   // Tiempo total de simulación (s) (AUMENTADO)
#define ALPHA 0.0001   // Difusividad térmica (m^2/s)
#define THREADS 4      // Número de hilos

int main() {
    const double dx = L / (NX - 1);
    const double dy = L / (NY - 1);
    const double dt = (dx * dx) / (4 * ALPHA); // Condición de estabilidad
    const int steps = (int)(T_TOTAL / dt);
    printf("dt = %g, steps = %d\n", dt, steps); // DEPURACIÓN
    const double factor = ALPHA * dt / (dx * dx);

    omp_set_num_threads(THREADS);

    // Reservar memoria
    double **u = (double**)malloc(NX * sizeof(double*));
    double **u_new = (double**)malloc(NX * sizeof(double*));
    for (int i = 0; i < NX; i++) {
        u[i] = (double*)malloc(NY * sizeof(double));
        u_new[i] = (double*)malloc(NY * sizeof(double));
    }

    // Inicialización: todo frío
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < NX; i++) {
        for (int j = 0; j < NY; j++) {
            u[i][j] = 0.0;
        }
    }

    // Condición inicial: bloque caliente en el centro
    int bloque_x_inicio = NX / 3;
    int bloque_x_fin = 2 * NX / 3;
    int bloque_y_inicio = NY / 3;
    int bloque_y_fin = 2 * NY / 3;
    for (int i = bloque_x_inicio; i < bloque_x_fin; i++) {
        for (int j = bloque_y_inicio; j < bloque_y_fin; j++) {
            u[i][j] = 100.0;
        }
    }

    // Abrir archivo para guardar resultados
    FILE *output = fopen("heat2d_results.csv", "w");
    if (!output) {
        printf("Error: No se pudo abrir heat2d_results.csv para escritura.\n");
        // Liberar memoria antes de salir
        for (int i = 0; i < NX; i++) {
            free(u[i]);
            free(u_new[i]);
        }
        free(u);
        free(u_new);
        return 1;
    }
    fprintf(output, "time,x,y,temperature\n");

    double start_time = omp_get_wtime();

    // Bucle principal de simulación
    for (int n = 0; n < steps; n++) {
        // Condiciones de frontera fijas (0°C)
        #pragma omp parallel for
        for (int i = 0; i < NX; i++) {
            u_new[i][0] = 0.0;
            u_new[i][NY-1] = 0.0;
        }
        #pragma omp parallel for
        for (int j = 0; j < NY; j++) {
            u_new[0][j] = 0.0;
            u_new[NX-1][j] = 0.0;
        }

        // Cálculo paralelo de nuevas temperaturas
        #pragma omp parallel for collapse(2)
        for (int i = 1; i < NX-1; i++) {
            for (int j = 1; j < NY-1; j++) {
                u_new[i][j] = u[i][j] + factor * (
                    u[i-1][j] + u[i+1][j] + u[i][j-1] + u[i][j+1] - 4*u[i][j]
                );
            }
        }

        // Actualización
        #pragma omp parallel for collapse(2)
        for (int i = 0; i < NX; i++) {
            for (int j = 0; j < NY; j++) {
                u[i][j] = u_new[i][j];
            }
        }

        // Guardar datos cada 20 pasos (fuera de regiones paralelas)
        if (n % 20 == 0) {
            for (int i = 0; i < NX; i++) {
                for (int j = 0; j < NY; j++) {
                    fprintf(output, "%f,%f,%f,%f\n", n*dt, i*dx, j*dy, u[i][j]);
                }
            }
        }
    }

    double end_time = omp_get_wtime();

    printf("Simulación 2D completada:\n");
    printf("- Pasos temporales: %d\n", steps);
    printf("- Tiempo de ejecución: %.4f segundos\n", end_time - start_time);
    printf("- Datos guardados en heat2d_results.csv\n");

    // Liberar memoria
    for (int i = 0; i < NX; i++) {
        free(u[i]);
        free(u_new[i]);
    }
    free(u);
    free(u_new);
    fclose(output);

    return 0;
}
