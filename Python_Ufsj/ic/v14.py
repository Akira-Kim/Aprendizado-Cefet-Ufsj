import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# === Funções de apoio ===
def derivada_numerica(f, t, dt=1e-5):
    return (f(t + dt) - f(t - dt)) / (2 * dt)

def normal_parametrizada(dx_dt, dy_dt):
    normal = np.array([-dy_dt, dx_dt])
    return normal / np.linalg.norm(normal)

def tangente_parametrizada(dx_dt, dy_dt):
    tangente = np.array([dx_dt, dy_dt])
    return tangente / np.linalg.norm(tangente)

# === Função da curva parametrizada ===
def curva_parametrizada(t, amp):
    x = t
    y = amp * np.sin(t) + 1.5
    return np.array([x, y])

# === Parâmetros iniciais ===
amplitude = 0.5  # Valor inicial ajustável
dt = 0.01
trajetoria = []

# === Setup do gráfico ===
fig, ax = plt.subplots(figsize=(7, 5))
plt.subplots_adjust(bottom=0.25)  # Ajuste para incluir o slider
ts = np.linspace(0, 10, 500)
xs, ys = curva_parametrizada(ts, amplitude)
linha_curva, = ax.plot(xs, ys, color="black", label="Curva Regular Parametrizada")
bolinha, = ax.plot([], [], 'ro')
trajeto, = ax.plot([], [], 'r-', linewidth=0.5)

ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Bilhar com Curva Parametrizada Regular")
ax.legend(loc='upper right')
ax.grid(True)
ax.set_aspect("equal")

# === Slider para ajuste da curva ===
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
slider = Slider(ax_slider, 'Amplitude', 0.1, 1.0, valinit=amplitude)

def update_slider(val):
    global amplitude
    amplitude = val
    xs, ys = curva_parametrizada(ts, amplitude)
    linha_curva.set_xdata(xs)
    linha_curva.set_ydata(ys)

slider.on_changed(update_slider)

# === Animação ===
pos = curva_parametrizada(1.0, amplitude)
vel = np.array([1.0, -0.4])

def init():
    bolinha.set_data([], [])
    trajeto.set_data([], [])
    return bolinha, trajeto

def update(frame):
    global pos, vel

    nova_pos = pos + vel * dt
    t_atual = nova_pos[0]

    # Reflexão na curva parametrizada
    dx_dt = derivada_numerica(lambda t: curva_parametrizada(t, amplitude)[0], t_atual)
    dy_dt = derivada_numerica(lambda t: curva_parametrizada(t, amplitude)[1], t_atual)

    if nova_pos[1] <= curva_parametrizada(t_atual, amplitude)[1]:
        normal = normal_parametrizada(dx_dt, dy_dt)
        tangente = tangente_parametrizada(dx_dt, dy_dt)
        vel = tangente.copy()

    pos += vel * dt
    trajetoria.append(pos.copy())

    traj = np.array(trajetoria)
    bolinha.set_data(pos[0], pos[1])
    trajeto.set_data(traj[:, 0], traj[:, 1])

    return bolinha, trajeto

ani = FuncAnimation(fig, update, frames=600, init_func=init, blit=True, interval=10)
plt.show()
