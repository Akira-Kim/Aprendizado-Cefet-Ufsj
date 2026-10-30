import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# === Parâmetros do Círculo ===
centro = np.array([5.0, 2.25])
raio = 2.0

# === Funções do Círculo ===
def ponto_circulo(t):
    return centro + raio * np.array([np.cos(t), np.sin(t)])

def normal_circulo(t):
    return np.array([np.cos(t), np.sin(t)])

def tangente_circulo(t):
    return np.array([-np.sin(t), np.cos(t)])

def refletir_vetor(v, normal):
    """Reflete o vetor v em relação à normal (lei da reflexão)"""
    normal = normal / np.linalg.norm(normal)
    return v - 2 * np.dot(v, normal) * normal

# === Estado da Simulação ===
class EstadoBilhar:
    def __init__(self):
        self.pos = np.array([3.0, 2.25])
        self.vel = np.array([1.0, 0.5])
        self.vel = self.vel / np.linalg.norm(self.vel) * 0.5
        self.trajetoria = [self.pos.copy()]
        self.angulos_colisao = []
        self.num_colisoes = 0
        self.ultima_colisao = None
        self.ultimo_angulo = None
        self.pausado = False

estado = EstadoBilhar()

# === Configuração do Gráfico ===
fig = plt.figure(figsize=(14, 8))
gs = fig.add_gridspec(2, 2, height_ratios=[3, 1], width_ratios=[3, 1])

ax = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax_controles = fig.add_subplot(gs[1, :])

# Círculo
theta_plot = np.linspace(0, 2*np.pi, 100)
circ_plot = np.column_stack([centro[0] + raio*np.cos(theta_plot), 
                            centro[1] + raio*np.sin(theta_plot)])
ax.plot(circ_plot[:, 0], circ_plot[:, 1], 'k-', linewidth=2)

# Elementos da animação
bolinha, = ax.plot([], [], 'ro', markersize=8)
trajeto, = ax.plot([], [], 'r-', linewidth=1, alpha=0.7)
normal_linha, = ax.plot([], [], 'b--', linewidth=1, alpha=0.5)
vel_linha, = ax.plot([], [], 'g-', linewidth=1, alpha=0.7)
texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.7))

# Gráfico de ângulos
angulo_plot, = ax2.plot([], [], 'ko', markersize=4)
ax2.set_xlabel("Número da Colisão")
ax2.set_ylabel("Ângulo de Colisão (°)")
ax2.grid(True)
ax2.set_title("Ângulos de Colisão")

ax.set_xlim(centro[0]-raio-1, centro[0]+raio+1)
ax.set_ylim(centro[1]-raio-1, centro[1]+raio+1)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Bilhar Simplético Circular")

# === Controles Interativos ===
plt.subplots_adjust(bottom=0.3)

# Sliders
ax_posx = plt.axes([0.2, 0.22, 0.6, 0.03])
ax_posy = plt.axes([0.2, 0.18, 0.6, 0.03])
ax_angulo = plt.axes([0.2, 0.14, 0.6, 0.03])
ax_velocidade = plt.axes([0.2, 0.10, 0.6, 0.03])

slider_posx = Slider(ax_posx, 'Posição X', centro[0]-raio-0.9, centro[0]+raio+0.9, valinit=3.0, valstep=0.1)
slider_posy = Slider(ax_posy, 'Posição Y', centro[1]-raio-0.9, centro[1]+raio+0.9, valinit=2.25, valstep=0.1)
slider_angulo = Slider(ax_angulo, 'Ângulo (graus)', 0, 360, valinit=30, valstep=1)
slider_velocidade = Slider(ax_velocidade, 'Velocidade', 0.1, 2.0, valinit=0.5, valstep=0.1)

# Botões
ax_botao_reset = plt.axes([0.2, 0.02, 0.15, 0.05])
ax_botao_pause = plt.axes([0.4, 0.02, 0.15, 0.05])
ax_botao_start = plt.axes([0.6, 0.02, 0.15, 0.05])

botao_reset = Button(ax_botao_reset, 'Reset')
botao_pause = Button(ax_botao_pause, 'Pausar')
botao_start = Button(ax_botao_start, 'Iniciar')

def reset_simulacao(event):
    estado.pos = np.array([slider_posx.val, slider_posy.val])
    angulo_rad = np.radians(slider_angulo.val)
    velocidade = slider_velocidade.val
    estado.vel = np.array([np.cos(angulo_rad), np.sin(angulo_rad)]) * velocidade
    estado.trajetoria = [estado.pos.copy()]
    estado.angulos_colisao = []
    estado.num_colisoes = 0
    estado.ultima_colisao = None
    estado.ultimo_angulo = None
    estado.pausado = False
    ax2.set_xlim(0, 10)  # Reset dos limites do gráfico
    ax2.set_ylim(0, 180)

