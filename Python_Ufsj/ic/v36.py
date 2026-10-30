import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox, RadioButtons
from matplotlib import gridspec
from scipy.optimize import minimize_scalar

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
        """Calcula a derivada numericamente com tratamento de contorno"""
        t1 = t - h if t > h else t + 2*np.pi - h
        t2 = t + h if t < 2*np.pi - h else t - 2*np.pi + h
        p1 = self(t1)
        p2 = self(t2)
        return (p2 - p1) / (2*h)
    
    def normal(self, t):
        """Calcula o vetor normal unitário com fallback"""
        deriv = self.derivada(t)
        norm_deriv = np.linalg.norm(deriv)
        
        if norm_deriv < 1e-8:
            # Tentar pontos vizinhos
            for dt in [1e-3, -1e-3, 1e-2]:
                t_alt = (t + dt) % (2*np.pi)
                deriv_alt = self.derivada(t_alt)
                norm_alt = np.linalg.norm(deriv_alt)
                if norm_alt > 1e-8:
                    normal_vec = np.array([-deriv_alt[1], deriv_alt[0]])
                    return normal_vec / norm_alt
            return np.array([0.0, 1.0])  # Fallback
        
        normal_vec = np.array([-deriv[1], deriv[0]])
        return normal_vec / norm_deriv
    
    def tangente(self, t):
        """Calcula o vetor tangente unitário"""
        try:
            deriv = self.derivada(t)
            norm = np.linalg.norm(deriv)
            if norm == 0:
                return np.array([0.0, 1.0])
            return deriv / norm
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
        self.modo_bilhar = 'Convencional'  # 'Convencional' ou 'Simpletico'
        self.ultimo_ponto = None  # Para bilhar simplético
        self.proximo_ponto = None  # Para visualização
        self.tangente_atual = None  # Para visualização
        self.curve_points = None  # Pontos pré-computados da curva
        self.curve_t = None       # Parâmetros t correspondentes
        self.modo_inicio = 'Livre'  # 'Livre' ou 'Borda'

estado = EstadoBilhar()

# === Funções de Detecção de Colisão Aprimoradas ===
def encontrar_colisao_robusta(ponto, direcao):
    """Detecção híbrida de colisão: amostragem + refinamento"""
    if np.linalg.norm(direcao) < 1e-8:
        return None, None
    
    # 1. Amostragem inicial
    t_samples = np.linspace(0, 2*np.pi, 100)
    pontos_curva = np.array([estado.funcao_parametrica(t) for t in t_samples])
    
    # Vetor direção normalizado
    dir_norm = direcao / np.linalg.norm(direcao)
    
    # Calcular distâncias e produtos escalares
    vetores = pontos_curva - ponto
    distancias = np.linalg.norm(vetores, axis=1)
    proj_direcao = np.dot(vetores, dir_norm)
    
    # Critério: ponto na frente e próximo da reta
    dist_perp = np.abs(np.cross(vetores, dir_norm))
    candidatos = np.where((proj_direcao > 0) & (dist_perp < 0.2))[0]
    
    if len(candidatos) == 0:
        return None, None
    
    # 2. Refinamento com busca binária
    melhor_idx = candidatos[np.argmin(dist_perp[candidatos])]
    t_min = t_samples[melhor_idx-1] if melhor_idx > 0 else t_samples[-1]
    t_max = t_samples[melhor_idx+1] if melhor_idx < len(t_samples)-1 else t_samples[0]
    
    # Garantir intervalo válido
    if t_min > t_max:
        t_min, t_max = t_max, t_min
    
    for _ in range(8):  # 8 iterações de refinamento
        t_meio = (t_min + t_max)/2
        p_meio = estado.funcao_parametrica(t_meio)
        vec_meio = p_meio - ponto
        dist_meio = np.abs(np.cross(vec_meio, dir_norm))
        
        # Avaliar pontos adjacentes
        t_antes = (t_min + t_meio)/2
        p_antes = estado.funcao_parametrica(t_antes)
        vec_antes = p_antes - ponto
        dist_antes = np.abs(np.cross(vec_antes, dir_norm))
        
        t_depois = (t_meio + t_max)/2
        p_depois = estado.funcao_parametrica(t_depois)
        vec_depois = p_depois - ponto
        dist_depois = np.abs(np.cross(vec_depois, dir_norm))
        
        # Atualizar intervalo
        if dist_antes < dist_meio and dist_antes < dist_depois:
            t_max = t_meio
        elif dist_depois < dist_meio:
            t_min = t_meio
        else:
            t_min = t_antes
            t_max = t_depois
    
    t_final = (t_min + t_max)/2
    ponto_final = estado.funcao_parametrica(t_final)
    
    # Verificar se está na direção do movimento
    if np.dot(ponto_final - ponto, dir_norm) > 0:
        return ponto_final, t_final
    
    return None, None

