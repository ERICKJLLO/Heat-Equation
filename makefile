# Compiladores y flags
CC=gcc
CFLAGS=-O2 -Wall
OMPFLAGS=-fopenmp

# Archivos fuente
SRC_DIR=src
BIN_DIR=bin

# Ejecutables
BIN_1D_SEQ=$(BIN_DIR)/heat_1d_secuencial.exe
BIN_1D_PAR=$(BIN_DIR)/heat_1d_parallel.exe
BIN_2D_SEQ=$(BIN_DIR)/heat_2d_secuencial.exe
BIN_2D_PAR=$(BIN_DIR)/heat_2d_parallel.exe
BIN_3D_SEQ=$(BIN_DIR)/heat_3d_secuencial.exe
BIN_3D_PAR=$(BIN_DIR)/heat_3d_parallel.exe

# Archivos de resultados
RESULTS=heat_results.csv heat_results_secuencial.csv heat2d_results.csv heat2d_results_secuencial.csv heat3d_results.csv heat3d_results_secuencial.csv

# Crear carpeta bin si no existe
$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# Compilación 1D
$(BIN_1D_SEQ): $(SRC_DIR)/heat_1d_secuencial.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $<

$(BIN_1D_PAR): $(SRC_DIR)/heat_1d_parallel.c | $(BIN_DIR)
	$(CC) $(CFLAGS) $(OMPFLAGS) -o $@ $<

# Compilación 2D
$(BIN_2D_SEQ): $(SRC_DIR)/heat_2d_secuencial.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $<

$(BIN_2D_PAR): $(SRC_DIR)/heat_2d_parallel.c | $(BIN_DIR)
	$(CC) $(CFLAGS) $(OMPFLAGS) -o $@ $<

# Compilación 3D
$(BIN_3D_SEQ): $(SRC_DIR)/heat_3d_secuencial.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $<

$(BIN_3D_PAR): $(SRC_DIR)/heat_3d_parallel.c | $(BIN_DIR)
	$(CC) $(CFLAGS) $(OMPFLAGS) -o $@ $<

# Compilar todos
all: $(BIN_1D_SEQ) $(BIN_1D_PAR) $(BIN_2D_SEQ) $(BIN_2D_PAR) $(BIN_3D_SEQ) $(BIN_3D_PAR)

# Limpiar ejecutables y resultados
clean:
	rm -f $(BIN_DIR)/*.exe
	rm -f $(RESULTS)

.PHONY: all clean
