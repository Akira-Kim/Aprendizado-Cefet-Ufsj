import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox, RadioButtons
from matplotlib import gridspec, patches
from scipy.optimize import minimize_scalar


# === Sistema de Funções Paramétricas ===
erro_colisao = 5e-3   # um pouco maior que o dt típico para capturar overshoot

class CurvaParametrica:
    def __init__(self):
        self.curvas = {
            'Círculo': self.circulo,	
            'Elipse': self.elipse            
        }
        self.parametro_a = 1.0
        self.parametro_b = 1.0
        self.curva_atual = 'Círculo'
       
    def __call__(self, t):
        try:
            return self.curvas[self.curva_atual](t)
        except:
            return np.array([0, 0, 0])    
        
    def circulo(self, t):
        return np.array([t, np.cos(t), np.sin(t)])

    def elipse(self, t):
        a, b = self.parametro_a, self.parametro_b
        return np.array([t, a * np.cos(t), b * np.sin(t)])

    def colisao(self, pos):
        if self.curva_atual == 'Círculo':
            return np.abs(pos[0]**2 + pos[1]**2 - 1) < erro_colisao
        if self.curva_atual == 'Elipse':
            return np.abs((pos[0]**2)/(self.parametro_a**2) + (pos[1]**2)/(self.parametro_b**2) - 1) < erro_colisao
        return False

    def intersect_line(self, point, direction):
        """Retorna os valores de lambda onde a reta point + lambda * direction intersecta a curva.
           Sempre retorna 2 valores (um deles ≈ 0 quando point está na curva)."""
        if self.curva_atual == 'Círculo':
            aa = bb = 1.0
        else:
            aa = self.parametro_a
            bb = self.parametro_b

        px, py = point
        dx, dy = direction
        A = (dx / aa)**2 + (dy / bb)**2
        B = 2 * (px * dx / aa**2 + py * dy / bb**2)
        C = (px / aa)**2 + (py / bb)**2 - 1

        disc = B**2 - 4 * A * C
        if disc < 0:
            return []
        if A == 0:
            return [0.0]

        sd = math.sqrt(disc)
        l1 = (-B + sd) / (2 * A)
        l2 = (-B - sd) / (2 * A)
        return [l1, l2]


# === Estado da Simulação ===
class EstadoBilhar:
    def __init__(self):
        self.pausado = True
        self.primeiro_inicio = True        
        self.modo_bilhar = 'Elástico'  # 'Elástico' ou 'Simplético'
        self.pos = np.array([1.0, 0.0])
        self.t = 0.0 
        self.vel = np.array([-1.0, 1.0]) / np.sqrt(2)
        self.angulo_vel = 0.25 * np.pi
        self.velocidade_simulacao = 1.0
        self.curva_parametrica = CurvaParametrica()
        self.curve_points = None
        self.trajetoria = [self.pos.copy()]
        self.trajetoria_aux = []
    
        self.lista_t_colisao = []
        self.lista_angulo_colisao = []
        self.erro = 1e-5        
        self.reset_all = False

    def reset(self):
        self.pausado = True
        self.primeiro_inicio = True
        self.pos = np.array([1.0, 0.0])
        self.t = 0.0 
        self.vel = np.array([-1.0, 1.0]) / np.sqrt(2)
        self.angulo_vel = 0.25 * np.pi
        self.velocidade_simulacao = 1.0
        self.curva_parametrica = CurvaParametrica()
        self.curve_points = None
        self.trajetoria = [self.pos.copy()]
        self.trajetoria_aux = []
        self.lista_t_colisao = []
        self.lista_angulo_colisao = []
        self.reset_all = False


# === Funções de Utilidade ===

def derivada(t):
    h = 1e-5
    t1 = t - h
    t2 = t + h
    p1 = estado.curva_parametrica(t1)
    p2 = estado.curva_parametrica(t2)
    p1 = np.array([p1[1], p1[2]])
    p2 = np.array([p2[1], p2[2]])
    return (p2 - p1) / (2 * h)

def tangente(t):
    deriv = derivada(t)
    norm = np.linalg.norm(deriv)
    if norm < 1e-12:
        return np.array([1.0, 0.0])
    return deriv / norm

def normal(t):  # para dentro
    tng = tangente(t)
    return np.array([-tng[1], tng[0]])

