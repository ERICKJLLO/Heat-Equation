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

def plot_1d_comparison(file_seq, file_par, save_path="comparacion_1d.png"):
    """
    Compara la evolución 1D entre secuencial y paralelo y guarda la imagen.
    """
    if not os.path.exists(file_seq) or not os.path.exists(file_par):
        print("No se encuentran ambos archivos para comparar 1D.")
        return
    df_seq = pd.read_csv(file_seq)
    df_par = pd.read_csv(file_par)
    # Selecciona el último tiempo disponible en ambos
    t_seq = df_seq['time'].max()
    t_par = df_par['time'].max()
    subset_seq = df_seq[df_seq['time'] == t_seq].sort_values('position')
    subset_par = df_par[df_par['time'] == t_par].sort_values('position')
    plt.figure()
    plt.plot(subset_seq['position'], subset_seq['temperature'], label=f"Secuencial t={t_seq:.3f}s")
    plt.plot(subset_par['position'], subset_par['temperature'], '--', label=f"Paralelo t={t_par:.3f}s")
    plt.xlabel("Posición (m)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Comparación Difusión de Calor 1D (Secuencial vs Paralelo)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Comparación 1D guardada en {save_path}")

def plot_2d_comparison(file_seq, file_par, time_index=0, save_path="comparacion_2d.png"):
    """
    Compara la evolución 2D entre secuencial y paralelo y guarda la imagen.
    """
    if not os.path.exists(file_seq) or not os.path.exists(file_par): 
        print("No se encuentran ambos archivos para comparar 2D.")
        return
    df_seq = pd.read_csv(file_seq)
    df_par = pd.read_csv(file_par)
    times_seq = sorted(df_seq['time'].unique())
    times_par = sorted(df_par['time'].unique())
    if time_index >= len(times_seq) or time_index >= len(times_par):
        print("Índice de tiempo fuera de rango para comparación 2D.")
        return
    t_seq = times_seq[time_index]
    t_par = times_par[time_index]
    subset_seq = df_seq[df_seq['time'] == t_seq].sort_values(['x', 'y'])
    subset_par = df_par[df_par['time'] == t_par].sort_values(['x', 'y'])
    x_seq = np.sort(subset_seq['x'].unique())
    y_seq = np.sort(subset_seq['y'].unique())
    x_par = np.sort(subset_par['x'].unique())
    y_par = np.sort(subset_par['y'].unique())
    X_seq, Y_seq = np.meshgrid(x_seq, y_seq)
    X_par, Y_par = np.meshgrid(x_par, y_par)
    Z_seq = subset_seq.pivot(index='y', columns='x', values='temperature').values
    Z_par = subset_par.pivot(index='y', columns='x', values='temperature').values
    fig, axs = plt.subplots(1, 2, figsize=(12,5))
    cs1 = axs[0].contourf(X_seq, Y_seq, Z_seq, 20, cmap='hot')
    fig.colorbar(cs1, ax=axs[0])
    axs[0].set_title(f"Secuencial t={t_seq:.3f}s")
    axs[0].set_xlabel("x (m)")
    axs[0].set_ylabel("y (m)")
    cs2 = axs[1].contourf(X_par, Y_par, Z_par, 20, cmap='hot')
    fig.colorbar(cs2, ax=axs[1])
    axs[1].set_title(f"Paralelo t={t_par:.3f}s")
    axs[1].set_xlabel("x (m)")
    axs[1].set_ylabel("y (m)")
    plt.suptitle("Comparación Difusión de Calor 2D (Secuencial vs Paralelo)")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Comparación 2D guardada en {save_path}")

