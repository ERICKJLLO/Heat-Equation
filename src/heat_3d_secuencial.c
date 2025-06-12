#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define NX 40         // Número de puntos en x
#define NY 40         // Número de puntos en y
#define NZ 40         // Número de puntos en z
#define L 1.0         // Longitud del cubo (m)
#define T_TOTAL 2.0   // Tiempo total de simulación (s)
#define ALPHA 0.0001  // Difusividad térmica (m^2/s)

int main() {
    const double dx = L / (NX - 1);
    const double dy = L / (NY - 1);
    const double dz = L / (NZ - 1);
    const double dt = (dx * dx) / (6 * ALPHA); // Condición de estabilidad para 3D
    const int steps = (int)(T_TOTAL / dt);
    const double factor = ALPHA * dt / (dx * dx);

    // Reservar memoria
    double ***u = (double***)malloc(NX * sizeof(double**));
    double ***u_new = (double***)malloc(NX * sizeof(double**));
    for (int i = 0; i < NX; i++) {
        u[i] = (double**)malloc(NY * sizeof(double*));
        u_new[i] = (double**)malloc(NY * sizeof(double*));
        for (int j = 0; j < NY; j++) {
            u[i][j] = (double*)malloc(NZ * sizeof(double));
            u_new[i][j] = (double*)malloc(NZ * sizeof(double));
        }
    }

    // Inicialización: todo frío
    for (int i = 0; i < NX; i++) {
        for (int j = 0; j < NY; j++) {
            for (int k = 0; k < NZ; k++) {
                u[i][j][k] = 0.0;
            }
        }
    }

    // Condición inicial: bloque caliente en el centro
    int bloque_x_inicio = NX / 3;
    int bloque_x_fin = 2 * NX / 3;
    int bloque_y_inicio = NY / 3;
    int bloque_y_fin = 2 * NY / 3;
    int bloque_z_inicio = NZ / 3;
    int bloque_z_fin = 2 * NZ / 3;
    for (int i = bloque_x_inicio; i < bloque_x_fin; i++) {
        for (int j = bloque_y_inicio; j < bloque_y_fin; j++) {
            for (int k = bloque_z_inicio; k < bloque_z_fin; k++) {
                u[i][j][k] = 100.0;
            }
        }
    }

    // Abrir archivo para guardar resultados
    FILE *output = fopen("heat3d_results_secuencial.csv", "w");
    if (!output) {
        printf("Error: No se pudo abrir heat3d_results_secuencial.csv para escritura.\n");
        for (int i = 0; i < NX; i++) {
            for (int j = 0; j < NY; j++) {
                free(u[i][j]);
                free(u_new[i][j]);
            }
            free(u[i]);
            free(u_new[i]);
        }
        free(u);
        free(u_new);
        return 1;
    }
    fprintf(output, "time,x,y,z,temperature\n");

    double start_time = (double)clock() / CLOCKS_PER_SEC;

    // Bucle principal de simulación
    for (int n = 0; n < steps; n++) {
        // Condiciones de frontera fijas (0°C)
        for (int i = 0; i < NX; i++) {
            for (int j = 0; j < NY; j++) {
                u_new[i][j][0] = 0.0;
                u_new[i][j][NZ-1] = 0.0;
            }
        }
        for (int i = 0; i < NX; i++) {
            for (int k = 0; k < NZ; k++) {
                u_new[i][0][k] = 0.0;
                u_new[i][NY-1][k] = 0.0;
            }
        }
        for (int j = 0; j < NY; j++) {
            for (int k = 0; k < NZ; k++) {
                u_new[0][j][k] = 0.0;
                u_new[NX-1][j][k] = 0.0;
            }
        }

        // Cálculo secuencial de nuevas temperaturas
        for (int i = 1; i < NX-1; i++) {
            for (int j = 1; j < NY-1; j++) {
                for (int k = 1; k < NZ-1; k++) {
                    u_new[i][j][k] = u[i][j][k] + factor * (
                        u[i-1][j][k] + u[i+1][j][k] +
                        u[i][j-1][k] + u[i][j+1][k] +
                        u[i][j][k-1] + u[i][j][k+1] -
                        6*u[i][j][k]
                    );
                }
            }
        }

        // Actualización
        for (int i = 0; i < NX; i++) {
            for (int j = 0; j < NY; j++) {
                for (int k = 0; k < NZ; k++) {
                    u[i][j][k] = u_new[i][j][k];
                }
            }
        }

        // Guardar datos cada 5 pasos (para no generar archivos enormes)
        if (n % 5 == 0) {
            for (int i = 0; i < NX; i++) {
                for (int j = 0; j < NY; j++) {
                    for (int k = 0; k < NZ; k++) {
                        fprintf(output, "%f,%f,%f,%f,%f\n", n*dt, i*dx, j*dy, k*dz, u[i][j][k]);
                    }
                }
            }
        }
    }

    double end_time = (double)clock() / CLOCKS_PER_SEC;

    printf("Simulación 3D completada (secuencial):\n");
    printf("- Pasos temporales: %d\n", steps);
    printf("- Tiempo de ejecución: %.4f segundos\n", end_time - start_time);
    printf("- Datos guardados en heat3d_results_secuencial.csv\n");

    // Liberar memoria
    for (int i = 0; i < NX; i++) {
        for (int j = 0; j < NY; j++) {
            free(u[i][j]);
            free(u_new[i][j]);
        }
        free(u[i]);
        free(u_new[i]);
    }
    free(u);
    free(u_new);
    fclose(output);

    return 0;
}
