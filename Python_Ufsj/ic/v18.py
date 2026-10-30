import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# === Parâmetros do Círculo ===
centro = np.array([5.0, 2.25])
raio = 2.0

# === Funções do Círculo ===
def circulo(t):
    return centro.reshape(2, 1) + raio * np.vstack([np.cos(t), np.sin(t)])

def ponto_circulo(t):
    return centro + raio * np.array([np.cos(t), np.sin(t)])

def derivada_circulo(t):
    return raio * np.array([-np.sin(t), np.cos(t)])

# === Funções de Apoio ===
def normal_circulo(t):
    return np.array([np.cos(t), np.sin(t)])

def tangente_circulo(t):
    derivada = derivada_circulo(t)
    return derivada / np.linalg.norm(derivada)

def refletir_vetor(v, normal):
    normal = normal / np.linalg.norm(normal)
    return v - 2 * np.dot(v, normal) * normal

def calcula_angulo(v1, v2):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    cos_theta = np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)
    return np.degrees(np.arccos(cos_theta))

# === Variáveis de Estado ===
class EstadoSimulacao:
    def __init__(self):
        self.pos = np.array([5.0, 2.25])
        self.vel = np.array([0.8, 0.6])
        self.trajetoria = [self.pos.copy()]
        self.angulos = []
        self.colisoes = []
        self.fase = 0  # 0: normal, 1: medindo, 2: simplético
        self.ponto_fase1 = None
        self.tangente_fase1 = None
        self.limite_fase2 = None

estado = EstadoSimulacao()

# === Configuração do Gráfico ===
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={'width_ratios': [3, 1]})

theta_plot = np.linspace(0, 2*np.pi, 100)
circ_plot = circulo(theta_plot)
linha_circular, = ax.plot(circ_plot[0, :], circ_plot[1, :], color="black", label="Círculo")

bolinha, = ax.plot([], [], 'ro', markersize=6)
trajeto, = ax.plot([], [], 'r-', linewidth=1)
texto_angulo = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                      bbox=dict(facecolor='white', alpha=0.7))
texto_fase = ax.text(0.02, 0.85, '', transform=ax.transAxes, fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.7))

ax.set_xlim(centro[0]-raio-1, centro[0]+raio+1)
ax.set_ylim(centro[1]-raio-1, centro[1]+raio+1)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Simulação Simplética em 3 Fases")

plot_angulo, = ax2.plot([], [], 'bo-', markersize=3)
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 180)
ax2.set_xlabel("Número da Colisão")
ax2.set_ylabel("Ângulo (°)")
ax2.grid(True)

# === Animação ===
def init():
    bolinha.set_data([], [])
    trajeto.set_data([], [])
    texto_angulo.set_text('')
    texto_fase.set_text('Fase: 0 - Normal')
    plot_angulo.set_data([], [])
    return bolinha, trajeto, texto_angulo, texto_fase, plot_angulo

def update(frame):
    global estado
    
    nova_pos = estado.pos + estado.vel * 0.05
    distancia = np.linalg.norm(nova_pos - centro)
    
    if distancia >= raio * 0.99:  # Detecção de colisão
        t = np.arctan2(estado.pos[1]-centro[1], estado.pos[0]-centro[0])
        ponto_colisao = ponto_circulo(t)
        estado.pos = ponto_colisao
        normal = normal_circulo(t)
        tangente = tangente_circulo(t)
        
        # Lógica das três fases
        if estado.fase == 0:  # Fase 1: Colisão normal
            estado.vel = refletir_vetor(estado.vel, normal)
            estado.ponto_fase1 = ponto_colisao
            estado.tangente_fase1 = tangente
            estado.fase = 1
            texto_fase.set_text('Fase: 1 - Medindo')
            
        elif estado.fase == 1:  # Fase 2: Determinar limite
            # Calcula ponto limite na direção da tangente anterior
            estado.limite_fase2 = estado.ponto_fase1 + estado.tangente_fase1 * raio * 1.5
            estado.fase = 2
            texto_fase.set_text('Fase: 2 - Simplético')
            
        else:  # Fase 3: Movimento simplético
            # Move diretamente para o ponto limite
            direcao = estado.limite_fase2 - estado.pos
            estado.vel = direcao / np.linalg.norm(direcao) * 0.8
            estado.fase = 0  # Reinicia o ciclo
            texto_fase.set_text('Fase: 0 - Normal')
        
        # Registra colisão
        angulo = calcula_angulo(-estado.vel, normal)
        estado.angulos.append(angulo)
        estado.colisoes.append(len(estado.angulos))
        
        texto_angulo.set_text(f"Colisão {len(estado.angulos)}\nÂngulo: {angulo:.1f}°")
        
        if estado.angulos:
            plot_angulo.set_data(estado.colisoes, estado.angulos)
    else:
        estado.pos = nova_pos
    
    estado.trajetoria.append(estado.pos.copy())
    
    # Atualiza gráficos
    bolinha.set_data(estado.pos[0], estado.pos[1])
    trajeto.set_data([p[0] for p in estado.trajetoria], [p[1] for p in estado.trajetoria])
    
    # Desenha ponto limite quando na fase 3
    if estado.fase == 2:
        ax.plot(estado.limite_fase2[0], estado.limite_fase2[1], 'go', markersize=8, alpha=0.5)
    
    return bolinha, trajeto, texto_angulo, texto_fase, plot_angulo

ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=True, interval=20)
plt.tight_layout()
plt.show()