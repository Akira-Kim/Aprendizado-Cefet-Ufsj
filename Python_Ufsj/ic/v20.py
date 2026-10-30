import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

def encontrar_colisao(ponto, direcao):
    """Encontra o próximo ponto de colisão com o círculo"""
    a = np.dot(direcao, direcao)
    b = 2 * np.dot(direcao, ponto - centro)
    c = np.dot(ponto - centro, ponto - centro) - raio**2
    
    discriminant = b**2 - 4*a*c
    if discriminant <= 0:
        return None
    
    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)
    
    # Escolhe o menor t positivo (mais próximo)
    t = min(t for t in [t1, t2] if t > 1e-5)
    return ponto + t * direcao

# === Estado da Simulação ===
class EstadoBilhar:
    def __init__(self):
        # Posição inicial (fora do círculo para evitar colisão imediata)
        self.pos = np.array([3.0, 2.25])
        # Velocidade inicial (normalizada)
        self.vel = np.array([1.0, 0.5])
        self.vel = self.vel / np.linalg.norm(self.vel) * 0.5  # Velocidade constante
        self.trajetoria = [self.pos.copy()]
        self.angulos_colisao = []
        self.num_colisoes = 0
        self.ultima_colisao = None
        self.ultimo_angulo = None

estado = EstadoBilhar()

# === Configuração do Gráfico ===
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={'width_ratios': [3, 1]})

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
angulo_plot, = ax2.plot([], [], 'bo-', markersize=4)
ax2.set_xlim(0, 50)
ax2.set_ylim(0, 180)
ax2.set_xlabel("Número da Colisão")
ax2.set_ylabel("Ângulo de Colisão (°)")
ax2.grid(True)
ax2.set_title("Ângulos de Colisão")

ax.set_xlim(centro[0]-raio-1, centro[0]+raio+1)
ax.set_ylim(centro[1]-raio-1, centro[1]+raio+1)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Bilhar Simplético Circular")

# === Animação ===
def init():
    bolinha.set_data([], [])
    trajeto.set_data([], [])
    normal_linha.set_data([], [])
    vel_linha.set_data([], [])
    texto_info.set_text('')
    angulo_plot.set_data([], [])
    return bolinha, trajeto, normal_linha, vel_linha, texto_info, angulo_plot

def update(frame):
    dt = 0.05
    
    # Movimento livre
    nova_pos = estado.pos + estado.vel * dt
    
    # Verifica colisão com o círculo
    distancia = np.linalg.norm(nova_pos - centro)
    if distancia >= raio:
        # Encontra o ponto exato da colisão
        t_colisao = np.arctan2(estado.pos[1]-centro[1], estado.pos[0]-centro[0])
        ponto_colisao = ponto_circulo(t_colisao)
        
        # Calcula normal e tangente no ponto de colisão
        normal = normal_circulo(t_colisao)
        tangente = tangente_circulo(t_colisao)
        
        # Atualiza estado
        estado.pos = ponto_colisao
        estado.vel = refletir_vetor(estado.vel, normal)
        estado.ultima_colisao = ponto_colisao
        
        # Calcula ângulo de colisão (entre direção incidente e normal)
        angulo = np.degrees(np.arccos(np.dot(-estado.vel/np.linalg.norm(estado.vel), normal)))
        estado.ultimo_angulo = angulo
        estado.angulos_colisao.append(angulo)
        estado.num_colisoes += 1
        
        # Atualiza texto
        texto_info.set_text(f"Colisão: {estado.num_colisoes}\nÂngulo: {angulo:.1f}°")
    else:
        estado.pos = nova_pos
    
    estado.trajetoria.append(estado.pos.copy())
    
    # Atualiza gráficos
    bolinha.set_data(estado.pos[0], estado.pos[1])
    trajeto.set_data([p[0] for p in estado.trajetoria], [p[1] for p in estado.trajetoria])
    
    # Mostra normal e velocidade na última colisão
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
    
    # Atualiza gráfico de ângulos
    if estado.angulos_colisao:
        angulo_plot.set_data(
            range(1, estado.num_colisoes+1),
            estado.angulos_colisao
        )
        ax2.set_xlim(0, max(10, estado.num_colisoes+1))
    
    return bolinha, trajeto, normal_linha, vel_linha, texto_info, angulo_plot

ani = FuncAnimation(fig, update, frames=1000, init_func=init, blit=True, interval=20)
plt.tight_layout()
plt.show()