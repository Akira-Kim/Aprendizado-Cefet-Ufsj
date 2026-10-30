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
    # Encontra a interseção da reta com o círculo
    a = np.dot(direcao, direcao)
    b = 2 * np.dot(direcao, ponto - centro)
    c = np.dot(ponto - centro, ponto - centro) - raio**2
    
    discriminant = b**2 - 4*a*c
    if discriminant <= 0:
        return None
    
    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)
    
    # Escolhe o ponto mais distante na direção do vetor
    t = t1 if abs(t1) > abs(t2) else t2
    return ponto + t * direcao

# === Variáveis de Estado ===
class EstadoSimulacao:
    def __init__(self):
        self.pos = np.array([5.0, 2.25])
        self.vel = np.array([0.8, 0.6])  # Velocidade inicial
        self.trajetoria = [self.pos.copy()]
        self.angulos = []
        self.colisoes = []
        self.fase = 0  # 0: reflexão normal, 1: salvar ponto, 2: mover para tangente
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
ax.set_title("Simulação com 3 Fases Corrigida")

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
    linha_tangente.set_data([], [])
    ponto_alvo.set_data([], [])
    texto_angulo.set_text('')
    texto_fase.set_text('Fase: 0 - Reflexão normal')
    plot_angulo.set_data([], [])
    return bolinha, trajeto, linha_tangente, ponto_alvo, texto_angulo, texto_fase, plot_angulo

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
        
        # Registra colisão
        estado.contador_colisoes += 1
        estado.ultima_colisao = ponto_colisao
        
        # Lógica das três fases
        if estado.fase == 0:  # Fase 0: Apenas reflexão normal (entrada única)
            estado.vel = refletir_vetor(estado.vel, normal)
            estado.fase = 1  # Próxima fase
            texto_fase.set_text('Fase: 1 - Salvar ponto e calcular tangente')
            
        elif estado.fase == 1:  # Fase 1: Salva ponto e calcula próximo alvo
            estado.ponto_anterior = ponto_colisao
            estado.tangente_anterior = tangente
            estado.proximo_ponto = encontrar_proxima_colisao(ponto_colisao, tangente)
            estado.fase = 2  # Próxima fase
            texto_fase.set_text('Fase: 2 - Mover para ponto alvo')
            
        elif estado.fase == 2:  # Fase 2: Move para o ponto alvo
            # Primeiro aplica a reflexão normal
            estado.vel = refletir_vetor(estado.vel, normal)
            # Depois calcula nova direção para o ponto alvo
            if estado.proximo_ponto is not None:
                direcao = estado.proximo_ponto - estado.pos
                estado.vel = direcao / np.linalg.norm(direcao) * 0.8
            estado.fase = 1  # Volta para fase 1
            texto_fase.set_text('Fase: 1 - Salvar ponto e calcular tangente')
        
        # Calcula ângulo apenas para registro
        angulo = calcula_angulo(-estado.vel, normal)
        estado.angulos.append(angulo)
        estado.colisoes.append(estado.contador_colisoes)
        
        texto_angulo.set_text(f"Colisão {estado.contador_colisoes}\nÂngulo: {angulo:.1f}°")
    else:
        estado.pos = nova_pos
    
    estado.trajetoria.append(estado.pos.copy())
    
    # Atualiza visualização da tangente e ponto alvo
    if estado.fase >= 1 and estado.proximo_ponto is not None:
        linha_tangente.set_data(
            [estado.ponto_anterior[0], estado.proximo_ponto[0]],
            [estado.ponto_anterior[1], estado.proximo_ponto[1]]
        )
        ponto_alvo.set_data([estado.proximo_ponto[0]], [estado.proximo_ponto[1]])
    else:
        linha_tangente.set_data([], [])
        ponto_alvo.set_data([], [])
    
    # Atualiza gráficos
    bolinha.set_data(estado.pos[0], estado.pos[1])
    trajeto.set_data([p[0] for p in estado.trajetoria], [p[1] for p in estado.trajetoria])
    
    # Atualiza gráfico de ângulos
    if estado.angulos:
        plot_angulo.set_data(estado.colisoes, estado.angulos)
        ax2.set_xlim(0, max(10, estado.contador_colisoes+1))
    
    return bolinha, trajeto, linha_tangente, ponto_alvo, texto_angulo, texto_fase, plot_angulo

ani = FuncAnimation(fig, update, frames=1000, init_func=init, blit=True, interval=20)
plt.tight_layout()
plt.show()