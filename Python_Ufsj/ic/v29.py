import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox
from matplotlib import gridspec

# === Funções de Utilidade ===
def refletir_vetor(v, normal):
    """Reflete o vetor v em relação à normal (lei da reflexão simplética)"""
    normal = normal / np.linalg.norm(normal)
    return v - 2 * np.dot(v, normal) * normal

# === Configuração da Curva Paramétrica ===
def curva_paramétrica(t, a=2.0, b=2.0, n=1.0):
    """Função paramétrica que define a borda do bilhar"""
    return np.array([a * np.cos(t)**n, b * np.sin(t)**n])

def normal_paramétrica(t, a=2.0, b=2.0, n=1.0):
    """Calcula o vetor normal à curva paramétrica"""
    dx = -a * n * np.cos(t)**(n-1) * np.sin(t)
    dy = b * n * np.sin(t)**(n-1) * np.cos(t)
    normal = np.array([-dy, dx])
    return normal / np.linalg.norm(normal)

# === Estado da Simulação ===
class EstadoBilhar:
    def __init__(self):
        self.pos = np.array([1.0, 1.0])
        self.vel = np.array([0.0, 0.0])  # Inicia com velocidade zero
        self.trajetoria = [self.pos.copy()]
        self.angulos_colisao = []
        self.num_colisoes = 0
        self.ultima_colisao = None
        self.ultimo_angulo = None
        self.pausado = True  # Começa pausado
        self.parametros_curva = {'a': 2.0, 'b': 2.0, 'n': 1.0}
        self.velocidade_simulacao = 0.5  # Valor médio inicial
        self.primeiro_inicio = True

estado = EstadoBilhar()

# === Configuração do Gráfico Responsivo ===
plt.style.use('seaborn')  # Estilo mais moderno
fig = plt.figure(figsize=(12, 8), tight_layout=True)
gs = gridspec.GridSpec(3, 2, height_ratios=[3, 1, 1], width_ratios=[3, 1])

# Área principal de visualização
ax = fig.add_subplot(gs[0, 0])
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title("Bilhar Paramétrico", pad=20)

# Gráfico de ângulos
ax2 = fig.add_subplot(gs[0, 1])
ax2.grid(True, alpha=0.3)
ax2.set_title("Ângulos de Colisão", pad=20)

# Área de controles (organizada em 3 linhas)
ax_controles1 = fig.add_subplot(gs[1, :])
ax_controles1.axis('off')  # Usaremos para organizar os sliders

ax_controles2 = fig.add_subplot(gs[2, :])
ax_controles2.axis('off')  # Usaremos para organizar os botões

# === Elementos Visuais ===
theta_plot = np.linspace(0, 2*np.pi, 300)
curva_plot, = ax.plot([], [], 'k-', linewidth=2)
bolinha, = ax.plot([], [], 'ro', markersize=8, zorder=3)
trajeto, = ax.plot([], [], 'r-', linewidth=1, alpha=0.7)
normal_linha, = ax.plot([], [], 'b--', linewidth=1, alpha=0.5)
vel_linha, = ax.plot([], [], 'g-', linewidth=1, alpha=0.7)

