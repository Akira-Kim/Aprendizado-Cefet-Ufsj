import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox, RadioButtons
from matplotlib import gridspec, patches
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
        """Calcula o vetor normal unitário com fallback robusto"""
        # Tentar calcular a derivada em pontos próximos para evitar singularidades
        pontos = []
        for dt in [-1e-4, 0, 1e-4]:
            t_adj = (t + dt) % (2*np.pi)
            deriv = self.derivada(t_adj)
            norm_deriv = np.linalg.norm(deriv)
            if norm_deriv > 1e-8:
                pontos.append(deriv / norm_deriv)
        
        if not pontos:
            return np.array([0.0, 1.0])  # Fallback
        
        # Usar a média das derivadas válidas
        deriv_media = np.mean(pontos, axis=0)
        norm_media = np.linalg.norm(deriv_media)
        if norm_media < 1e-8:
            return np.array([0.0, 1.0])
        
        deriv_media /= norm_media
        return np.array([-deriv_media[1], deriv_media[0]])
    
    def tangente(self, t):
        """Calcula o vetor tangente unitário"""
        deriv = self.derivada(t)
        norm = np.linalg.norm(deriv)
        if norm == 0:
            return np.array([0.0, 1.0])
        return deriv / norm
    
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
        self.controls_visible = False  # Controles visíveis ou não

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

def encontrar_colisao_precisa(ponto, direcao, max_iter=10, tol=1e-5):
    """Detecção de colisão usando método de Newton para encontrar interseção exata"""
    if np.linalg.norm(direcao) < 1e-8:
        return None, None
    
    # Tentativa inicial usando o método robusto
    ponto_estimado, t_estimado = encontrar_colisao_robusta(ponto, direcao)
    if ponto_estimado is None:
        return None, None
    
    # Refinamento usando método de Newton
    t = t_estimado
    for _ in range(max_iter):
        f_t = estado.funcao_parametrica(t)
        f_prime = estado.funcao_parametrica.derivada(t)
        
        # Vetor do ponto inicial ao ponto na curva
        r = f_t - ponto
        
        # Função objetivo: (r × direcao) = 0 (perpendicularidade)
        F = np.cross(r, direcao)
        
        # Derivada da função objetivo
        F_prime = np.cross(f_prime, direcao)
        
        if abs(F_prime) < tol:
            break
            
        delta_t = -F / F_prime
        t += delta_t
        
        # Garantir que t permaneça no intervalo [0, 2π]
        t = t % (2 * np.pi)
        
        if abs(delta_t) < tol:
            break
    
    ponto_final = estado.funcao_parametrica(t)
    return ponto_final, t

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

fig = plt.figure(figsize=(16, 12))
fig.set_facecolor('#f0f0f5')

# Criação de um GridSpec principal
gs_main = gridspec.GridSpec(2, 1, height_ratios=[8, 2], hspace=0.05)

# Área para os gráficos
gs_graficos = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs_main[0], width_ratios=[2, 1])
ax = fig.add_subplot(gs_graficos[0])
ax.set_facecolor('#fafafa')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title("Bilhar Paramétrico", pad=20, fontsize=16, color='#333333')

ax2 = fig.add_subplot(gs_graficos[1])
ax2.set_facecolor('#fafafa')
ax2.grid(True, alpha=0.3)
ax2.set_title("Ângulo de Colisão vs Posição na Curva", pad=20, fontsize=14)
ax2.set_xlabel("Parâmetro t (0 a 2π)", fontsize=10)
ax2.set_ylabel("Ângulo de Colisão (°)", fontsize=10)
ax2.set_xlim(0, 2*np.pi)
ax2.set_ylim(0, 180)

# Área para controles (inicialmente invisível)
ax_controles = fig.add_subplot(gs_main[1])
ax_controles.set_axis_off()
ax_controles.set_visible(False)

# Área para página inicial - Fundo mais opaco
ax_inicial = fig.add_axes([0, 0, 1, 1])
ax_inicial.set_axis_off()
ax_inicial.set_facecolor('#1c1c2a')  # Cor mais escura e opaca

# Elementos da página inicial
titulo = ax_inicial.text(0.5, 0.6, "Bilhar Paramétrico", 
                         ha='center', va='center', fontsize=32, color='white', weight='bold')