# === Bilhar Simplético Aprimorado ===
def encontrar_proximo_ponto_otimizado(x, y, t_y):
    """Encontra o próximo ponto usando otimização matemática"""
    tang_y = estado.funcao_parametrica.tangente(t_y)
    
    # Função objetivo: distância perpendicular
    def objetivo(t):
        z = estado.funcao_parametrica(t)
        vetor_xz = z - x
        # Produto vetual em 2D: |a_x*b_y - a_y*b_x|
        return abs(vetor_xz[0]*tang_y[1] - vetor_xz[1]*tang_y[0])
    
    # Evitar o ponto atual (t_y)
    if t_y > 0.1 and t_y < 2*np.pi - 0.1:
        bounds = [(0, t_y-0.1), (t_y+0.1, 2*np.pi)]
    else:
        # Caso especial perto dos limites
        if t_y < 0.1:
            bounds = [(t_y+0.1, 2*np.pi)]
        else:  # t_y > 2*np.pi - 0.1
            bounds = [(0, t_y-0.1)]
    
    melhor_t = None
    melhor_valor = float('inf')
    
    # Testar múltiplos pontos iniciais
    for bound in bounds:
        try:
            res = minimize_scalar(objetivo, bounds=bound, method='bounded')
            if res.fun < melhor_valor and abs(res.x - t_y) > 0.1:
                melhor_valor = res.fun
                melhor_t = res.x
        except:
            continue
    
    if melhor_t is None:
        # Fallback: amostragem simples
        t_candidates = np.linspace(0, 2*np.pi, 36)
        t_candidates = t_candidates[np.abs(t_candidates - t_y) > 0.2]
        if len(t_candidates) > 0:
            dists = [objetivo(t) for t in t_candidates]
            idx_min = np.argmin(dists)
            melhor_t = t_candidates[idx_min]
        else:
            return None, None
    
    return estado.funcao_parametrica(melhor_t), melhor_t

# === Configuração do Gráfico ===
plt.style.use('seaborn-v0_8')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlepad'] = 12

fig = plt.figure(figsize=(14, 9))
fig.set_facecolor('#f0f0f5')
gs = gridspec.GridSpec(3, 2, height_ratios=[3, 1, 1], width_ratios=[3, 1])

ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor('#fafafa')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title("Bilhar Paramétrico", pad=20, fontsize=14, color='#333333')

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor('#fafafa')
ax2.grid(True, alpha=0.3)
ax2.set_title("Ângulo de Colisão vs Posição na Curva", pad=20, fontsize=12)
ax2.set_xlabel("Parâmetro t (0 a 2π)", fontsize=10)
ax2.set_ylabel("Ângulo de Colisão (°)", fontsize=10)
ax2.set_xlim(0, 2*np.pi)
ax2.set_ylim(0, 180)

