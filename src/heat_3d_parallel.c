#include <stdio.h>

// ...aquí iría la lógica de simulación...

void guardar_resultados_csv_3d(double tiempo, int NX, int NY, int NZ, double dx, double dy, double dz, double ***u) {
    FILE *output = fopen("heat3d_results.csv", "w");
    fprintf(output, "time,x,y,z,temperature\n");
    for (int i = 0; i < NX; i++) {
        for (int j = 0; j < NY; j++) {
            for (int k = 0; k < NZ; k++) {
                fprintf(output, "%f,%f,%f,%f,%f\n", tiempo, i*dx, j*dy, k*dz, u[i][j][k]);
            }
        }
    }
    fclose(output);
}

// ...main y demás lógica...