subtitulo = ax_inicial.text(0.5, 0.5, "Simulador de Sistemas Dinâmicos em Curvas Paramétricas", 
                           ha='center', va='center', fontsize=18, color='#ecf0f1')
autores = ax_inicial.text(0.5, 0.4, "Desenvolvido por: Akira e Ivana", 
                         ha='center', va='center', fontsize=14, color='#bdc3c7')
btn_iniciar_ax = plt.axes([0.4, 0.3, 0.2, 0.08])
btn_iniciar = Button(btn_iniciar_ax, 'INICIAR SIMULAÇÃO', color='#27ae60', hovercolor='#2ecc71')
btn_iniciar.label.set_fontsize(14)

# === Elementos Visuais ===
curva_plot, = ax.plot([], [], 'k-', linewidth=2, alpha=0.8)
bolinha, = ax.plot([], [], 'ro', markersize=8, zorder=3)
trajeto, = ax.plot([], [], 'r-', linewidth=1, alpha=0.7)
normal_linha, = ax.plot([], [], 'b--', linewidth=1.5, alpha=0.7)
vel_linha, = ax.plot([], [], 'g-', linewidth=1.5, alpha=0.7)
tangente_linha, = ax.plot([], [], 'm-', linewidth=1.5, alpha=0.7)  # Para bilhar simplético
proxima_linha, = ax.plot([], [], 'c-', linewidth=1.5, alpha=0.7)    # Para bilhar simplético

angulo_plot, = ax2.plot([], [], 'ro', markersize=5, alpha=0.7)

texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.9, edgecolor='#cccccc'))
texto_funcao = ax.text(0.02, 0.85, '', transform=ax.transAxes, fontsize=9,
                      bbox=dict(facecolor='white', alpha=0.9, edgecolor='#cccccc'))

# === Controles Interativos - Reorganizados ===
# Botão para mostrar/ocultar controles
ax_btn_controles = plt.axes([0.01, 0.01, 0.1, 0.04])
btn_controles = Button(ax_btn_controles, 'Controles', color='#3498db')
ax_btn_controles.set_visible(False)  # Inicialmente oculto

# === REORGANIZAÇÃO COMPLETA DOS CONTROLES ===