# === Elementos Visuais ===
curva_plot, = ax.plot([], [], 'k-', linewidth=2, alpha=0.8)
bolinha, = ax.plot([], [], 'ro', markersize=8, zorder=3)
trajeto, = ax.plot([], [], 'r-', linewidth=1, alpha=0.7)
normal_linha, = ax.plot([], [], 'b--', linewidth=1.5, alpha=0.7)
vel_linha, = ax.plot([], [], 'g-', linewidth=1.5, alpha=0.7)
tangente_linha, = ax.plot([], [], 'm-', linewidth=1.5, alpha=0.7)  # Para bilhar simplético
proxima_linha, = ax.plot([], [], 'c-', linewidth=1.5, alpha=0.7)    # Para bilhar simplético

angulo_plot, = ax2.plot([], [], 'ro', markersize=5, alpha=0.7)

texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=9,
                    bbox=dict(facecolor='white', alpha=0.9, edgecolor='#cccccc'))
texto_funcao = ax.text(0.02, 0.80, '', transform=ax.transAxes, fontsize=9,
                      bbox=dict(facecolor='white', alpha=0.9, edgecolor='#cccccc'))

# === Controles Interativos ===
# Área para controles na parte inferior
ax_controles = fig.add_axes([0.05, 0.05, 0.9, 0.15])
ax_controles.set_axis_off()

# Labels explicativos
fig.text(0.05, 0.23, "Tipo de Curva", fontsize=9)
fig.text(0.18, 0.23, "Modo de Bilhar", fontsize=9)
fig.text(0.31, 0.23, "Posição Inicial", fontsize=9)

# Funções de curva
ax_radio = plt.axes([0.05, 0.15, 0.12, 0.07])
radio = RadioButtons(ax_radio, ['Elipse', 'Astroide', 'Cardioide', 'Lemniscata', 'Personalizada'], active=0)

# Modo de bilhar
ax_radio_modo = plt.axes([0.18, 0.15, 0.12, 0.07])
radio_modo = RadioButtons(ax_radio_modo, ['Convencional', 'Simpletico'], active=0)

# Modo de posição inicial
ax_radio_posicao = plt.axes([0.31, 0.15, 0.12, 0.07])
radio_posicao = RadioButtons(ax_radio_posicao, ['Livre', 'Borda'], active=0)

# Sliders
slider_width = 0.2
ax_posx = plt.axes([0.05, 0.05, slider_width, 0.03])
slider_posx = Slider(ax_posx, 'Posição X', -3.9, 3.9, valinit=1.0, valstep=0.1)

ax_posy = plt.axes([0.05, 0.01, slider_width, 0.03])
slider_posy = Slider(ax_posy, 'Posição Y', -3.9, 3.9, valinit=1.0, valstep=0.1)

# Novo slider para posição na borda
ax_pos_t = plt.axes([0.05, 0.03, slider_width, 0.03])
ax_pos_t.set_visible(False)  # Inicialmente oculto
slider_pos_t = Slider(ax_pos_t, 't (0 a 2π)', 0, 2*np.pi, valinit=0, valstep=0.01)

ax_angulo = plt.axes([0.30, 0.05, slider_width, 0.03])
slider_angulo = Slider(ax_angulo, 'Ângulo (graus)', 0, 360, valinit=30, valstep=1)

ax_vel = plt.axes([0.30, 0.01, slider_width, 0.03])
slider_vel = Slider(ax_vel, 'Velocidade', 0.1, 3.0, valinit=1.0, valstep=0.1)

# Parâmetros da curva
param_width = 0.08
texto_a = TextBox(plt.axes([0.55, 0.05, param_width, 0.03]), 'a', initial='2.0')
texto_b = TextBox(plt.axes([0.55+param_width+0.01, 0.05, param_width, 0.03]), 'b', initial='2.0')
texto_n = TextBox(plt.axes([0.55+2*(param_width+0.01), 0.05, param_width, 0.03]), 'n', initial='1.0')