# Textos informativos com estilo melhorado
texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=9,
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
texto_funcao = ax.text(0.02, 0.80, '', transform=ax.transAxes, fontsize=9,
                      bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# Gráfico de ângulos
angulo_plot, = ax2.plot([], [], 'ko', markersize=4)
ax2.set_xlabel("Número da Colisão", labelpad=5)
ax2.set_ylabel("Ângulo de Colisão (°)", labelpad=5)

# === Controles Interativos (Layout Organizado) ===

# Sliders organizados na primeira linha de controles
slider_width = 0.25
slider_pad = 0.03

# Posição X
ax_posx = fig.add_axes([0.10, 0.25, slider_width, 0.03])
slider_posx = Slider(ax_posx, 'Posição X', -2.9, 2.9, valinit=1.0, valstep=0.1)

# Posição Y
ax_posy = fig.add_axes([0.10, 0.20, slider_width, 0.03])
slider_posy = Slider(ax_posy, 'Posição Y', -2.9, 2.9, valinit=1.0, valstep=0.1)

# Ângulo
ax_angulo = fig.add_axes([0.10, 0.15, slider_width, 0.03])
slider_angulo = Slider(ax_angulo, 'Ângulo (graus)', 0, 360, valinit=30, valstep=1)

# Velocidade (agora vai de 0.1 a 1.0)
ax_vel = fig.add_axes([0.45, 0.25, slider_width, 0.03])
slider_vel = Slider(ax_vel, 'Velocidade', 0.1, 1.0, valinit=0.5, valstep=0.05)

# Parâmetros da curva (organizados na horizontal)
param_width = 0.15
texto_a = TextBox(fig.add_axes([0.45, 0.20, param_width, 0.03]), 'a', initial='2.0')
texto_b = TextBox(fig.add_axes([0.45+param_width+0.05, 0.20, param_width, 0.03]), 'b', initial='2.0')
texto_n = TextBox(fig.add_axes([0.45+2*(param_width+0.05), 0.20, param_width, 0.03]), 'n', initial='1.0')

# Botões (organizados na segunda linha)
btn_width = 0.15
botao_reset = Button(fig.add_axes([0.15, 0.05, btn_width, 0.05]), 'Reset', color='lightgoldenrodyellow')
botao_pause = Button(fig.add_axes([0.35, 0.05, btn_width, 0.05]), 'Pausar', color='lightcoral')
botao_start = Button(fig.add_axes([0.55, 0.05, btn_width, 0.05]), 'Iniciar', color='palegreen')

# === Funções de Atualização ===
def atualizar_curva():
    """Atualiza a curva paramétrica com os novos parâmetros"""
    t = np.linspace(0, 2*np.pi, 300)
    x, y = curva_paramétrica(t, **estado.parametros_curva)
    curva_plot.set_data(x, y)
    
    # Ajusta os limites do gráfico
    ax.set_xlim(min(x)-0.5, max(x)+0.5)
    ax.set_ylim(min(y)-0.5, max(y)+0.5)
    
    # Atualiza a exibição da função
    a, b, n = estado.parametros_curva['a'], estado.parametros_curva['b'], estado.parametros_curva['n']
    texto_funcao.set_text(f"Função atual:\nx = {a:.1f}·cos(t)^{n:.1f}\ny = {b:.1f}·sin(t)^{n:.1f}")
    
    # Atualiza a posição da bolinha
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    fig.canvas.draw_idle()

def atualizar_parametros(val):
    """Atualiza os parâmetros da curva"""
    try:
        estado.parametros_curva['a'] = float(texto_a.text)
        estado.parametros_curva['b'] = float(texto_b.text)
        estado.parametros_curva['n'] = float(texto_n.text)
        estado.velocidade_simulacao = slider_vel.val  # Atualiza a velocidade
        atualizar_curva()
    except ValueError:
        pass

texto_a.on_submit(atualizar_parametros)
texto_b.on_submit(atualizar_parametros)
texto_n.on_submit(atualizar_parametros)

def reset_simulacao(event):
    estado.pos = np.array([slider_posx.val, slider_posy.val])
    estado.vel = np.array([0.0, 0.0])  # Reseta a velocidade
    estado.trajetoria = [estado.pos.copy()]
    estado.angulos_colisao = []
    estado.num_colisoes = 0
    estado.ultima_colisao = None
    estado.ultimo_angulo = None
    estado.pausado = True
    estado.primeiro_inicio = True
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 180)
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data([], [])
    texto_info.set_text('Pronto para iniciar')
    atualizar_curva()

def pausar_simulacao(event):
    estado.pausado = True
    texto_info.set_text('Simulação pausada')

def iniciar_simulacao(event):
    if estado.primeiro_inicio:
        # Só define a velocidade na primeira vez que inicia
        angulo_rad = np.radians(slider_angulo.val)
        velocidade = 0.5
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
        velocidade = 0.5
        estado.vel = np.array([np.cos(angulo_rad), np.sin(angulo_rad)]) * velocidade

slider_posx.on_changed(update_posicao)
slider_posy.on_changed(update_posicao)
slider_angulo.on_changed(update_angulo)
slider_vel.on_changed(lambda val: setattr(estado, 'velocidade_simulacao', val))