def pausar_simulacao(event):
    estado.pausado = True

def iniciar_simulacao(event):
    estado.pausado = False

botao_reset.on_clicked(reset_simulacao)
botao_pause.on_clicked(pausar_simulacao)
botao_start.on_clicked(iniciar_simulacao)

def update_velocidade(val):
    angulo_rad = np.radians(slider_angulo.val)
    velocidade = slider_velocidade.val
    estado.vel = np.array([np.cos(angulo_rad), np.sin(angulo_rad)]) * velocidade

def update_posicao(val):
    estado.pos = np.array([slider_posx.val, slider_posy.val])
    estado.trajetoria = [estado.pos.copy()]

slider_angulo.on_changed(update_velocidade)
slider_velocidade.on_changed(update_velocidade)
slider_posx.on_changed(update_posicao)
slider_posy.on_changed(update_posicao)

def ajustar_zoom():
    """Ajusta o zoom do gráfico de ângulos dinamicamente"""
    if not estado.angulos_colisao:
        return
    
    # Ajuste do eixo X
    num_pontos = len(estado.angulos_colisao)
    if num_pontos > 40:
        ax2.set_xlim(num_pontos - 40, num_pontos + 2)
    else:
        ax2.set_xlim(0, 42)
    
    # Ajuste do eixo Y
    min_ang = min(estado.angulos_colisao[-40:]) if num_pontos > 0 else 0
    max_ang = max(estado.angulos_colisao[-40:]) if num_pontos > 0 else 180
    
    margem = 10  # Margem de 10 graus
    if max_ang - min_ang < 40:  # Se os ângulos estiverem concentrados
        centro_y = (min_ang + max_ang) / 2
        ax2.set_ylim(max(0, centro_y - 25), min(180, centro_y + 25))
    else:  # Caso contrário, mostra toda a faixa
        ax2.set_ylim(max(0, min_ang - margem), min(180, max_ang + margem))

def init():
    bolinha.set_data([], [])
    trajeto.set_data([], [])
    normal_linha.set_data([], [])
    vel_linha.set_data([], [])
    texto_info.set_text('')
    angulo_plot.set_data([], [])
    return bolinha, trajeto, normal_linha, vel_linha, texto_info, angulo_plot

def update(frame):
    if estado.pausado:
        return bolinha, trajeto, normal_linha, vel_linha, texto_info, angulo_plot
    
    dt = 0.05
    nova_pos = estado.pos + estado.vel * dt
    
    # Verifica colisão com o círculo
    distancia = np.linalg.norm(nova_pos - centro)
    if distancia >= raio:
        t_colisao = np.arctan2(estado.pos[1]-centro[1], estado.pos[0]-centro[0])
        ponto_colisao = ponto_circulo(t_colisao)
        normal = normal_circulo(t_colisao)
        
        estado.pos = ponto_colisao
        estado.vel = refletir_vetor(estado.vel, normal)
        estado.ultima_colisao = ponto_colisao
        
        angulo = np.degrees(np.arccos(np.dot(-estado.vel/np.linalg.norm(estado.vel), normal)))
        estado.ultimo_angulo = angulo
        estado.angulos_colisao.append(angulo)
        estado.num_colisoes += 1
        
        texto_info.set_text(f"Colisão: {estado.num_colisoes}\nÂngulo: {angulo:.1f}°")
        
        # Ajusta o zoom após cada colisão
        ajustar_zoom()
    else:
        estado.pos = nova_pos
    
    estado.trajetoria.append(estado.pos.copy())
    
    # Atualiza gráficos
    bolinha.set_data(estado.pos[0], estado.pos[1])
    trajeto.set_data([p[0] for p in estado.trajetoria], [p[1] for p in estado.trajetoria])
    
    if estado.ultima_colisao is not None:
        t = np.arctan2(estado.ultima_colisao[1]-centro[1], estado.ultima_colisao[0]-centro[0])
        normal = normal_circulo(t)
        normal_linha.set_data(
            [estado.ultima_colisao[0], estado.ultima_colisao[0]+normal[0]],
            [estado.ultima_colisao[1], estado.ultima_colisao[1]+normal[1]]
        )
        vel_linha.set_data(
            [estado.ultima_colisao[0], estado.ultima_colisao[0]+estado.vel[0]],
            [estado.ultima_colisao[1], estado.ultima_colisao[1]+estado.vel[1]]
        )
    
    if estado.angulos_colisao:
        angulo_plot.set_data(
            range(1, estado.num_colisoes+1),
            estado.angulos_colisao
        )
    
    return bolinha, trajeto, normal_linha, vel_linha, texto_info, angulo_plot

ani = FuncAnimation(fig, update, frames=1000, init_func=init, blit=True, interval=20)
plt.tight_layout()
plt.show()