def refletir_vetor(v, n):
    return v - 2 * np.dot(v, n) * n


# === Configuração do Gráfico ===
plt.style.use('seaborn-v0_8')
plt.rcParams['font.size'] = 10

fig = plt.figure(figsize=(16, 12))
fig.set_facecolor('#f0f0f5')

gs_main = gridspec.GridSpec(2, 1, height_ratios=[8, 2], hspace=0.05)
gs_graficos = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs_main[0], width_ratios=[2, 1])

ax = fig.add_subplot(gs_graficos[0])
ax.set_facecolor('#fafafa')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title("Espaço de Configuração", pad=20, fontsize=14, color='#333333')

ax2 = fig.add_subplot(gs_graficos[1])
ax2.set_facecolor('#fafafa')
ax2.grid(True, alpha=0.3)
ax2.set_title("Espaço de Fase", pad=20, fontsize=14)
ax2.set_xlabel("Parâmetro t (× π)", fontsize=10)
ax2.set_ylabel("cos θ (ângulo com a tangente)", fontsize=10)
ax2.set_xlim(0, 2)
ax2.set_ylim(-1, 1)

ax_controles = fig.add_subplot(gs_main[1])
ax_controles.set_axis_off()

# === Elementos Visuais ===
curva_plot, = ax.plot([], [], 'k-', linewidth=2, alpha=0.8)
bolinha, = ax.plot([], [], 'ro', markersize=6, zorder=3)
trajeto, = ax.plot([], [], 'r-', linewidth=1.2, alpha=0.75)
trajeto_aux, = ax.plot([], [], 'c--', linewidth=1.8, alpha=0.85)   # linha de construção simplético
normal_linha, = ax.plot([], [], 'b--', linewidth=1.5, alpha=0.6)
vel_linha, = ax.plot([], [], 'g-', linewidth=1.5, alpha=0.8)
tangente_linha, = ax.plot([], [], 'm-', linewidth=1.5, alpha=0.6)

colisao_plot, = ax2.plot([], [], 'ro', markersize=3, alpha=0.85)

texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                     bbox=dict(facecolor='white', alpha=0.95, edgecolor='#cccccc'))