# Botões
btn_width = 0.1
botao_reset = Button(plt.axes([0.80, 0.05, btn_width, 0.04]), 'Reset', color='#ffdddd')
botao_pause = Button(plt.axes([0.80, 0.01, btn_width, 0.04]), 'Pausar', color='#ddddff')
botao_start = Button(plt.axes([0.90, 0.05, btn_width, 0.04]), 'Iniciar', color='#ddffdd')
botao_info = Button(plt.axes([0.90, 0.01, btn_width, 0.04]), 'Info', color='#ffffdd')

# === Funções de Atualização ===
def atualizar_visibilidade_posicao():
    """Atualiza a visibilidade dos controles de posição"""
    if estado.modo_inicio == 'Livre':
        ax_posx.set_visible(True)
        ax_posy.set_visible(True)
        ax_pos_t.set_visible(False)
    else:  # Modo 'Borda'
        ax_posx.set_visible(False)
        ax_posy.set_visible(False)
        ax_pos_t.set_visible(True)

def atualizar_funcao(label):
    estado.funcao_parametrica.funcao_atual = label
    atualizar_curva()

def atualizar_modo(label):
    estado.modo_bilhar = label
    estado.ultimo_ponto = None
    estado.proximo_ponto = None
    atualizar_curva()

def atualizar_modo_posicao(label):
    estado.modo_inicio = label
    atualizar_visibilidade_posicao()
    
    # Atualizar posição se estivermos no modo borda
    if estado.modo_inicio == 'Borda':
        t_val = slider_pos_t.val
        estado.pos = estado.funcao_parametrica(t_val)
        slider_posx.set_val(estado.pos[0])
        slider_posy.set_val(estado.pos[1])
        if estado.pausado or estado.primeiro_inicio:
            estado.trajetoria = [estado.pos.copy()]
            bolinha.set_data([estado.pos[0]], [estado.pos[1]])
            fig.canvas.draw_idle()

radio.on_clicked(atualizar_funcao)
radio_modo.on_clicked(atualizar_modo)
radio_posicao.on_clicked(atualizar_modo_posicao)

def atualizar_curva():
    try:
        estado.funcao_parametrica.parametros['a'] = float(texto_a.text)
        estado.funcao_parametrica.parametros['b'] = float(texto_b.text)
        estado.funcao_parametrica.parametros['n'] = float(texto_n.text)
    except ValueError:
        pass
    
    t = np.linspace(0, 2*np.pi, 1000)
    pontos = np.array([estado.funcao_parametrica(ti) for ti in t]).T
    curva_plot.set_data(pontos[0], pontos[1])
    
    # Pré-computar pontos da curva
    estado.curve_points = pontos
    estado.curve_t = t
    
    ax.set_xlim(np.min(pontos[0])-0.5, np.max(pontos[0])+0.5)
    ax.set_ylim(np.min(pontos[1])-0.5, np.max(pontos[1])+0.5)
    
    texto_funcao.set_text(f"Função: {estado.funcao_parametrica.funcao_atual}\nModo: {estado.modo_bilhar}")
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    
    # Se estiver no modo borda, atualizar a posição
    if estado.modo_inicio == 'Borda':
        t_val = slider_pos_t.val
        estado.pos = estado.funcao_parametrica(t_val)
        slider_posx.set_val(estado.pos[0])
        slider_posy.set_val(estado.pos[1])
        bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    
    fig.canvas.draw_idle()

def atualizar_parametros(val):
    atualizar_curva()

texto_a.on_submit(atualizar_parametros)
texto_b.on_submit(atualizar_parametros)
texto_n.on_submit(atualizar_parametros)

def reset_simulacao(event):
    estado.reset()
    
    if estado.modo_inicio == 'Livre':
        estado.pos = np.array([slider_posx.val, slider_posy.val])
    else:  # Modo 'Borda'
        t_val = slider_pos_t.val
        estado.pos = estado.funcao_parametrica(t_val)
        slider_posx.set_val(estado.pos[0])
        slider_posy.set_val(estado.pos[1])
    
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data([], [])
    angulo_plot.set_data([], [])
    tangente_linha.set_data([], [])
    proxima_linha.set_data([], [])
    estado.angulos_colisao = []
    estado.t_colisao = []
    texto_info.set_text('Simulação reiniciada\nPronto para iniciar')
    
    # Reset dos controles
    slider_posx.set_val(1.0)
    slider_posy.set_val(1.0)
    slider_pos_t.set_val(0)
    slider_angulo.set_val(30)
    slider_vel.set_val(1.0)
    texto_a.set_val('2.0')
    texto_b.set_val('2.0')
    texto_n.set_val('1.0')
    radio.set_active(0)
    radio_modo.set_active(0)
    radio_posicao.set_active(0)
    
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

