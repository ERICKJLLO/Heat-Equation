#include <stdio.h>

// ...aquí iría la lógica de simulación...

void guardar_resultados_csv_2d(double tiempo, int NX, int NY, double dx, double dy, double **u) {
    FILE *output = fopen("heat2d_results.csv", "w");
    fprintf(output, "time,x,y,temperature\n");
    for (int i = 0; i < NX; i++) {
        for (int j = 0; j < NY; j++) {
            fprintf(output, "%f,%f,%f,%f\n", tiempo, i*dx, j*dy, u[i][j]);
        }
    }
    fclose(output);
}

// ...main y demás lógica...