# Controles
ax.add_patch(patches.Rectangle((0.05, 0.15), 0.15, 0.07, transform=fig.transFigure,
                               facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax_radio = plt.axes([0.05, 0.07, 0.13, 0.1])
radio = RadioButtons(ax_radio, ['Círculo', 'Elipse'], active=0)
ax.text(0.095, 0.18, "Fronteira", transform=fig.transFigure, ha='center', fontsize=9)

ax.add_patch(patches.Rectangle((0.25, 0.15), 0.20, 0.07, transform=fig.transFigure,
                               facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax.text(0.25, 0.18, "Parâmetros da Curva", transform=fig.transFigure, ha='center', fontsize=9)
ax_texto_a = plt.axes([0.24, 0.14, 0.06, 0.04])
texto_a = TextBox(ax_texto_a, 'a', initial='1.0')
ax_texto_b = plt.axes([0.24, 0.10, 0.06, 0.04])
texto_b = TextBox(ax_texto_b, 'b', initial='1.0')

ax.add_patch(patches.Rectangle((0.35, 0.15), 0.15, 0.07, transform=fig.transFigure,
                               facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax_radio_modo = plt.axes([0.34, 0.07, 0.13, 0.1])
radio_modo = RadioButtons(ax_radio_modo, ['Elástico', 'Simplético'], active=0)
ax.text(0.385, 0.18, "Colisão", transform=fig.transFigure, ha='center', fontsize=9)

ax.text(0.65, 0.18, "Condição Inicial", transform=fig.transFigure, ha='center', fontsize=9)
ax_pos_t = plt.axes([0.60, 0.15, 0.15, 0.02])
slider_pos_t = Slider(ax_pos_t, 't (× π)', 0, 2, valinit=0, valstep=0.005)
ax_angulo = plt.axes([0.60, 0.11, 0.15, 0.02])
slider_angulo = Slider(ax_angulo, 'Ângulo (× π)', 0, 1, valinit=0.25, valstep=0.01)
ax_vel = plt.axes([0.60, 0.07, 0.15, 0.02])
slider_vel = Slider(ax_vel, 'Velocidade', 0.5, 4.0, valinit=1.0, valstep=0.1)

ax.add_patch(patches.Rectangle((0.50, 0.05), 0.48, 0.09, transform=fig.transFigure,
                               facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax.text(0.86, 0.18, "Controles da Simulação", transform=fig.transFigure, ha='center', fontsize=9)

ax_botao_start_pause = plt.axes([0.82, 0.13, 0.08, 0.04])
botao_start_pause = Button(ax_botao_start_pause, 'Iniciar', color='#ddffdd')
ax_botao_reset = plt.axes([0.82, 0.08, 0.08, 0.04])
botao_reset = Button(ax_botao_reset, 'Reset', color='#ffdddd')
ax_botao_info = plt.axes([0.82, 0.03, 0.08, 0.04])
botao_info = Button(ax_botao_info, 'Info', color='#ddddff')


# ====================== CALLBACKS ======================

def preparar_simulacao(event):
    global estado
    normal_linha.set_data([], [])
    vel_linha.set_data([], [])
    tangente_linha.set_data([], [])
    trajeto_aux.set_data([], [])
    texto_info.set_text('Pronto para iniciar')
    atualizar_curva_e_bolinha()

def reset_simulacao(event):
    slider_pos_t.set_val(0)
    slider_angulo.set_val(0.25)
    slider_vel.set_val(1.0)
    texto_a.set_val('1.0')
    texto_b.set_val('1.0')
    botao_start_pause.label.set_text('Iniciar')
    texto_info.set_text('Pronto para iniciar')
    
    estado.reset()
    atualizar_curva_e_bolinha()
    
    if estado.reset_all:
        botao_reset.label.set_text("Reset")
        estado.reset_all = False
    else:
        estado.reset_all = True
        botao_reset.label.set_text("Reset all")


def atualizar_curva(label):
    if estado.primeiro_inicio:
        estado.curva_parametrica.curva_atual = label
        atualizar_curva_e_bolinha()

def atualizar_modo(label):
    if estado.primeiro_inicio:
        estado.modo_bilhar = label

def atualizar_curva_e_bolinha():
    estado.curva_parametrica.parametro_a = float(texto_a.text)
    estado.curva_parametrica.parametro_b = float(texto_b.text)
    
    t = np.linspace(0, 2*np.pi, 10000)
    pontos = np.array([estado.curva_parametrica(ti) for ti in t]).T
    curva_plot.set_data(pontos[1], pontos[2])
    estado.curve_points = pontos
    
    ax.set_xlim(np.min(pontos[1])-0.6, np.max(pontos[1])+0.6)
    ax.set_ylim(np.min(pontos[2])-0.6, np.max(pontos[2])+0.6)
    
    estado.pos = np.array([estado.curva_parametrica(estado.t)[1],
                           estado.curva_parametrica(estado.t)[2]])
    
    tng = tangente(estado.t)
    tangente_linha.set_data([estado.pos[0], estado.pos[0]+tng[0]],
                            [estado.pos[1], estado.pos[1]+tng[1]])
    
    estado.vel = np.array([
        tng[0]*np.cos(estado.angulo_vel) - tng[1]*np.sin(estado.angulo_vel),
        tng[1]*np.cos(estado.angulo_vel) + tng[0]*np.sin(estado.angulo_vel)
    ])
    
    vel_linha.set_data([estado.pos[0], estado.pos[0]+estado.vel[0]],
                       [estado.pos[1], estado.pos[1]+estado.vel[1]])
    
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data([], [])
    trajeto_aux.set_data([], [])
    colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)
    
    texto_info.set_text(f"Curva: {estado.curva_parametrica.curva_atual} | Modo: {estado.modo_bilhar}")
    fig.canvas.draw_idle()


def continuar_ou_pausar_simulacao(event):
    if estado.pausado:
        estado.pausado = False
        texto_info.set_text('Simulação em andamento...')
        botao_start_pause.label.set_text('Pausar')
        botao_reset.label.set_text("Reset")
        estado.reset_all = False
        iniciar_simulacao()
    else:
        estado.pausado = True
        texto_info.set_text('Simulação pausada')
        botao_start_pause.label.set_text('Continuar')


def iniciar_simulacao():
    global ani
    if estado.primeiro_inicio:
        estado.primeiro_inicio = False
     
    ani = FuncAnimation(fig, update, frames=None, init_func=init,
                        blit=False, interval=1, cache_frame_data=False)
    fig.canvas.draw()


def mostrar_info(event):
    texto_info.set_text(
        "Simulação de Bilhares\n"
        "Bilhar Elástico (reflexão clássica) × Bilhar Simplético\n"
        "Implementação corrigida e otimizada"
    )


# ====================== SLIDERS ======================

def update_posicao_t(val):
    if estado.primeiro_inicio:
        estado.t = val * np.pi
        atualizar_curva_e_bolinha()

def update_angulo(val):
    if estado.primeiro_inicio:
        estado.angulo_vel = val * np.pi
        atualizar_curva_e_bolinha()

def update_vel(val):
    if estado.primeiro_inicio:
        estado.velocidade_simulacao = val

slider_pos_t.on_changed(update_posicao_t)
slider_angulo.on_changed(update_angulo)
slider_vel.on_changed(update_vel)

radio.on_clicked(atualizar_curva)
radio_modo.on_clicked(atualizar_modo)
botao_reset.on_clicked(reset_simulacao)
botao_start_pause.on_clicked(continuar_ou_pausar_simulacao)
botao_info.on_clicked(mostrar_info)


def init():
    return (curva_plot, bolinha, trajeto, trajeto_aux,
            normal_linha, vel_linha, tangente_linha,
            colisao_plot, texto_info)


def update(frame):
    if estado.pausado:
        return (curva_plot, bolinha, trajeto, trajeto_aux,
                normal_linha, vel_linha, tangente_linha,
                colisao_plot, texto_info)

    dt = 0.012 * estado.velocidade_simulacao

    # Movimento
    estado.pos += estado.vel * dt
    estado.trajetoria.append(estado.pos.copy())

    # Detecção de colisão
    if estado.curva_parametrica.colisao(estado.pos):
        # Encontra o ponto mais próximo na malha
        x, y = estado.curve_points[1], estado.curve_points[2]
        dist2 = (x - estado.pos[0])**2 + (y - estado.pos[1])**2
        i_min = np.argmin(dist2)
        t_min = estado.curve_points[0, i_min]

        hit_pos = np.array([estado.curva_parametrica(t_min)[1],
                            estado.curva_parametrica(t_min)[2]])

        if estado.modo_bilhar == 'Elástico':
            estado.vel = refletir_vetor(estado.vel, normal(t_min))
            trajeto_aux.set_data([], [])   # limpa auxiliar

        else:  # Simplético - construção exata
            x_pos = np.array([estado.curva_parametrica(estado.t)[1],
                              estado.curva_parametrica(estado.t)[2]])
            T = tangente(t_min)
            lambdas = estado.curva_parametrica.intersect_line(x_pos, T)

            other_lambda = 0.0
            for lam in lambdas:
                if abs(lam) > 1e-6:
                    other_lambda = lam
                    break

            z_pos = x_pos + other_lambda * T

            # Direção de saída
            if np.linalg.norm(z_pos - hit_pos) < 1e-8:
                # degenerado → fallback elástico
                estado.vel = refletir_vetor(estado.vel, normal(t_min))
            else:
                estado.vel = (z_pos - hit_pos)
                estado.vel /= np.linalg.norm(estado.vel)

            # Linha de construção (visualização)
            estado.trajetoria_aux = [x_pos, z_pos]
            trajeto_aux.set_data([p[0] for p in estado.trajetoria_aux],
                                 [p[1] for p in estado.trajetoria_aux])

        # Posição exata no impacto + pequeno push para fora
        estado.pos = hit_pos.copy() + 1e-5 * estado.vel
        estado.t = t_min
        estado.cos_angulo = float(np.dot(estado.vel, tangente(estado.t)))

        # Registra no espaço de fase
        estado.lista_t_colisao.append(estado.t / np.pi)
        estado.lista_angulo_colisao.append(estado.cos_angulo)
        colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)

    # Atualiza gráficos
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data([p[0] for p in estado.trajetoria],
                     [p[1] for p in estado.trajetoria])

    return (curva_plot, bolinha, trajeto, trajeto_aux,
            normal_linha, vel_linha, tangente_linha,
            colisao_plot, texto_info)


# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    estado = EstadoBilhar()
    preparar_simulacao(None)
    plt.show()