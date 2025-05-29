import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_1d_heat(filename):
    df = pd.read_csv(filename)
    # Selecciona algunos tiempos para graficar
    times = df['time'].unique()
    for t in times[::max(1, len(times)//5)]:
        subset = df[df['time'] == t]
        plt.plot(subset['position'], subset['temperature'], label=f"t={t:.3f}s")
    plt.xlabel("Posición (m)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Difusión de calor 1D")
    plt.legend()
    plt.show()

def plot_2d_heat(filename, time_index=0):
    """
    Grafica la temperatura en 2D para un tiempo específico.
    """
    df = pd.read_csv(filename)
    times = sorted(df['time'].unique())
    t = times[time_index]
    subset = df[df['time'] == t]
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
    plt.show()

def plot_3d_heat(filename, time_index=0, z_index=0):
    """
    Grafica la temperatura en 3D como un mapa de calor 2D para un plano z específico y tiempo específico.
    """
    df = pd.read_csv(filename)
    times = sorted(df['time'].unique())
    zs = sorted(df['z'].unique())
    t = times[time_index]
    z = zs[z_index]
    subset = df[(df['time'] == t) & (df['z'] == z)]
    x = np.sort(subset['x'].unique())
    y = np.sort(subset['y'].unique())
    X, Y = np.meshgrid(x, y)
    Z = subset.pivot(index='y', columns='x', values='temperature').values
    plt.figure(figsize=(6,5))
    plt.contourf(X, Y, Z, 20, cmap='hot')
    plt.colorbar(label="Temperatura (°C)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title(f"Difusión de calor 3D (t={t:.3f}s, z={z:.3f}m)")
    plt.show()

if __name__ == "__main__":
    plot_1d_heat("heat_results.csv")