def mostrar_info(event):
    texto_info.set_text(
        "Modo Simplético:\n"
        "Reflexão baseada na área do triângulo\n"
        "x -> y -> z onde xz ∥ tangente(y)\n\n"
        "Modo Convencional:\n"
        "Reflexão padrão: ângulo incidência = reflexão\n\n"
        "Modo Borda:\n"
        "A bolinha começa na borda da curva\n"
        "Use o slider 't' para posicioná-la"
    )

botao_reset.on_clicked(reset_simulacao)
botao_pause.on_clicked(pausar_simulacao)
botao_start.on_clicked(iniciar_simulacao)
botao_info.on_clicked(mostrar_info)

def update_posicao(val):
    if estado.modo_inicio == 'Livre':
        estado.pos = np.array([slider_posx.val, slider_posy.val])
        if estado.pausado or estado.primeiro_inicio:
            estado.trajetoria = [estado.pos.copy()]
            bolinha.set_data([estado.pos[0]], [estado.pos[1]])
            fig.canvas.draw_idle()

def update_posicao_t(val):
    """Atualiza a posição quando o slider de t é alterado (modo borda)"""
    if estado.modo_inicio == 'Borda':
        t_val = slider_pos_t.val
        estado.pos = estado.funcao_parametrica(t_val)
        slider_posx.set_val(estado.pos[0])
        slider_posy.set_val(estado.pos[1])
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
slider_pos_t.on_changed(update_posicao_t)
slider_angulo.on_changed(update_angulo)
slider_vel.on_changed(lambda val: setattr(estado, 'velocidade_simulacao', val))

def init():
    curva_plot.set_data([], [])
    bolinha.set_data([], [])
    trajeto.set_data([], [])
    normal_linha.set_data([], [])
    vel_linha.set_data([], [])
    tangente_linha.set_data([], [])
    proxima_linha.set_data([], [])
    angulo_plot.set_data([], [])
    texto_info.set_text('Pronto para iniciar')
    texto_funcao.set_text('')
    return curva_plot, bolinha, trajeto, normal_linha, vel_linha, tangente_linha, proxima_linha, angulo_plot, texto_info, texto_funcao

