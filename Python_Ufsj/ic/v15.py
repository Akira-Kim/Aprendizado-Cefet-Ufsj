import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# === Função parametrizada padrão: Círculo ===
def curva_parametrizada(t):
    x = 1.5 + np.cos(t)
    y = 1.5 + np.sin(t)
    return np.array([x, y])

# === Derivada numérica para calcular tangentes ===
def derivada_parametrizada(t):
    dx_dt = -np.sin(t)
    dy_dt = np.cos(t)
    return np.array([dx_dt, dy_dt]) / np.linalg.norm([dx_dt, dy_dt])

# === Parâmetros da simulação ===
dt = 0.01
pos = np.array([1.5, 1.5])  # Começa no centro
vel = np.array([-1.0, 0])   # Movimento inicial da direita para a esquerda
trajetoria = [pos.copy()]
pontos_colisao = []
tangentes_visuais = []
primeira_colisao = True  # Flag para indicar a primeira colisão

# === Configuração do gráfico ===
fig, ax = plt.subplots(figsize=(7, 7))
ts = np.linspace(0, 2 * np.pi, 500)
xs, ys = curva_parametrizada(ts)
linha_curva, = ax.plot(xs, ys, color="black", label="Curva Parametrizada (Círculo)")
bolinha, = ax.plot([], [], 'ro', markersize=5)
trajeto, = ax.plot([], [], 'r-', linewidth=0.5)
ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Bilhar com Reflexão Tangencial")
ax.legend(loc='upper right')
ax.grid(True)
ax.set_aspect("equal")

# === Função de atualização ===
def update(frame):
    global pos, vel, pontos_colisao, tangentes_visuais, primeira_colisao

    nova_pos = pos + vel * dt

    # Verifica colisão com a curva
    distancias = np.linalg.norm(curva_parametrizada(ts) - nova_pos[:, None], axis=0)
    t_colisao = ts[np.argmin(distancias)]

    if np.min(distancias) <= 0.03:  # Impacto detectado
        pontos_colisao.append(curva_parametrizada(t_colisao))
        tangente = derivada_parametrizada(t_colisao)

        if primeira_colisao:
            # Reflexão simples na primeira colisão
            vel = -vel  
            primeira_colisao = False  
        elif len(pontos_colisao) > 1:
            # Após a primeira colisão, segue a tangente da colisão anterior
            vel = tangente.copy()

            # Desenha temporariamente a tangente entre os pontos de colisão
            linha_tangente, = ax.plot(
                [pontos_colisao[-2][0], pontos_colisao[-1][0]],
                [pontos_colisao[-2][1], pontos_colisao[-1][1]],
                linestyle="--", color="blue"
            )
            tangentes_visuais.append(linha_tangente)

    pos += vel * dt
    trajetoria.append(pos.copy())

    traj = np.array(trajetoria)
    bolinha.set_data(pos[0], pos[1])
    trajeto.set_data(traj[:, 0], traj[:, 1])

    return bolinha, trajeto, *tangentes_visuais

ani = FuncAnimation(fig, update, frames=600, interval=10)
plt.show()
