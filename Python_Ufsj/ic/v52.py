"""
Simulador Interativo de Bilhares Simpléticos (versão do artigo)
================================================================
Fronteiras: Círculo e Elipse (suaves).
Modos: Elástico e Simplético.
No modo Simplético NÃO há fallback para reflexão elástica.

Referência teórica: Albers & Tabachnikov (2018).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox, RadioButtons
from matplotlib import gridspec, patches


# =====================================================================
# GEOMETRIA DA MESA
# =====================================================================

class CurvaParametrica:
    """
    Representa a fronteira da mesa de bilhar como curva paramétrica.

    Usada em: todo cálculo geométrico (ponto, tangente, normal,
    interseção reta–curva, recuperação do parâmetro t).

    Curvas disponíveis: Círculo e Elipse (fechadas e suaves).
    """

    def __init__(self):
        """
        Inicializa a curva no círculo unitário.
        Quando: criação do estado da simulação / reset.
        """
        self.curvas = {
            'Círculo': self.circulo,
            'Elipse': self.elipse,
        }
        self.parametro_a = 1.0   # semi-eixo x (elipse)
        self.parametro_b = 1.0   # semi-eixo y (elipse)
        self.curva_atual = 'Círculo'

    def __call__(self, t):
        """
        Avalia a curva no parâmetro t.

        Retorna: array [t, x(t), y(t)].
        Quando: sempre que se precisa de um ponto da fronteira.
        """
        try:
            return self.curvas[self.curva_atual](t)
        except Exception:
            return np.array([0.0, 0.0, 0.0])

    def circulo(self, t):
        """
        Círculo unitário: (cos t, sin t).
        Quando: curva_atual == 'Círculo'.
        """
        return np.array([t, np.cos(t), np.sin(t)])

    def elipse(self, t):
        """
        Elipse: (a cos t, b sin t).
        Quando: curva_atual == 'Elipse'.
        """
        a, b = self.parametro_a, self.parametro_b
        return np.array([t, a * np.cos(t), b * np.sin(t)])

    def intersect_line(self, point, direction):
        """
        Interseção da reta (point + λ * direction) com a curva atual.

        Resolve a equação quadrática da elipse/círculo.
        Retorna: lista de λ (0, 1 ou 2 valores).

        Quando:
        - localizar a próxima colisão da partícula;
        - construir o ponto a3 na colisão simplética.
        """
        if self.curva_atual == 'Círculo':
            aa = bb = 1.0
        else:
            aa = self.parametro_a
            bb = self.parametro_b

        px, py = point
        dx, dy = direction
        A = (dx / aa) ** 2 + (dy / bb) ** 2
        B = 2 * (px * dx / aa ** 2 + py * dy / bb ** 2)
        C = (px / aa) ** 2 + (py / bb) ** 2 - 1

        disc = B ** 2 - 4 * A * C
        if disc < 0:
            return []
        if abs(A) < 1e-16:
            return [0.0]

        sd = np.sqrt(disc)
        l1 = (-B + sd) / (2 * A)
        l2 = (-B - sd) / (2 * A)
        return [l1, l2]

    def get_tangente(self, t):
        """
        Tangente unitária T(t) no ponto r(t).

        Quando:
        - montar a condição inicial (direção da velocidade);
        - construir a colisão simplética (direção da reta auxiliar);
        - calcular cos θ no espaço de fase.
        """
        if self.curva_atual == 'Círculo':
            return np.array([-np.sin(t), np.cos(t)])
        a, b = self.parametro_a, self.parametro_b
        d = np.array([-a * np.sin(t), b * np.cos(t)])
        norm = np.linalg.norm(d)
        return d / norm if norm > 1e-12 else np.array([1.0, 0.0])

    def get_normal(self, t):
        """
        Normal unitária N(t) apontando para o INTERIOR da mesa.

        Quando:
        - reflexão elástica;
        - checagem de direção na colisão simplética.
        """
        tng = self.get_tangente(t)
        n = np.array([-tng[1], tng[0]])  # rotação 90°
        p = self(t)
        pos = np.array([p[1], p[2]])
        # garante que aponta para dentro (origem)
        if np.dot(n, pos) > 0:
            n = -n
        return n

    def get_t_from_pos(self, pos_plane):
        """
        Recupera o parâmetro t ∈ [0, 2π) a partir de um ponto (x, y)
        aproximadamente sobre a curva.

        Quando: após detectar o ponto de impacto (hit_pos).
        """
        x, y = pos_plane
        if self.curva_atual == 'Círculo':
            t = np.arctan2(y, x)
        else:
            a, b = self.parametro_a, self.parametro_b
            t = np.arctan2(y / b, x / a)
        return t if t >= 0 else t + 2 * np.pi


# =====================================================================
# ESTADO DA SIMULAÇÃO
# =====================================================================

class EstadoBilhar:
    """
    Armazena todo o estado dinâmico e de interface da simulação.

    Quando: criado no início do programa; atualizado a cada colisão
    e a cada interação do usuário com os controles.
    """

    def __init__(self):
        """
        Define condição inicial padrão:
        - partícula em (1, 0) no círculo;
        - modo Elástico;
        - simulação pausada.
        """
        self.pausado = True
        self.primeiro_inicio = True   # True = ainda dá para mudar condição inicial
        self.modo_bilhar = 'Elástico'

        self.pos = np.array([1.0, 0.0])
        self.t = 0.0
        self.vel = np.array([-1.0, 1.0]) / np.sqrt(2)
        self.angulo_vel = 0.25 * np.pi
        self.velocidade_simulacao = 1.0

        self.curva_parametrica = CurvaParametrica()
        self.curve_points = None

        self.traj_x = [self.pos[0]]
        self.traj_y = [self.pos[1]]
        self.trajetoria_aux_x = []   # linha ciano (construção simplética)
        self.trajetoria_aux_y = []

        self.lista_t_colisao = []        # eixo x do espaço de fase (t/π)
        self.lista_angulo_colisao = []   # eixo y do espaço de fase (cos θ)
        self.cos_angulo = 0.0
        self.reset_all = False

        self.heatmap = None
        self.heatmap_bins = 120

    def reset(self):
        """
        Restaura o estado inicial e limpa trajetória / heatmap.

        Quando: usuário clica em Reset.
        """
        self.pausado = True
        self.primeiro_inicio = True
        self.pos = np.array([1.0, 0.0])
        self.t = 0.0
        self.vel = np.array([-1.0, 1.0]) / np.sqrt(2)
        self.angulo_vel = 0.25 * np.pi
        self.velocidade_simulacao = 1.0
        self.curva_parametrica = CurvaParametrica()
        self.curve_points = None

        self.traj_x = [self.pos[0]]
        self.traj_y = [self.pos[1]]
        self.trajetoria_aux_x = []
        self.trajetoria_aux_y = []

        self.lista_t_colisao = []
        self.lista_angulo_colisao = []
        self.cos_angulo = 0.0

        if self.heatmap is not None:
            self.heatmap.set_data(np.zeros((self.heatmap_bins, self.heatmap_bins)))
            self.heatmap.set_clim(0, 1)

        self.reset_all = False


# =====================================================================
# FÍSICA
# =====================================================================

def refletir_vetor(v, n):
    """
    Reflexão elástica clássica: v' = v - 2 (v·n) n.

    Quando: SOMENTE no modo 'Elástico', no instante da colisão.
    Não é usada no modo Simplético.
    """
    return v - 2 * np.dot(v, n) * n


def colisao_simpletica_robusta(curva, t_hit, hit_pos, t_anterior, vel):
    """
    Colisão simplética (Albers–Tabachnikov) SEM fallback elástico.

    Construção:
      a1 = r(t_anterior)     ponto anterior na fronteira
      a2 = hit_pos           ponto de impacto atual
      T  = tangente em a2
      a3 = outra interseção da reta (a1 + λ T) com a fronteira
      nova velocidade = direção (a3 - a2)

    Estratégia:
      1) interseção analítica (equação quadrática);
      2) se falhar, resolve f(s) = <r(s)-a1, N(a2)> = 0 por bisseção;
      3) se ainda falhar, mantém a velocidade (não troca de lei).

    Quando: modo_bilhar == 'Simplético', a cada colisão.
    """
    p_ant = curva(t_anterior)
    a1 = np.array([p_ant[1], p_ant[2]], dtype=float)

    T = curva.get_tangente(t_hit)
    N = curva.get_normal(t_hit)

    # ----- Tentativa 1: interseção analítica -----
    lambdas = curva.intersect_line(a1, T)
    candidatos = []
    for lam in lambdas:
        if abs(lam) < 1e-8:
            continue
        z = a1 + lam * T
        if np.linalg.norm(z - hit_pos) < 1e-7:
            continue
        if np.linalg.norm(z - a1) < 1e-7:
            continue
        candidatos.append((abs(lam), z))

    if candidatos:
        candidatos.sort(key=lambda x: x[0])
        z_pos = candidatos[0][1]
        nova_vel = z_pos - hit_pos
        norma = np.linalg.norm(nova_vel)
        if norma > 1e-12:
            nova_vel = nova_vel / norma
            # se aponta para fora, tenta o outro candidato
            if np.dot(nova_vel, N) < 0 and len(candidatos) > 1:
                z_pos = candidatos[1][1]
                nova_vel = z_pos - hit_pos
                norma = np.linalg.norm(nova_vel)
                if norma > 1e-12:
                    nova_vel = nova_vel / norma
            if np.dot(nova_vel, N) >= 0:
                return (
                    nova_vel,
                    [float(a1[0]), float(z_pos[0])],
                    [float(a1[1]), float(z_pos[1])],
                )

    # ----- Tentativa 2: raiz de f(s) = <r(s)-a1, N> = 0 -----
    def f(s):
        p = curva(s)
        r = np.array([p[1], p[2]], dtype=float)
        return float(np.dot(r - a1, N))

    def dist_ang(a, b):
        d = abs(a - b) % (2 * np.pi)
        return min(d, 2 * np.pi - d)

    n_sample = 80
    ts = np.linspace(0, 2 * np.pi, n_sample, endpoint=False)
    melhor_s = None
    melhor_val = np.inf

    for i in range(n_sample):
        s0 = ts[i]
        s1 = ts[(i + 1) % n_sample]
        # evita vizinhança de t_hit e t_anterior
        if dist_ang(s0, t_hit) < 0.05 or dist_ang(s0, t_anterior) < 0.05:
            continue
        f0, f1 = f(s0), f(s1)
        if f0 * f1 > 0:
            continue
        lo, hi = s0, s1
        if hi < lo:
            hi += 2 * np.pi
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if f(lo % (2 * np.pi)) * f(mid % (2 * np.pi)) <= 0:
                hi = mid
            else:
                lo = mid
        s_star = mid % (2 * np.pi)
        val = abs(f(s_star))
        if val < melhor_val:
            melhor_val = val
            melhor_s = s_star

    if melhor_s is not None and melhor_val < 1e-5:
        p = curva(melhor_s)
        z_pos = np.array([p[1], p[2]], dtype=float)
        nova_vel = z_pos - hit_pos
        norma = np.linalg.norm(nova_vel)
        if norma > 1e-12:
            nova_vel = nova_vel / norma
            return (
                nova_vel,
                [float(a1[0]), float(z_pos[0])],
                [float(a1[1]), float(z_pos[1])],
            )

    # ----- Falha numérica: mantém velocidade (não usa elástico) -----
    norma = np.linalg.norm(vel)
    if norma > 1e-12:
        vel = vel / norma
    return vel, [], []


# =====================================================================
# INTERFACE GRÁFICA
# =====================================================================

plt.style.use('seaborn-v0_8')
plt.rcParams['font.size'] = 10

fig = plt.figure(figsize=(16, 12))
fig.set_facecolor('#f0f0f5')

gs_main = gridspec.GridSpec(2, 1, height_ratios=[8, 2], hspace=0.05)
gs_graficos = gridspec.GridSpecFromSubplotSpec(
    1, 2, subplot_spec=gs_main[0], width_ratios=[2, 1]
)

# Espaço de configuração (mesa + trajetória)
ax = fig.add_subplot(gs_graficos[0])
ax.set_facecolor('#fafafa')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title("Espaço de Configuração", pad=20, fontsize=14, color='#333333')

# Espaço de fase + mapa de calor
ax2 = fig.add_subplot(gs_graficos[1])
ax2.set_facecolor('#fafafa')
ax2.grid(True, alpha=0.3)
ax2.set_title("Espaço de Fase + Mapa de Calor (inferno)", pad=20, fontsize=14)
ax2.set_xlabel("Parâmetro t (× π)", fontsize=10)
ax2.set_ylabel("cos θ (ângulo com a tangente)", fontsize=10)
ax2.set_xlim(0, 2)
ax2.set_ylim(-1, 1)

ax_controles = fig.add_subplot(gs_main[1])
ax_controles.set_axis_off()

# Artistas gráficos (atualizados a cada frame / interação)
curva_plot, = ax.plot([], [], 'k-', linewidth=2, alpha=0.8)
bolinha, = ax.plot([], [], 'ro', markersize=6, zorder=3)
trajeto, = ax.plot([], [], 'r-', linewidth=1.2, alpha=0.75)
trajeto_aux, = ax.plot([], [], 'c--', linewidth=1.8, alpha=0.85)
normal_linha, = ax.plot([], [], 'b--', linewidth=1.5, alpha=0.6)
vel_linha, = ax.plot([], [], 'g-', linewidth=1.5, alpha=0.8)
tangente_linha, = ax.plot([], [], 'm-', linewidth=1.5, alpha=0.6)

colisao_plot, = ax2.plot([], [], 'ro', markersize=3.5, alpha=0.98, zorder=10)
texto_info = ax.text(
    0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
    bbox=dict(facecolor='white', alpha=0.95, edgecolor='#cccccc')
)

# ---- Controles: fronteira ----
ax.add_patch(patches.Rectangle(
    (0.05, 0.15), 0.15, 0.07, transform=fig.transFigure,
    facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7
))
ax_radio = plt.axes([0.05, 0.07, 0.13, 0.1])
radio = RadioButtons(ax_radio, ['Círculo', 'Elipse'], active=0)
ax.text(0.095, 0.18, "Fronteira", transform=fig.transFigure, ha='center', fontsize=9)

# ---- Controles: parâmetros a, b ----
ax.add_patch(patches.Rectangle(
    (0.25, 0.15), 0.20, 0.07, transform=fig.transFigure,
    facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7
))
ax.text(0.25, 0.18, "Parâmetros da Curva", transform=fig.transFigure, ha='center', fontsize=9)
ax_texto_a = plt.axes([0.24, 0.14, 0.06, 0.04])
texto_a = TextBox(ax_texto_a, 'a', initial='1.0')
ax_texto_b = plt.axes([0.24, 0.10, 0.06, 0.04])
texto_b = TextBox(ax_texto_b, 'b', initial='1.0')

# ---- Controles: modo de colisão ----
ax.add_patch(patches.Rectangle(
    (0.35, 0.15), 0.15, 0.07, transform=fig.transFigure,
    facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7
))
ax_radio_modo = plt.axes([0.34, 0.07, 0.13, 0.1])
radio_modo = RadioButtons(ax_radio_modo, ['Elástico', 'Simplético'], active=0)
ax.text(0.385, 0.18, "Colisão", transform=fig.transFigure, ha='center', fontsize=9)

# ---- Controles: condição inicial ----
ax.text(0.65, 0.18, "Condição Inicial", transform=fig.transFigure, ha='center', fontsize=9)
ax_pos_t = plt.axes([0.60, 0.15, 0.15, 0.02])
slider_pos_t = Slider(ax_pos_t, 't (× π)', 0, 2, valinit=0, valstep=0.005)
ax_angulo = plt.axes([0.60, 0.11, 0.15, 0.02])
slider_angulo = Slider(ax_angulo, 'Ângulo (× π)', 0, 1, valinit=0.25, valstep=0.01)
ax_vel = plt.axes([0.60, 0.07, 0.15, 0.02])
slider_vel = Slider(ax_vel, 'Velocidade', 0.5, 4.0, valinit=1.0, valstep=0.1)

# ---- Controles: botões ----
ax.add_patch(patches.Rectangle(
    (0.50, 0.05), 0.48, 0.09, transform=fig.transFigure,
    facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7
))
ax.text(0.86, 0.18, "Controles da Simulação", transform=fig.transFigure, ha='center', fontsize=9)

ax_botao_start_pause = plt.axes([0.82, 0.13, 0.08, 0.04])
botao_start_pause = Button(ax_botao_start_pause, 'Iniciar', color='#ddffdd')
ax_botao_reset = plt.axes([0.82, 0.08, 0.08, 0.04])
botao_reset = Button(ax_botao_reset, 'Reset', color='#ffdddd')
ax_botao_info = plt.axes([0.82, 0.03, 0.08, 0.04])
botao_info = Button(ax_botao_info, 'Info', color='#ddddff')


# =====================================================================
# CALLBACKS DA INTERFACE
# =====================================================================

def preparar_simulacao(event):
    """
    Prepara o desenho inicial e cria o heatmap (uma vez).

    Quando: no arranque do programa.
    """
    global estado
    normal_linha.set_data([], [])
    vel_linha.set_data([], [])
    tangente_linha.set_data([], [])
    trajeto_aux.set_data([], [])
    texto_info.set_text('Pronto para iniciar')
    atualizar_curva_e_bolinha()

    if estado.heatmap is None:
        initial_hist = np.zeros((estado.heatmap_bins, estado.heatmap_bins))
        estado.heatmap = ax2.imshow(
            initial_hist, origin='lower',
            extent=[0, 2, -1, 1],
            cmap='inferno',
            aspect='auto',
            alpha=0.92,
            interpolation='nearest',
        )
        colisao_plot.set_zorder(10)
        estado.heatmap.set_zorder(1)
        plt.colorbar(
            estado.heatmap, ax=ax2, pad=0.02,
            label='log(1 + nº de colisões por bin)',
        )


def reset_simulacao(event):
    """
    Reinicia controles e estado físico.

    Quando: clique em Reset.
    """
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
    """
    Troca a fronteira (Círculo / Elipse).

    Quando: clique no radio de fronteira, só antes do primeiro Iniciar.
    """
    if estado.primeiro_inicio:
        estado.curva_parametrica.curva_atual = label
        atualizar_curva_e_bolinha()


def atualizar_modo(label):
    """
    Troca o modo de colisão (Elástico / Simplético).

    Quando: clique no radio de colisão, só antes do primeiro Iniciar.
    """
    if estado.primeiro_inicio:
        estado.modo_bilhar = label


def atualizar_parametros(val=None):
    """
    Lê a e b dos TextBox e redesenha a curva.

    Quando: usuário confirma valor em a ou b (Enter), só em primeiro_inicio.
    """
    if estado.primeiro_inicio:
        atualizar_curva_e_bolinha()


def atualizar_curva_e_bolinha():
    """
    Redesenha a mesa, a partícula, tangente e velocidade inicial.

    Quando:
    - mudança de curva / parâmetros / sliders (antes de iniciar);
    - após Reset.
    """
    estado.curva_parametrica.parametro_a = float(texto_a.text)
    estado.curva_parametrica.parametro_b = float(texto_b.text)

    t = np.linspace(0, 2 * np.pi, 10000)
    pontos = np.array([estado.curva_parametrica(ti) for ti in t]).T
    curva_plot.set_data(pontos[1], pontos[2])
    estado.curve_points = pontos

    ax.set_xlim(np.min(pontos[1]) - 0.6, np.max(pontos[1]) + 0.6)
    ax.set_ylim(np.min(pontos[2]) - 0.6, np.max(pontos[2]) + 0.6)

    estado.pos = np.array([
        estado.curva_parametrica(estado.t)[1],
        estado.curva_parametrica(estado.t)[2],
    ])

    tng = estado.curva_parametrica.get_tangente(estado.t)
    tangente_linha.set_data(
        [estado.pos[0], estado.pos[0] + tng[0]],
        [estado.pos[1], estado.pos[1] + tng[1]],
    )

    # velocidade a partir do ângulo com a tangente
    estado.vel = np.array([
        tng[0] * np.cos(estado.angulo_vel) - tng[1] * np.sin(estado.angulo_vel),
        tng[1] * np.cos(estado.angulo_vel) + tng[0] * np.sin(estado.angulo_vel),
    ])
    n0 = estado.curva_parametrica.get_normal(estado.t)
    if np.dot(estado.vel, n0) < 0:
        estado.vel = -estado.vel

    vel_linha.set_data(
        [estado.pos[0], estado.pos[0] + estado.vel[0]],
        [estado.pos[1], estado.pos[1] + estado.vel[1]],
    )

    bolinha.set_data([estado.pos[0]], [estado.pos[1]])

    estado.traj_x = [estado.pos[0]]
    estado.traj_y = [estado.pos[1]]
    estado.trajetoria_aux_x = []
    estado.trajetoria_aux_y = []
    trajeto.set_data(estado.traj_x, estado.traj_y)
    trajeto_aux.set_data([], [])

    colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)

    texto_info.set_text(
        f"Curva: {estado.curva_parametrica.curva_atual} | Modo: {estado.modo_bilhar}"
    )
    fig.canvas.draw_idle()


def continuar_ou_pausar_simulacao(event):
    """
    Alterna entre rodando e pausado.

    Quando: clique em Iniciar / Pausar / Continuar.
    """
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
    """
    Cria a FuncAnimation que chama update a cada frame.

    Quando: primeira vez que o usuário clica em Iniciar (ou Continuar
    após pausa, reaproveitando a animação já criada pelo Matplotlib).
    """
    global ani
    if estado.primeiro_inicio:
        estado.primeiro_inicio = False

    ani = FuncAnimation(
        fig, update, frames=None, init_func=init,
        blit=False, interval=10, cache_frame_data=False,
    )
    fig.canvas.draw()


def mostrar_info(event):
    """
    Mostra texto de ajuda na área de informação.

    Quando: clique em Info.
    """
    texto_info.set_text(
        "Simulação de Bilhares - Versão artigo (sem fallback elástico)\n"
        "• Simplético: construção analítica + raiz de f(s)=0\n"
        "• Nunca troca para reflexão elástica no modo Simplético\n"
        "• Fronteiras: Círculo e Elipse (suaves)"
    )


def update_posicao_t(val):
    """
    Atualiza o parâmetro t da condição inicial.

    Quando: movimento do slider t, só em primeiro_inicio.
    """
    if estado.primeiro_inicio:
        estado.t = val * np.pi
        atualizar_curva_e_bolinha()


def update_angulo(val):
    """
    Atualiza o ângulo da velocidade inicial (em relação à tangente).

    Quando: movimento do slider de ângulo, só em primeiro_inicio.
    """
    if estado.primeiro_inicio:
        estado.angulo_vel = val * np.pi
        atualizar_curva_e_bolinha()


def update_vel(val):
    """
    Atualiza o fator de velocidade da animação (não a física em si).

    Quando: movimento do slider de velocidade, só em primeiro_inicio.
    """
    if estado.primeiro_inicio:
        estado.velocidade_simulacao = val


# Ligação dos widgets às callbacks
slider_pos_t.on_changed(update_posicao_t)
slider_angulo.on_changed(update_angulo)
slider_vel.on_changed(update_vel)
radio.on_clicked(atualizar_curva)
radio_modo.on_clicked(atualizar_modo)
texto_a.on_submit(atualizar_parametros)
texto_b.on_submit(atualizar_parametros)
botao_reset.on_clicked(reset_simulacao)
botao_start_pause.on_clicked(continuar_ou_pausar_simulacao)
botao_info.on_clicked(mostrar_info)


def init():
    """
    Função de inicialização exigida pelo FuncAnimation.
    Quando: criação da animação.
    """
    return (
        curva_plot, bolinha, trajeto, trajeto_aux,
        normal_linha, vel_linha, tangente_linha,
        colisao_plot, texto_info,
    )


def update(frame):
    """
    Núcleo da simulação: avança o tempo e trata colisões.

    Quando: a cada frame da FuncAnimation (enquanto não pausado).

    Algoritmo:
      1. Avança no máximo dt = 0.012 * velocidade_simulacao.
      2. Calcula interseções da trajetória retilínea com a fronteira.
      3. Se houver colisão neste intervalo:
         - Elástico  → refletir_vetor
         - Simplético → colisao_simpletica_robusta (sem fallback elástico)
      4. Atualiza posição, listas de colisão, heatmap e desenho.
    """
    if estado.pausado:
        return (
            curva_plot, bolinha, trajeto, trajeto_aux,
            normal_linha, vel_linha, tangente_linha,
            colisao_plot, texto_info,
        )

    dt = 0.012 * estado.velocidade_simulacao
    time_left = dt

    while time_left > 1e-8:
        lambdas = estado.curva_parametrica.intersect_line(estado.pos, estado.vel)
        positive_lams = [lam for lam in lambdas if lam > 1e-8]

        if not positive_lams:
            # sem interseção futura (não esperado em curva fechada convexa)
            estado.pos += estado.vel * time_left
            estado.traj_x.append(estado.pos[0])
            estado.traj_y.append(estado.pos[1])
            break

        lam = min(positive_lams)

        if lam >= time_left:
            # próxima colisão está além deste passo de tempo
            estado.pos += estado.vel * time_left
            estado.traj_x.append(estado.pos[0])
            estado.traj_y.append(estado.pos[1])
            break

        # ----- colisão neste passo -----
        hit_pos = estado.pos + lam * estado.vel
        estado.traj_x.append(hit_pos[0])
        estado.traj_y.append(hit_pos[1])

        t_hit = estado.curva_parametrica.get_t_from_pos(hit_pos)

        if estado.modo_bilhar == 'Elástico':
            n = estado.curva_parametrica.get_normal(t_hit)
            estado.vel = refletir_vetor(estado.vel, n)
            norma = np.linalg.norm(estado.vel)
            if norma > 1e-12:
                estado.vel = estado.vel / norma
            estado.trajetoria_aux_x = []
            estado.trajetoria_aux_y = []
            trajeto_aux.set_data([], [])
        else:
            # Simplético: nunca usa reflexão elástica
            nova_vel, aux_x, aux_y = colisao_simpletica_robusta(
                estado.curva_parametrica,
                t_hit,
                hit_pos,
                estado.t,       # t anterior (ainda não atualizado)
                estado.vel,
            )
            estado.vel = nova_vel
            estado.trajetoria_aux_x = aux_x
            estado.trajetoria_aux_y = aux_y
            trajeto_aux.set_data(aux_x, aux_y)

        # pequeno empurrão para não “grudar” na fronteira
        estado.pos = hit_pos.copy() + 1e-8 * estado.vel
        estado.t = t_hit

        tg = estado.curva_parametrica.get_tangente(estado.t)
        estado.cos_angulo = float(np.dot(estado.vel, tg))

        estado.lista_t_colisao.append(estado.t / np.pi)
        estado.lista_angulo_colisao.append(estado.cos_angulo)
        colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)

        # atualiza heatmap a cada 2 colisões (após as primeiras)
        if len(estado.lista_t_colisao) % 2 == 0 and len(estado.lista_t_colisao) > 5:
            hist, _, _ = np.histogram2d(
                estado.lista_t_colisao,
                estado.lista_angulo_colisao,
                bins=estado.heatmap_bins,
                range=[[0, 2], [-1, 1]],
            )
            log_hist = np.log1p(hist)
            estado.heatmap.set_data(log_hist.T)
            if np.max(log_hist) > 0:
                estado.heatmap.set_clim(0, np.max(log_hist) * 1.05)

        estado.traj_x.append(estado.pos[0])
        estado.traj_y.append(estado.pos[1])
        time_left -= lam

    # limita memória da trajetória desenhada
    if len(estado.traj_x) > 20000:
        estado.traj_x = estado.traj_x[-10000:]
        estado.traj_y = estado.traj_y[-10000:]

    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data(estado.traj_x, estado.traj_y)

    return (
        curva_plot, bolinha, trajeto, trajeto_aux,
        normal_linha, vel_linha, tangente_linha,
        colisao_plot, texto_info,
    )


# =====================================================================
# EXECUÇÃO
# =====================================================================
if __name__ == "__main__":
    # Cria o estado global e desenha a tela inicial.
    # Quando: execução do script (python arquivo.py).
    estado = EstadoBilhar()
    preparar_simulacao(None)
    plt.show()