def update(frame):
    if estado.pausado:
        return curva_plot, bolinha, trajeto, normal_linha, vel_linha, tangente_linha, proxima_linha, angulo_plot, texto_info, texto_funcao
    
    dt = 0.015 * estado.velocidade_simulacao
    nova_pos = estado.pos + estado.vel * dt
    
    # Usar novo método de detecção de colisão
    ponto_colisao, t_colisao = encontrar_colisao_robusta(estado.pos, estado.vel * dt)
    
    if ponto_colisao is not None and t_colisao is not None:
        # Verificar se não é colisão repetida
        if estado.ultima_colisao is None or np.linalg.norm(ponto_colisao - estado.ultima_colisao) > 0.05:
            try:
                normal = estado.funcao_parametrica.normal(t_colisao)
                estado.pos = ponto_colisao + normal * 0.01
                
                if estado.modo_bilhar == 'Simpletico':
                    # Bilhar simplético: usar ponto anterior e ponto atual para calcular próximo ponto
                    if estado.ultimo_ponto is None:
                        # Primeira colisão, usa reflexão convencional
                        estado.vel = refletir_vetor(estado.vel, normal) * 0.99
                        estado.ultimo_ponto = estado.trajetoria[-2] if len(estado.trajetoria) >= 2 else ponto_colisao
                    else:
                        # Calcular próximo ponto z com novo método otimizado
                        z, s_z = encontrar_proximo_ponto_otimizado(estado.ultimo_ponto, ponto_colisao, t_colisao)
                        
                        if z is not None:
                            # Calcular nova direção (de y para z)
                            nova_direcao = z - ponto_colisao
                            magnitude = np.linalg.norm(nova_direcao)
                            if magnitude > 0:
                                # Atualizar velocidade para direção de z
                                estado.vel = nova_direcao / magnitude * np.linalg.norm(estado.vel)
                                
                                # Atualizar elementos visuais
                                tang = estado.funcao_parametrica.tangente(t_colisao)
                                estado.tangente_atual = tang
                                estado.proximo_ponto = z
                                
                                tangente_linha.set_data(
                                    [ponto_colisao[0], ponto_colisao[0] + tang[0]],
                                    [ponto_colisao[1], ponto_colisao[1] + tang[1]]
                                )
                                proxima_linha.set_data(
                                    [estado.ultimo_ponto[0], z[0]],
                                    [estado.ultimo_ponto[1], z[1]]
                                )
                    
                    # Atualizar último ponto para a próxima colisão
                    estado.ultimo_ponto = ponto_colisao.copy()
                else:
                    # Modo convencional
                    estado.vel = refletir_vetor(estado.vel, normal) * 0.99
                    estado.ultimo_ponto = None
                    estado.proximo_ponto = None
                
                estado.ultima_colisao = ponto_colisao
                
                # Calcular ângulo de colisão
                direcao_incidente = -estado.vel / np.linalg.norm(estado.vel)
                angulo = np.degrees(np.arccos(np.clip(np.dot(direcao_incidente, normal), -1, 1)))
                estado.angulos_colisao.append(angulo)
                estado.t_colisao.append(t_colisao)
                estado.num_colisoes += 1
                
                if estado.t_colisao and estado.angulos_colisao:
                    angulo_plot.set_data(estado.t_colisao, estado.angulos_colisao)
                
                texto_info.set_text(
                    f"Modo: {estado.modo_bilhar}\n"
                    f"Colisões: {estado.num_colisoes}\n"
                    f"Ângulo: {angulo:.1f}°\n"
                    f"t: {t_colisao:.2f} rad"
                )
            except Exception as e:
                print(f"Erro durante colisão: {e}")
                estado.pos = nova_pos
    else:
        estado.pos = nova_pos
    
    estado.trajetoria.append(estado.pos.copy())
    
    # Limitar o tamanho da trajetória
    if len(estado.trajetoria) > 1000:
        estado.trajetoria.pop(0)
    
    # Atualiza gráficos
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data([p[0] for p in estado.trajetoria], [p[1] for p in estado.trajetoria])
    
    # Atualizar linhas de normal e velocidade
    if estado.ultima_colisao is not None:
        try:
            t_last = estado.t_colisao[-1] if estado.t_colisao else 0
            normal = estado.funcao_parametrica.normal(t_last)
            normal_linha.set_data(
                [estado.ultima_colisao[0], estado.ultima_colisao[0] + normal[0]],
                [estado.ultima_colisao[1], estado.ultima_colisao[1] + normal[1]]
            )
            vel_linha.set_data(
                [estado.ultima_colisao[0], estado.ultima_colisao[0] + estado.vel[0]],
                [estado.ultima_colisao[1], estado.ultima_colisao[1] + estado.vel[1]]
            )
        except:
            pass
    
    return curva_plot, bolinha, trajeto, normal_linha, vel_linha, tangente_linha, proxima_linha, angulo_plot, texto_info, texto_funcao

# Inicialização
reset_simulacao(None)
atualizar_curva()
atualizar_visibilidade_posicao()

ani = FuncAnimation(fig, update, frames=None, init_func=init, blit=False, interval=20, cache_frame_data=False)

plt.show()