# --- Grupo 1: Seleção de Função e Modos ---
# Rótulo para Funções
ax.add_patch(patches.Rectangle((0.02, 0.15), 0.15, 0.07, transform=fig.transFigure, 
                              facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax_radio = plt.axes([0.03, 0.16, 0.13, 0.05])
radio = RadioButtons(ax_radio, ['Elipse', 'Astroide', 'Cardioide', 'Lemniscata', 'Personalizada'], active=0)
ax_radio.set_visible(False)
ax.text(0.09, 0.22, "Função", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

# Rótulo para Modo de Bilhar
ax.add_patch(patches.Rectangle((0.18, 0.15), 0.15, 0.07, transform=fig.transFigure, 
                              facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax_radio_modo = plt.axes([0.19, 0.16, 0.13, 0.05])
radio_modo = RadioButtons(ax_radio_modo, ['Convencional', 'Simpletico'], active=0)
ax_radio_modo.set_visible(False)
ax.text(0.255, 0.22, "Modo de Bilhar", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

# Rótulo para Modo de Início
ax.add_patch(patches.Rectangle((0.34, 0.15), 0.15, 0.07, transform=fig.transFigure, 
                              facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax_radio_posicao = plt.axes([0.35, 0.16, 0.13, 0.05])
radio_posicao = RadioButtons(ax_radio_posicao, ['Livre', 'Borda'], active=0)
ax_radio_posicao.set_visible(False)
ax.text(0.415, 0.22, "Posição Inicial", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

# --- Grupo 2: Parâmetros da curva ---
ax.add_patch(patches.Rectangle((0.50, 0.15), 0.20, 0.07, transform=fig.transFigure, 
                              facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax.text(0.60, 0.22, "Parâmetros da Curva", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

ax_texto_a = plt.axes([0.51, 0.16, 0.06, 0.04])
texto_a = TextBox(ax_texto_a, 'a', initial='2.0')
ax_texto_a.set_visible(False)

ax_texto_b = plt.axes([0.58, 0.16, 0.06, 0.04])
texto_b = TextBox(ax_texto_b, 'b', initial='2.0')
ax_texto_b.set_visible(False)

ax_texto_n = plt.axes([0.65, 0.16, 0.06, 0.04])
texto_n = TextBox(ax_texto_n, 'n', initial='1.0')
ax_texto_n.set_visible(False)

# --- Grupo 3: Posição e Ângulo ---
ax.add_patch(patches.Rectangle((0.02, 0.05), 0.35, 0.09, transform=fig.transFigure, 
                              facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax.text(0.195, 0.12, "Configuração Inicial", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

# Sliders de posição (modo livre)
ax_posx = plt.axes([0.03, 0.09, 0.15, 0.02])
slider_posx = Slider(ax_posx, 'Posição X', -3.9, 3.9, valinit=1.0, valstep=0.1)
ax_posx.set_visible(False)

ax_posy = plt.axes([0.03, 0.06, 0.15, 0.02])
slider_posy = Slider(ax_posy, 'Posição Y', -3.9, 3.9, valinit=1.0, valstep=0.1)
ax_posy.set_visible(False)

# Slider para posição na borda (modo borda)
ax_pos_t = plt.axes([0.03, 0.06, 0.15, 0.02])
slider_pos_t = Slider(ax_pos_t, 't (0 a 2π)', 0, 2*np.pi, valinit=0, valstep=0.01)
ax_pos_t.set_visible(False)

# Slider de ângulo
ax_angulo = plt.axes([0.20, 0.09, 0.15, 0.02])
slider_angulo = Slider(ax_angulo, 'Ângulo (graus)', 0, 360, valinit=30, valstep=1)
ax_angulo.set_visible(False)

# Slider de velocidade
ax_vel = plt.axes([0.20, 0.06, 0.15, 0.02])
slider_vel = Slider(ax_vel, 'Velocidade', 0.1, 3.0, valinit=1.0, valstep=0.1)
ax_vel.set_visible(False)

# --- Grupo 4: Botões de Controle ---
ax.add_patch(patches.Rectangle((0.50, 0.05), 0.48, 0.09, transform=fig.transFigure, 
                              facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax.text(0.74, 0.12, "Controles da Simulação", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

ax_botao_reset = plt.axes([0.52, 0.06, 0.08, 0.04])
botao_reset = Button(ax_botao_reset, 'Reset', color='#ffdddd')
ax_botao_reset.set_visible(False)

ax_botao_pause = plt.axes([0.62, 0.06, 0.08, 0.04])
botao_pause = Button(ax_botao_pause, 'Pausar', color='#ddddff')
ax_botao_pause.set_visible(False)

ax_botao_start = plt.axes([0.72, 0.06, 0.08, 0.04])
botao_start = Button(ax_botao_start, 'Iniciar', color='#ddffdd')
ax_botao_start.set_visible(False)

ax_botao_info = plt.axes([0.82, 0.06, 0.08, 0.04])
botao_info = Button(ax_botao_info, 'Ajuda', color='#ffffdd')
ax_botao_info.set_visible(False)

# === Funções de Atualização ===
def mostrar_controles():
    """Mostra todos os controles da simulação"""
    estado.controls_visible = True
    # Mostrar os eixos dos controles
    ax_controles.set_visible(True)
    ax_radio.set_visible(True)
    ax_radio_modo.set_visible(True)
    ax_radio_posicao.set_visible(True)
    # Atualizar a visibilidade dos controles de posição
    atualizar_visibilidade_posicao()
    ax_angulo.set_visible(True)
    ax_vel.set_visible(True)
    ax_texto_a.set_visible(True)
    ax_texto_b.set_visible(True)
    ax_texto_n.set_visible(True)
    ax_botao_reset.set_visible(True)
    ax_botao_pause.set_visible(True)
    ax_botao_start.set_visible(True)
    ax_botao_info.set_visible(True)
    # Mudar o texto do botão de controles
    btn_controles.label.set_text('Ocultar Controles')
    fig.canvas.draw()

def ocultar_controles():
    """Oculta todos os controles da simulação"""
    estado.controls_visible = False
    # Ocultar os eixos dos controles
    ax_controles.set_visible(False)
    ax_radio.set_visible(False)
    ax_radio_modo.set_visible(False)
    ax_radio_posicao.set_visible(False)
    ax_posx.set_visible(False)
    ax_posy.set_visible(False)
    ax_pos_t.set_visible(False)
    ax_angulo.set_visible(False)
    ax_vel.set_visible(False)
    ax_texto_a.set_visible(False)
    ax_texto_b.set_visible(False)
    ax_texto_n.set_visible(False)
    ax_botao_reset.set_visible(False)
    ax_botao_pause.set_visible(False)
    ax_botao_start.set_visible(False)
    ax_botao_info.set_visible(False)
    # Mudar o texto do botão de controles
    btn_controles.label.set_text('Mostrar Controles')
    fig.canvas.draw()

def toggle_controles(event):
    """Alterna entre mostrar e ocultar controles"""
    if estado.controls_visible:
        ocultar_controles()
    else:
        mostrar_controles()

# Variável global para a animação
ani = None

def iniciar_simulacao_pagina(event):
    """Transição da página inicial para a simulação"""
    global ani
    
    ax_inicial.set_visible(False)
    btn_iniciar_ax.set_visible(False)
    
    # Mostrar os gráficos
    ax.set_visible(True)
    ax2.set_visible(True)
    
    # Mostrar o botão de controles
    ax_btn_controles.set_visible(True)
    
    # Inicializar a simulação
    reset_simulacao(None)
    
    # Criar a animação somente agora (após tornar os eixos visíveis)
    ani = FuncAnimation(
        fig, 
        update, 
        frames=None, 
        init_func=init, 
        blit=False, 
        interval=20, 
        cache_frame_data=False
    )
    
    fig.canvas.draw()

def atualizar_visibilidade_posicao():
    """Atualiza a visibilidade dos controles de posição"""
    if estado.modo_inicio == 'Livre':
        ax_posx.set_visible(True)
        ax_posy.set_visible(True)
        ax_pos_t.set_visible(False)
        slider_angulo.label.set_color('black')
    else:  # Modo 'Borda'
        ax_posx.set_visible(False)
        ax_posy.set_visible(False)
        ax_pos_t.set_visible(True)
        slider_angulo.label.set_color('gray')

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
        
        # Calcular tangente e definir direção inicial
        tang = estado.funcao_parametrica.tangente(t_val)
        velocidade = min(slider_vel.val, 3.0)
        estado.vel = tang * velocidade
        
        # Calcular e atualizar ângulo visualmente
        angulo = np.degrees(np.arctan2(tang[1], tang[0])) % 360
        slider_angulo.set_val(angulo)
        
        if estado.pausado or estado.primeiro_inicio:
            estado.trajetoria = [estado.pos.copy()]
            bolinha.set_data([estado.pos[0]], [estado.pos[1]])
            fig.canvas.draw_idle()
    else:
        # Restaurar direção definida pelo ângulo
        angulo_rad = np.radians(slider_angulo.val)
        velocidade = min(slider_vel.val, 3.0)
        estado.vel = np.array([np.cos(angulo_rad), np.sin(angulo_rad)]) * velocidade

btn_controles.on_clicked(toggle_controles)
btn_iniciar.on_clicked(iniciar_simulacao_pagina)
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
    
    # Se estiver no modo borda, atualizar a posição
    if estado.modo_inicio == 'Borda':
        t_val = slider_pos_t.val
        estado.pos = estado.funcao_parametrica(t_val)
        slider_posx.set_val(estado.pos[0])
        slider_posy.set_val(estado.pos[1])
        
        # Atualizar direção pela tangente
        tang = estado.funcao_parametrica.tangente(t_val)
        velocidade = min(slider_vel.val, 3.0)
        estado.vel = tang * velocidade
        
        # Atualizar ângulo visualmente
        angulo = np.degrees(np.arctan2(tang[1], tang[0])) % 360
        slider_angulo.set_val(angulo)
    
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
        
        # Definir direção pela tangente
        tang = estado.funcao_parametrica.tangente(t_val)
        velocidade = min(slider_vel.val, 3.0)
        estado.vel = tang * velocidade
        
        # Atualizar ângulo visualmente
        angulo = np.degrees(np.arctan2(tang[1], tang[0])) % 360
        slider_angulo.set_val(angulo)
    
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
    botao_pause.label.set_text('Continuar')
    botao_pause.on_clicked(None)
    botao_pause.on_clicked(continuar_simulacao)

def continuar_simulacao(event):
    estado.pausado = False
    texto_info.set_text('Simulação em andamento')
    botao_pause.label.set_text('Pausar')
    botao_pause.on_clicked(None)
    botao_pause.on_clicked(pausar_simulacao)

def iniciar_simulacao(event):
    if estado.primeiro_inicio:
        if estado.modo_inicio == 'Livre':
            angulo_rad = np.radians(slider_angulo.val)
            velocidade = min(slider_vel.val, 3.0)
            estado.vel = np.array([np.cos(angulo_rad), np.sin(angulo_rad)]) * velocidade
        estado.primeiro_inicio = False
    
    estado.pausado = False
    texto_info.set_text('Simulação em andamento')
    botao_pause.label.set_text('Pausar')
    botao_pause.on_clicked(None)
    botao_pause.on_clicked(pausar_simulacao)

def mostrar_info(event):
    texto_info.set_text(
        "Modo Simplético:\n"
        "Reflexão baseada na área do triângulo\n"
        "x -> y -> z onde xz ∥ tangente(y)\n\n"
        "Modo Convencional:\n"
        "Reflexão padrão: ângulo incidência = reflexão\n\n"
        "Modo Borda:\n"
        "A bolinha começa na borda da curva\n"
        "e segue na direção da tangente"
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
        
        # Atualizar direção pela tangente
        tang = estado.funcao_parametrica.tangente(t_val)
        velocidade = min(slider_vel.val, 3.0)
        estado.vel = tang * velocidade
        
        # Atualizar ângulo visualmente
        angulo = np.degrees(np.arctan2(tang[1], tang[0])) % 360
        slider_angulo.set_val(angulo)
        
        if estado.pausado or estado.primeiro_inicio:
            estado.trajetoria = [estado.pos.copy()]
            bolinha.set_data([estado.pos[0]], [estado.pos[1]])
            fig.canvas.draw_idle()

def update_angulo(val):
    if estado.modo_inicio == 'Livre' and (estado.pausado or estado.primeiro_inicio):
        angulo_rad = np.radians(slider_angulo.val)
        velocidade = min(slider_vel.val, 3.0)
        estado.vel = np.array([np.cos(angulo_rad), np.sin(angulo_rad)]) * velocidade

slider_posx.on_changed(update_posicao)
slider_posy.on_changed(update_posicao)
slider_pos_t.on_changed(update_posicao_t)
slider_angulo.on_changed(update_angulo)
slider_vel.on_changed(lambda val: setattr(estado, 'velocidade_simulacao', val))

def init():
    """Função de inicialização com verificação de visibilidade"""
    # Não inicializar se os elementos principais não estiverem visíveis
    if not ax.get_visible() or not ax2.get_visible():
        return (curva_plot, bolinha, trajeto, normal_linha, vel_linha, 
                tangente_linha, proxima_linha, angulo_plot, 
                texto_info, texto_funcao)
    
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
    return (curva_plot, bolinha, trajeto, normal_linha, vel_linha, 
            tangente_linha, proxima_linha, angulo_plot, 
            texto_info, texto_funcao)

def update(frame):
    """Função de atualização com verificação de visibilidade"""
    # Não atualizar se os elementos principais não estiverem visíveis
    if not ax.get_visible() or not ax2.get_visible():
        return (curva_plot, bolinha, trajeto, normal_linha, vel_linha, 
                tangente_linha, proxima_linha, angulo_plot, 
                texto_info, texto_funcao)
    
    if estado.pausado:
        return (curva_plot, bolinha, trajeto, normal_linha, vel_linha, 
                tangente_linha, proxima_linha, angulo_plot, 
                texto_info, texto_funcao)
    
    dt = 0.015 * estado.velocidade_simulacao
    nova_pos = estado.pos + estado.vel * dt
    
    # Usar novo método de detecção de colisão
    ponto_colisao, t_colisao = encontrar_colisao_precisa(estado.pos, estado.vel * dt)
    
    if ponto_colisao is not None and t_colisao is not None:
        # Verificar se não é colisão repetida
        if estado.ultima_colisao is None or np.linalg.norm(ponto_colisao - estado.ultima_colisao) > 0.05:
            try:
                # Calcular normal de forma mais precisa
                normal = estado.funcao_parametrica.normal(t_colisao)
                
                # Ajuste crucial: mover a bolinha para o ponto de colisão + um pequeno deslocamento na direção da normal
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
    
    return (curva_plot, bolinha, trajeto, normal_linha, vel_linha, 
            tangente_linha, proxima_linha, angulo_plot, 
            texto_info, texto_funcao)

# === Execução Principal ===
if __name__ == "__main__":
    plt.show()