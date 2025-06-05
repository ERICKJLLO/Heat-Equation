import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D  # Importa el toolkit 3D

def plot_1d_heat(filename):
    df = pd.read_csv(filename)
    # Ordena por posición para evitar líneas locas
    times = df['time'].unique()
    for t in times[::max(1, len(times)//5)]:
        subset = df[df['time'] == t].sort_values('position')
        plt.plot(subset['position'], subset['temperature'], label=f"t={t:.3f}s")
    plt.xlabel("Posición (m)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Difusión de calor 1D")
    plt.legend()
    plt.show(block=False)

def plot_2d_heat(filename, time_index=0):
    """
    Grafica la temperatura en 2D para un tiempo específico.
    """
    if not os.path.exists(filename):
        print(f"El archivo '{filename}' no existe.")
        return
    df = pd.read_csv(filename)
    if df.empty:
        print(f"El archivo '{filename}' está vacío.")
        return
    if len(df.columns) < 4:
        print(f"El archivo '{filename}' no tiene las columnas necesarias.")
        print(f"Columnas encontradas: {df.columns.tolist()}")
        return
    if len(df['time'].unique()) == 0:
        print(f"El archivo '{filename}' no contiene datos de tiempo.")
        return
    times = sorted(df['time'].unique())
    if time_index >= len(times):
        print(f"El índice de tiempo {time_index} está fuera de rango. Hay {len(times)} tiempos disponibles.")
        return
    t = times[time_index]
    subset = df[df['time'] == t].sort_values(['x', 'y'])
    x = np.sort(subset['x'].unique())
    y = np.sort(subset['y'].unique())
    X, Y = np.meshgrid(x, y)
    Z = subset.pivot(index='y', columns='x', values='temperature').values
    plt.figure(figsize=(6,5))
    plt.contourf(X, Y, Z, 20, cmap='hot')
    plt.colorbar(label="Temperatura (°C)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title(f"Difusión de calor 2D (t={t:.3f}s)")
    plt.show(block=False)

def plot_3d_heat(filename, time_index=0, z_index=None):
    """
    Grafica la temperatura en 3D como un mapa de calor 2D para un plano z específico y tiempo específico.
    """
    import os
    if not os.path.exists(filename):
        print(f"El archivo '{filename}' no existe.")
        return
    df = pd.read_csv(filename)
    if df.empty:
        print(f"El archivo '{filename}' está vacío.")
        return
    if len(df.columns) < 5:
        print(f"El archivo '{filename}' no tiene las columnas necesarias.")
        print(f"Columnas encontradas: {df.columns.tolist()}")
        return
    if len(df['time'].unique()) == 0 or len(df['z'].unique()) == 0:
        print(f"El archivo '{filename}' no contiene datos de tiempo o de z.")
        return
    times = sorted(df['time'].unique())
    zs = sorted(df['z'].unique())
    if time_index >= len(times):
        print(f"El índice de tiempo {time_index} está fuera de rango. Hay {len(times)} tiempos disponibles.")
        return
    # Selecciona el plano z central si no se especifica
    if z_index is None:
        z_index = len(zs) // 2
    if z_index >= len(zs):
        print(f"El índice de z {z_index} está fuera de rango. Hay {len(zs)} planos z disponibles.")
        return
    t = times[time_index]
    z = zs[z_index]
    subset = df[(df['time'] == t) & (df['z'] == z)].sort_values(['x', 'y'])
    if subset.empty:
        print(f"No hay datos para t={t}, z={z}.")
        return
    x = np.sort(subset['x'].unique())
    y = np.sort(subset['y'].unique())
    X, Y = np.meshgrid(x, y)
    Z = subset.pivot(index='y', columns='x', values='temperature').values
    if np.all(Z == Z.flat[0]):
        print("Advertencia: Todos los valores de temperatura en este plano son iguales.")
    plt.figure(figsize=(6,5))
    plt.contourf(X, Y, Z, 20, cmap='hot')
    plt.colorbar(label="Temperatura (°C)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title(f"Difusión de calor 3D (t={t:.3f}s, z={z:.3f}m)")
    plt.show(block=False)

def plot_3d_heat_surface(filename, time_index=0, temp_threshold=1.0):
    """
    Grafica la temperatura en 3D como un scatter volumétrico para un tiempo específico.
    Solo muestra puntos con temperatura mayor a temp_threshold.
    """
    if not os.path.exists(filename):
        print(f"El archivo '{filename}' no existe.")
        return
    df = pd.read_csv(filename)
    if df.empty or len(df.columns) < 5:
        print(f"El archivo '{filename}' está vacío o no tiene las columnas necesarias.")
        return
    times = sorted(df['time'].unique())
    if time_index >= len(times):
        print(f"El índice de tiempo {time_index} está fuera de rango. Hay {len(times)} tiempos disponibles.")
        return
    t = times[time_index]
    subset = df[(df['time'] == t) & (df['temperature'] > temp_threshold)]
    if subset.empty:
        print(f"No hay datos para t={t} con temperatura > {temp_threshold}.")
        return
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    p = ax.scatter(subset['x'], subset['y'], subset['z'], c=subset['temperature'], cmap='hot', marker='o', s=8)
    fig.colorbar(p, label="Temperatura (°C)")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_zlabel("z (m)")
    ax.set_title(f"Difusión de calor 3D (t={t:.3f}s)")
    plt.show(block=False)

if __name__ == "__main__":
    plot_1d_heat("heat_results.csv")
    plot_2d_heat("heat2d_results.csv", time_index=0)
    # plot_3d_heat("heat3d_results.csv", time_index=0, z_index=None)  # Puedes comentar esta línea si quieres solo la 3D real
    plot_3d_heat_surface("heat3d_results.csv", time_index=0)
    input("Presiona Enter para cerrar las gráficas...")
