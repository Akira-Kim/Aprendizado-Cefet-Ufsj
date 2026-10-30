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

def encontrar_proxima_colisao(ponto, direcao):
    a = np.dot(direcao, direcao)
    b = 2 * np.dot(direcao, ponto - centro)
    c = np.dot(ponto - centro, ponto - centro) - raio**2
    
    discriminant = b**2 - 4*a*c
    if discriminant <= 0:
        return None
    
    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)

    t = max(t1, t2) if max(t1, t2) > 0 else min(t1, t2)
    return ponto + t * direcao if t > 0 else None

# === Variáveis de Estado ===
class EstadoSimulacao:
    def __init__(self):
        self.pos = np.array([5.0, 2.25])
        self.vel = np.array([0.8, 0.6])
        self.trajetoria = [self.pos.copy()]
        self.angulos = []
        self.colisoes = []
        self.fase = 0
        self.ponto_anterior = None
        self.tangente_anterior = None
        self.proximo_ponto = None
        self.contador_colisoes = 0
        self.ultima_colisao = None

estado = EstadoSimulacao()

# === Configuração do Gráfico ===
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={'width_ratios': [3, 1]})

theta_plot = np.linspace(0, 2*np.pi, 100)
circ_plot = circulo(theta_plot)
linha_circular, = ax.plot(circ_plot[0, :], circ_plot[1, :], color="black", label="Círculo")

bolinha, = ax.plot([], [], 'ro', markersize=6)
trajeto, = ax.plot([], [], 'r-', linewidth=1)
linha_tangente, = ax.plot([], [], 'g--', linewidth=1, alpha=0.5)
ponto_alvo, = ax.plot([], [], 'go', markersize=8, alpha=0.5)
texto_angulo = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                      bbox=dict(facecolor='white', alpha=0.7))
texto_fase = ax.text(0.02, 0.85, '', transform=ax.transAxes, fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.7))

ax.set_xlim(centro[0]-raio-1, centro[0]+raio+1)
ax.set_ylim(centro[1]-raio-1, centro[1]+raio+1)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Simulação Ajustada")

plot_angulo, = ax2.plot([], [], 'bo-', markersize=3)
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 180)
ax2.set_xlabel("Número da Colisão")
ax2.set_ylabel("Ângulo (°)")
ax2.grid(True)

# === Animação ===
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
        
        estado.contador_colisoes += 1
        estado.ultima_colisao = ponto_colisao
        
        if estado.fase == 0:
            estado.vel = refletir_vetor(estado.vel, normal)
            estado.fase = 1
            texto_fase.set_text('Fase: 1 - Salvar ponto e calcular tangente')
            
        elif estado.fase == 1:
            estado.ponto_anterior = ponto_colisao
            estado.tangente_anterior = tangente
            estado.proximo_ponto = encontrar_proxima_colisao(ponto_colisao, tangente)
            estado.fase = 2
            texto_fase.set_text('Fase: 2 - Mover para tangente antes de refletir')
            
        elif estado.fase == 2:
            estado.vel = estado.tangente_anterior * 0.8  # Move temporariamente na tangente
            estado.fase = 1  # Volta para a fase 1
            texto_fase.set_text('Fase: 1 - Salvar ponto e calcular nova direção')
        
        angulo = calcula_angulo(-estado.vel, normal)
        estado.angulos.append(angulo)
        estado.colisoes.append(estado.contador_colisoes)
        
        texto_angulo.set_text(f"Colisão {estado.contador_colisoes}\nÂngulo: {angulo:.1f}°")
    else:
        estado.pos = nova_pos
    
    estado.trajetoria.append(estado.pos.copy())

    bolinha.set_data(estado.pos[0], estado.pos[1])
    trajeto.set_data([p[0] for p in estado.trajetoria], [p[1] for p in estado.trajetoria])
    
    return bolinha, trajeto

ani = FuncAnimation(fig, update, frames=1000, interval=20)
plt.tight_layout()
plt.show()
