import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# === Funções de apoio ===
def refletir_vetor(v, normal):
    normal = normal / np.linalg.norm(normal)
    return v - 2 * np.dot(v, normal) * normal

def derivada_numerica(f, x, dx=1e-5):
    return (f(x + dx) - f(x - dx)) / (2 * dx)

def normal_funcao(f, x):
    dfdx = derivada_numerica(f, x)
    normal = np.array([-dfdx, 1])
    return normal / np.linalg.norm(normal)

def tangente_funcao(f, x):
    dfdx = derivada_numerica(f, x)
    return np.array([1, dfdx]) / np.linalg.norm([1, dfdx])

# === Definições das curvas ===
def curva(x):
    return 0.5 * np.sin(x) + 1.5  # Curva inferior

def curva_superior(x):
    return 3.0 + 0.5 * np.sin(x)  # Curva superior (opcional)

# === Configuração inicial ===
usar_segunda_curva = True # <<< ALTERE AQUI para True (2 curvas) ou False (apenas 1 curva)

# Posição e velocidade inicial da bolinha
pos = np.array([1.0, curva(1.0) + 0.1])
vel = np.array([1.0, -0.4])
primeira_colisao = True

# Variáveis de simulação
dt = 0.01
trajetoria = [pos.copy()]
angulos = []
perimetros = []

# === Configuração dos gráficos ===
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={'width_ratios': [3, 1]})
xs = np.linspace(0, 10, 500)

# Desenha a curva inferior
linha_inferior, = ax.plot(xs, curva(xs), color="black", label="Espelho Inferior: curva(x)")

# Se ativado, desenha a curva superior
if usar_segunda_curva:
    linha_superior, = ax.plot(xs, curva_superior(xs), color="gray", linestyle="--", label="Espelho Superior")
else:
    linha_superior, = ax.plot([], [])  # Placeholder vazio

# Elementos gráficos
bolinha, = ax.plot([], [], 'ro')               # A bolinha vermelha
trajeto, = ax.plot([], [], 'r-', linewidth=0.5)  # Linha de trajetória
texto_angulo = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                       bbox=dict(facecolor='white', alpha=0.7))

# Configurações do gráfico principal
ax.set_xlim(0, 10)
ax.set_ylim(0, 4.5)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Simulação: Bilhar Simplético")
ax.legend(loc='upper right')
ax.grid(True)
ax.set_aspect("equal")

# === Gráfico lateral de ângulos ===
plot_angulo, = ax2.plot([], [], 'bo-', markersize=3)
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 180)
ax2.set_xlabel("Perímetro")
ax2.set_ylabel("Ângulo (°)")
ax2.set_title("Ângulo por posição no perímetro")
ax2.grid(True)

# === Animação ===
vetores_visuais = []

def init():
    bolinha.set_data([], [])
    trajeto.set_data([], [])
    texto_angulo.set_text('')
    plot_angulo.set_data([], [])
    return bolinha, trajeto, texto_angulo, plot_angulo

def calcula_angulo(v1, v2):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    cos_theta = np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)
    return np.degrees(np.arccos(cos_theta))

def update(frame):
    global pos, vel, primeira_colisao, vetores_visuais

    nova_pos = pos + vel * dt
    texto = ''

    def calcula_perimetro(p):
        return (p[0] % 10) / 10 * 100  # Normaliza o perímetro entre 0 e 100

    # Remove vetores visuais antigos
    for vec in vetores_visuais:
        vec.remove()
    vetores_visuais.clear()

    # === Reflexão na curva inferior ===
    if nova_pos[1] <= curva(nova_pos[0]):
        base = np.array([nova_pos[0], curva(nova_pos[0])])
        normal = normal_funcao(curva, nova_pos[0])
        tangente = tangente_funcao(curva, nova_pos[0])
        v_entrada = vel.copy()

        if primeira_colisao:
            vel = tangente.copy()
            primeira_colisao = False
        else:
            vel = tangente.copy()

        v_saida = vel.copy()

        angulo = calcula_angulo(v_entrada, v_saida)
        texto = f"Ângulo de Ricochete: {angulo:.1f}°"
        angulos.append(angulo)
        perimetros.append(calcula_perimetro(base))

        # Vetores
        vetores_visuais.extend([
            ax.plot([base[0], base[0] + tangente[0]], [base[1], base[1] + tangente[1]], color='skyblue', linestyle='--', linewidth=1.5)[0],
            ax.plot([base[0], base[0] + normal[0]], [base[1], base[1] + normal[1]], color='orange', linestyle='--', linewidth=1.5)[0],
            ax.plot([base[0], base[0] - v_entrada[0]], [base[1], base[1] - v_entrada[1]], color='green', linewidth=1.2)[0],
            ax.plot([base[0], base[0] + v_saida[0]], [base[1], base[1] + v_saida[1]], color='purple', linewidth=1.2)[0],
        ])

    # === Reflexão na curva superior (se ativada) ===
    elif usar_segunda_curva and nova_pos[1] >= curva_superior(nova_pos[0]):
        base = np.array([nova_pos[0], curva_superior(nova_pos[0])])
        normal = -normal_funcao(curva_superior, nova_pos[0])
        tangente = tangente_funcao(curva_superior, nova_pos[0])
        v_entrada = vel.copy()

        vel = tangente.copy()
        v_saida = vel.copy()

        angulo = calcula_angulo(v_entrada, v_saida)
        texto = f"Ângulo de Ricochete: {angulo:.1f}°"
        angulos.append(angulo)
        perimetros.append(calcula_perimetro(base))

        # Vetores
        vetores_visuais.extend([
            ax.plot([base[0], base[0] + tangente[0]], [base[1], base[1] + tangente[1]], color='skyblue', linestyle='--', linewidth=1.5)[0],
            ax.plot([base[0], base[0] + normal[0]], [base[1], base[1] + normal[1]], color='orange', linestyle='--', linewidth=1.5)[0],
            ax.plot([base[0], base[0] - v_entrada[0]], [base[1], base[1] - v_entrada[1]], color='green', linewidth=1.2)[0],
            ax.plot([base[0], base[0] + v_saida[0]], [base[1], base[1] + v_saida[1]], color='purple', linewidth=1.2)[0],
        ])

    # Atualiza posição e trajetória
    pos += vel * dt
    trajetoria.append(pos.copy())
    traj = np.array(trajetoria)

    # Atualiza gráficos
    bolinha.set_data(pos[0], pos[1])
    trajeto.set_data(traj[:, 0], traj[:, 1])

    if angulos:
        texto_angulo.set_text(f"Último: {angulos[-1]:.1f}°")
        plot_angulo.set_data(perimetros, angulos)

    return bolinha, trajeto, texto_angulo, plot_angulo, *vetores_visuais

# === Execução da animação ===
ani = FuncAnimation(fig, update, frames=600, init_func=init, blit=True, interval=10)
plt.tight_layout()
plt.show()