def plot_3d_comparison(file_seq, file_par, time_index=0, z_index=None, save_path="comparacion_3d.png"):
    """
    Compara la evolución 3D entre secuencial y paralelo en subplots para un plano z y tiempo específico y guarda la imagen.
    """
    if not os.path.exists(file_seq) or not os.path.exists(file_par):
        print("No se encuentran ambos archivos para comparar 3D.")
        return
    df_seq = pd.read_csv(file_seq)
    df_par = pd.read_csv(file_par)
    if df_seq.empty or df_par.empty:
        print("Uno de los archivos está vacío.")
        return
    times_seq = sorted(df_seq['time'].unique())
    times_par = sorted(df_par['time'].unique())
    zs_seq = sorted(df_seq['z'].unique())
    zs_par = sorted(df_par['z'].unique())
    if time_index >= len(times_seq) or time_index >= len(times_par):
        print("Índice de tiempo fuera de rango para comparación 3D.")
        return
    # Selecciona el plano z central si no se especifica
    if z_index is None:
        z_index_seq = len(zs_seq) // 2
        z_index_par = len(zs_par) // 2
    else:
        z_index_seq = z_index
        z_index_par = z_index
    if z_index_seq >= len(zs_seq) or z_index_par >= len(zs_par):
        print("Índice de z fuera de rango para comparación 3D.")
        return
    t_seq = times_seq[time_index]
    t_par = times_par[time_index]
    z_seq = zs_seq[z_index_seq]
    z_par = zs_par[z_index_par]
    subset_seq = df_seq[(df_seq['time'] == t_seq) & (df_seq['z'] == z_seq)].sort_values(['x', 'y'])
    subset_par = df_par[(df_par['time'] == t_par) & (df_par['z'] == z_par)].sort_values(['x', 'y'])
    if subset_seq.empty or subset_par.empty:
        print("No hay datos para el tiempo y plano z seleccionados.")
        return
    x_seq = np.sort(subset_seq['x'].unique())
    y_seq = np.sort(subset_seq['y'].unique())
    x_par = np.sort(subset_par['x'].unique())
    y_par = np.sort(subset_par['y'].unique())
    X_seq, Y_seq = np.meshgrid(x_seq, y_seq)
    X_par, Y_par = np.meshgrid(x_par, y_par)
    Z_seq = subset_seq.pivot(index='y', columns='x', values='temperature').values
    Z_par = subset_par.pivot(index='y', columns='x', values='temperature').values
    fig, axs = plt.subplots(1, 2, figsize=(12,5))
    cs1 = axs[0].contourf(X_seq, Y_seq, Z_seq, 20, cmap='hot')
    fig.colorbar(cs1, ax=axs[0])
    axs[0].set_title(f"Secuencial t={t_seq:.3f}s, z={z_seq:.3f}m")
    axs[0].set_xlabel("x (m)")
    axs[0].set_ylabel("y (m)")
    cs2 = axs[1].contourf(X_par, Y_par, Z_par, 20, cmap='hot')
    fig.colorbar(cs2, ax=axs[1])
    axs[1].set_title(f"Paralelo t={t_par:.3f}s, z={z_par:.3f}m")
    axs[1].set_xlabel("x (m)")
    axs[1].set_ylabel("y (m)")
    plt.suptitle("Comparación Difusión de Calor 3D (Secuencial vs Paralelo)")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Comparación 3D guardada en {save_path}")

if __name__ == "__main__":
    plot_1d_heat("heat_results.csv")
    plot_2d_heat("heat2d_results.csv", time_index=0)
    # plot_3d_heat("heat3d_results.csv", time_index=0, z_index=None)  # Puedes comentar esta línea si quieres solo la 3D real
    plot_3d_heat_surface("heat3d_results.csv", time_index=0)
    # Comparación 1D
    plot_1d_comparison("heat_results_secuencial.csv", "heat_results.csv", save_path="comparacion_1d.png")
    # Comparación 2D
    plot_2d_comparison("heat2d_results_secuencial.csv", "heat2d_results.csv", time_index=0, save_path="comparacion_2d.png")
    # Comparación 3D
    plot_3d_comparison("heat3d_results_secuencial.csv", "heat3d_results.csv", time_index=0, z_index=None, save_path="comparacion_3d.png")
    print("Imágenes de comparación guardadas como PNG.")
    # input("Presiona Enter para cerrar las gráficas...") # Ya no es necesario si solo guardas imágenes
