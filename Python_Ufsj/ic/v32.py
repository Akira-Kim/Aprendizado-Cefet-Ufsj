import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox, RadioButtons
from matplotlib import gridspec

# === Funções de Utilidade ===
def refletir_vetor(v, normal):
    """Reflete o vetor v em relação à normal"""
    normal = normal / np.linalg.norm(normal)
    return v - 2 * np.dot(v, normal) * normal

# === Sistema de Funções Paramétricas ===
class FuncaoParametrica:
    def __init__(self):
        self.funcoes = {
            'Elipse': self.elipse,
            'Astroide': self.astroide,
            'Cardioide': self.cardioide,
            'Lemniscata': self.lemniscata,
            'Personalizada': self.personalizada
        }
        self.parametros = {'a': 2.0, 'b': 2.0, 'n': 1.0}
        self.funcao_atual = 'Elipse'
    
    def __call__(self, t):
        try:
            return self.funcoes[self.funcao_atual](t)
        except:
            return np.array([0.0, 0.0])
    
    def derivada(self, t, h=1e-5):
        """Calcula a derivada numericamente"""
        try:
            p1 = self(t - h)
            p2 = self(t + h)
            return (p2 - p1) / (2 * h)
        except:
            return np.array([0.0, 0.0])
    
    def normal(self, t):
        """Calcula o vetor normal unitário"""
        try:
            deriv = self.derivada(t)
            normal = np.array([-deriv[1], deriv[0]])
            norm = np.linalg.norm(normal)
            if norm == 0:
                return np.array([0.0, 1.0])
            return normal / norm
        except:
            return np.array([0.0, 1.0])
    
    def elipse(self, t):
        a, b = self.parametros['a'], self.parametros['b']
        return np.array([a * np.cos(t), b * np.sin(t)])
    
    def astroide(self, t):
        a = self.parametros['a']
        return np.array([a * np.cos(t)**3, a * np.sin(t)**3])
    
    def cardioide(self, t):
        a = self.parametros['a']
        return a * np.array([np.cos(t)*(1-np.cos(t)), np.sin(t)*(1-np.cos(t))])
    
    def lemniscata(self, t):
        a = self.parametros['a']
        den = 1 + np.sin(t)**2
        return a * np.array([np.cos(t)/den, np.sin(t)*np.cos(t)/den])
    
    def personalizada(self, t):
        try:
            a, b, n = self.parametros['a'], self.parametros['b'], self.parametros['n']
            safe_cos = np.sign(np.cos(t)) * (abs(np.cos(t)))**n
            safe_sin = np.sign(np.sin(t)) * (abs(np.sin(t)))**n
            return np.array([a * safe_cos, b * safe_sin])
        except:
            return np.array([0.0, 0.0])

# === Estado da Simulação ===
class EstadoBilhar:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.pos = np.array([1.0, 1.0])
        self.vel = np.array([0.0, 0.0])
        self.trajetoria = [self.pos.copy()]
        self.angulos_colisao = []
        self.t_colisao = []  # Armazena os parâmetros t de cada colisão
        self.num_colisoes = 0
        self.ultima_colisao = None
        self.ultimo_angulo = None
        self.pausado = True
        self.velocidade_simulacao = 1.0
        self.primeiro_inicio = True
        self.funcao_parametrica = FuncaoParametrica()

estado = EstadoBilhar()

# === Configuração do Gráfico ===
plt.style.use('seaborn-v0_8')
fig = plt.figure(figsize=(14, 9))
gs = gridspec.GridSpec(3, 2, height_ratios=[3, 1, 1], width_ratios=[3, 1])

ax = fig.add_subplot(gs[0, 0])
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title("Bilhar Paramétrico", pad=20)

ax2 = fig.add_subplot(gs[0, 1])
ax2.grid(True, alpha=0.3)
ax2.set_title("Ângulo de Colisão vs Posição na Curva", pad=20)
ax2.set_xlabel("Parâmetro t (0 a 2π)")
ax2.set_ylabel("Ângulo de Colisão (°)")
ax2.set_xlim(0, 2*np.pi)
ax2.set_ylim(0, 180)

# === Elementos Visuais ===
curva_plot, = ax.plot([], [], 'k-', linewidth=2)
bolinha, = ax.plot([], [], 'ro', markersize=8, zorder=3)
trajeto, = ax.plot([], [], 'r-', linewidth=1, alpha=0.7)
normal_linha, = ax.plot([], [], 'b--', linewidth=1, alpha=0.5)
vel_linha, = ax.plot([], [], 'g-', linewidth=1, alpha=0.7)

angulo_plot, = ax2.plot([], [], 'ro', markersize=5, alpha=0.7)

texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=9,
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
texto_funcao = ax.text(0.02, 0.80, '', transform=ax.transAxes, fontsize=9,
                      bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# === Controles Interativos ===
ax_radio = fig.add_axes([0.75, 0.85, 0.2, 0.1])
radio = RadioButtons(ax_radio, ['Elipse', 'Astroide', 'Cardioide', 'Lemniscata', 'Personalizada'], active=0)

slider_width = 0.25
ax_posx = fig.add_axes([0.10, 0.25, slider_width, 0.03])
slider_posx = Slider(ax_posx, 'Posição X', -3.9, 3.9, valinit=1.0, valstep=0.1)

ax_posy = fig.add_axes([0.10, 0.20, slider_width, 0.03])
slider_posy = Slider(ax_posy, 'Posição Y', -3.9, 3.9, valinit=1.0, valstep=0.1)

ax_angulo = fig.add_axes([0.10, 0.15, slider_width, 0.03])
slider_angulo = Slider(ax_angulo, 'Ângulo (graus)', 0, 360, valinit=30, valstep=1)

ax_vel = fig.add_axes([0.45, 0.25, slider_width, 0.03])
slider_vel = Slider(ax_vel, 'Velocidade', 0.1, 3.0, valinit=1.0, valstep=0.1)

param_width = 0.15
texto_a = TextBox(fig.add_axes([0.45, 0.20, param_width, 0.03]), 'a', initial='2.0')
texto_b = TextBox(fig.add_axes([0.45+param_width+0.05, 0.20, param_width, 0.03]), 'b', initial='2.0')
texto_n = TextBox(fig.add_axes([0.45+2*(param_width+0.05), 0.20, param_width, 0.03]), 'n', initial='1.0')

btn_width = 0.15
botao_reset = Button(fig.add_axes([0.15, 0.05, btn_width, 0.05]), 'Reset', color='lightgoldenrodyellow')
botao_pause = Button(fig.add_axes([0.35, 0.05, btn_width, 0.05]), 'Pausar', color='lightcoral')
botao_start = Button(fig.add_axes([0.55, 0.05, btn_width, 0.05]), 'Iniciar', color='palegreen')

# === Funções de Atualização ===
def atualizar_funcao(label):
    estado.funcao_parametrica.funcao_atual = label
    atualizar_curva()

radio.on_clicked(atualizar_funcao)

def atualizar_curva():
    try:
        estado.funcao_parametrica.parametros['a'] = float(texto_a.text)
        estado.funcao_parametrica.parametros['b'] = float(texto_b.text)
        estado.funcao_parametrica.parametros['n'] = float(texto_n.text)
    except ValueError:
        pass
    
    t = np.linspace(0, 2*np.pi, 500)
    pontos = np.array([estado.funcao_parametrica(ti) for ti in t]).T
    curva_plot.set_data(pontos[0], pontos[1])
    
    ax.set_xlim(np.min(pontos[0])-0.5, np.max(pontos[0])+0.5)
    ax.set_ylim(np.min(pontos[1])-0.5, np.max(pontos[1])+0.5)
    
    texto_funcao.set_text(f"Função: {estado.funcao_parametrica.funcao_atual}")
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    fig.canvas.draw_idle()

def atualizar_parametros(val):
    atualizar_curva()

texto_a.on_submit(atualizar_parametros)
texto_b.on_submit(atualizar_parametros)
texto_n.on_submit(atualizar_parametros)

def reset_simulacao(event):
    estado.reset()
    estado.pos = np.array([slider_posx.val, slider_posy.val])
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data([], [])
    angulo_plot.set_data([], [])
    estado.angulos_colisao = []
    estado.t_colisao = []
    texto_info.set_text('Pronto para iniciar')
    atualizar_curva()

def pausar_simulacao(event):
    estado.pausado = True
    texto_info.set_text('Simulação pausada')

def iniciar_simulacao(event):
    if estado.primeiro_inicio:
        angulo_rad = np.radians(slider_angulo.val)
        velocidade = min(slider_vel.val, 3.0)
        estado.vel = np.array([np.cos(angulo_rad), np.sin(angulo_rad)]) * velocidade
        estado.primeiro_inicio = False
    
    estado.pausado = False
    texto_info.set_text('Simulação em andamento')

botao_reset.on_clicked(reset_simulacao)
botao_pause.on_clicked(pausar_simulacao)
botao_start.on_clicked(iniciar_simulacao)

def update_posicao(val):
    estado.pos = np.array([slider_posx.val, slider_posy.val])
    if estado.pausado or estado.primeiro_inicio:
        estado.trajetoria = [estado.pos.copy()]
        bolinha.set_data([estado.pos[0]], [estado.pos[1]])
        fig.canvas.draw_idle()

def update_angulo(val):
    if estado.pausado or estado.primeiro_inicio:
        angulo_rad = np.radians(slider_angulo.val)
        velocidade = min(slider_vel.val, 3.0)
        estado.vel = np.array([np.cos(angulo_rad), np.sin(angulo_rad)]) * velocidade

slider_posx.on_changed(update_posicao)
slider_posy.on_changed(update_posicao)
slider_angulo.on_changed(update_angulo)
slider_vel.on_changed(lambda val: setattr(estado, 'velocidade_simulacao', val))

def encontrar_colisao(ponto, direcao):
    """Versão robusta de detecção de colisão"""
    if np.linalg.norm(direcao) < 1e-8:
        return None, None
    
    try:
        # Amostragem adaptativa
        num_samples = min(5000, max(1000, int(2000 * (1 + np.linalg.norm(direcao)))))
        t_samples = np.linspace(0, 2*np.pi, num_samples)
        curve_points = np.array([estado.funcao_parametrica(t) for t in t_samples])
        
        # Vetor direção normalizado
        dir_norm = direcao / np.linalg.norm(direcao)
        
        # Calcular distâncias e projeções
        delta = curve_points - ponto
        proj = np.dot(delta, dir_norm)
        dist = np.linalg.norm(delta - proj[:, None] * dir_norm, axis=1)
        
        # Filtrar pontos à frente e dentro da tolerância
        tol = max(0.01, min(0.05, 0.02 * np.linalg.norm(direcao)))
        mask = (proj > 0) & (dist < tol)
        
        if not np.any(mask):
            return None, None
        
        # Encontrar a colisão mais próxima
        idx = np.argmin(proj[mask])
        return curve_points[mask][idx], t_samples[mask][idx]
    except Exception as e:
        print(f"Erro na detecção de colisão: {e}")
        return None, None

def init():
    curva_plot.set_data([], [])
    bolinha.set_data([], [])
    trajeto.set_data([], [])
    normal_linha.set_data([], [])
    vel_linha.set_data([], [])
    angulo_plot.set_data([], [])
    texto_info.set_text('Pronto para iniciar')
    texto_funcao.set_text('')
    return curva_plot, bolinha, trajeto, normal_linha, vel_linha, angulo_plot, texto_info, texto_funcao

def update(frame):
    if estado.pausado:
        return curva_plot, bolinha, trajeto, normal_linha, vel_linha, angulo_plot, texto_info, texto_funcao
    
    dt = 0.015 * estado.velocidade_simulacao
    nova_pos = estado.pos + estado.vel * dt
    
    ponto_colisao, t_colisao = encontrar_colisao(estado.pos, estado.vel * dt)
    
    if ponto_colisao is not None and t_colisao is not None:
        try:
            normal = estado.funcao_parametrica.normal(t_colisao)
            estado.pos = ponto_colisao + normal * 0.01
            estado.vel = refletir_vetor(estado.vel, normal) * 0.99
            estado.ultima_colisao = ponto_colisao
            
            angulo = np.degrees(np.arccos(np.clip(np.dot(-estado.vel/np.linalg.norm(estado.vel), normal), -1, 1)))
            estado.angulos_colisao.append(angulo)
            estado.t_colisao.append(t_colisao)
            estado.num_colisoes += 1
            
            if estado.t_colisao and estado.angulos_colisao:
                angulo_plot.set_data(estado.t_colisao, estado.angulos_colisao)
            
            texto_info.set_text(f"Colisão: {estado.num_colisoes}\nÂngulo: {angulo:.1f}°\nt: {t_colisao:.2f} rad")
        except Exception as e:
            print(f"Erro durante colisão: {e}")
            estado.pos = nova_pos
    else:
        estado.pos = nova_pos
    
    estado.trajetoria.append(estado.pos.copy())
    
    # Atualiza gráficos
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data([p[0] for p in estado.trajetoria], [p[1] for p in estado.trajetoria])
    
    if estado.ultima_colisao is not None and t_colisao is not None:
        try:
            normal = estado.funcao_parametrica.normal(t_colisao)
            normal_linha.set_data(
                [estado.ultima_colisao[0], estado.ultima_colisao[0]+normal[0]],
                [estado.ultima_colisao[1], estado.ultima_colisao[1]+normal[1]]
            )
            vel_linha.set_data(
                [estado.ultima_colisao[0], estado.ultima_colisao[0]+estado.vel[0]],
                [estado.ultima_colisao[1], estado.ultima_colisao[1]+estado.vel[1]]
            )
        except:
            pass
    
    return curva_plot, bolinha, trajeto, normal_linha, vel_linha, angulo_plot, texto_info, texto_funcao

# Inicialização
reset_simulacao(None)
atualizar_curva()

ani = FuncAnimation(fig, update, frames=1000, init_func=init, blit=False, interval=20)

plt.show()