def encontrar_colisao(ponto, direcao):
    """Encontra a próxima colisão com a curva paramétrica"""
    if np.linalg.norm(direcao) == 0:
        return None, None
    
    dt = 0.01
    t = 0
    max_iter = 1000
    parametros = estado.parametros_curva
    
    for _ in range(max_iter):
        t += dt
        nova_pos = ponto + t * direcao
        angulo = np.arctan2(nova_pos[1], nova_pos[0])
        pos_curva = curva_paramétrica(angulo, **parametros)
        distancia = np.linalg.norm(nova_pos - pos_curva)
        
        if distancia < 0.05:  # Tolerância para colisão
            return nova_pos, angulo
    
    return None, None

def init():
    curva_plot.set_data([], [])
    bolinha.set_data([], [])
    trajeto.set_data([], [])
    normal_linha.set_data([], [])
    vel_linha.set_data([], [])
    texto_info.set_text('Pronto para iniciar')
    texto_funcao.set_text('')
    angulo_plot.set_data([], [])
    return curva_plot, bolinha, trajeto, normal_linha, vel_linha, texto_info, angulo_plot, texto_funcao

def update(frame):
    if estado.pausado:
        return curva_plot, bolinha, trajeto, normal_linha, vel_linha, texto_info, angulo_plot, texto_funcao
    
    dt = 0.02 * estado.velocidade_simulacao
    nova_pos = estado.pos + estado.vel * dt
    
    # Verifica colisão com a curva paramétrica
    ponto_colisao, t_colisao = encontrar_colisao(estado.pos, estado.vel)
    
    if ponto_colisao is not None:
        # Calcula normal e tangente no ponto de colisão
        normal = normal_paramétrica(t_colisao, **estado.parametros_curva)
        
        # Atualiza estado (reflexão simplética)
        estado.pos = ponto_colisao
        estado.vel = refletir_vetor(estado.vel, normal)
        estado.ultima_colisao = ponto_colisao
        
        # Calcula ângulo de colisão
        angulo = np.degrees(np.arccos(np.dot(-estado.vel/np.linalg.norm(estado.vel), normal)))
        estado.ultimo_angulo = angulo
        estado.angulos_colisao.append(angulo)
        estado.num_colisoes += 1
        
        texto_info.set_text(f"Colisão: {estado.num_colisoes}\nÂngulo: {angulo:.1f}°")
        ajustar_zoom()
    else:
        estado.pos = nova_pos
    
    estado.trajetoria.append(estado.pos.copy())
    
    # Atualiza gráficos
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data([p[0] for p in estado.trajetoria], [p[1] for p in estado.trajetoria])
    
    # Mostra normal e velocidade na última colisão
    if estado.ultima_colisao is not None:
        t = np.arctan2(estado.ultima_colisao[1], estado.ultima_colisao[0])
        normal = normal_paramétrica(t, **estado.parametros_curva)
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
    
    return curva_plot, bolinha, trajeto, normal_linha, vel_linha, texto_info, angulo_plot, texto_funcao

def ajustar_zoom():
    """Ajusta o zoom do gráfico de ângulos dinamicamente"""
    if not estado.angulos_colisao:
        return
    
    num_pontos = len(estado.angulos_colisao)
    if num_pontos > 40:
        ax2.set_xlim(num_pontos - 40, num_pontos + 2)
    else:
        ax2.set_xlim(0, 42)
    
    min_ang = min(estado.angulos_colisao[-40:]) if num_pontos > 0 else 0
    max_ang = max(estado.angulos_colisao[-40:]) if num_pontos > 0 else 180
    
    margem = 10
    if max_ang - min_ang < 40:
        centro_y = (min_ang + max_ang) / 2
        ax2.set_ylim(max(0, centro_y - 25), min(180, centro_y + 25))
    else:
        ax2.set_ylim(max(0, min_ang - margem), min(180, max_ang + margem))

# Inicialização
reset_simulacao(None)
atualizar_curva()

ani = FuncAnimation(fig, update, frames=1000, init_func=init, blit=True, interval=20)

plt.show()