"""
Simulador Interativo de Bilhares Simpléticos (versão do artigo)
================================================================
Fronteiras: Círculo e Elipse (suaves).
Modos de colisão: Elástico e Simplético (sem fallback elástico).

Extras:
- Passo a passo (avança 1 colisão e pausa)
- Prever N ricochetes (desenha trajetória futura sem alterar o estado)

Referência: Albers & Tabachnikov, Introducing symplectic billiards (2018).
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
    Fronteira da mesa de bilhar como curva paramétrica fechada e suave.

    Curvas: Círculo e Elipse.
    Usada em todo cálculo geométrico (ponto, tangente, normal, interseção).
    """

    def __init__(self):
        """
        Inicializa a curva no círculo unitário (a = b = 1).

        Quando: criação do estado da simulação ou reset.
        """
        self.curvas = {
            'Círculo': self.circulo,
            'Elipse': self.elipse,
        }
        self.parametro_a = 1.0
        self.parametro_b = 1.0
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
        Parametrização do círculo unitário: (cos t, sin t).

        Quando: curva_atual == 'Círculo'.
        """
        return np.array([t, np.cos(t), np.sin(t)])

    def elipse(self, t):
        """
        Parametrização da elipse: (a cos t, b sin t).

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
        return [(-B + sd) / (2 * A), (-B - sd) / (2 * A)]

    def get_tangente(self, t):
        """
        Tangente unitária T(t) no ponto r(t).

        Quando:
        - montar a condição inicial (direção da velocidade);
        - construir a colisão simplética;
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
        n = np.array([-tng[1], tng[0]])
        p = self(t)
        pos = np.array([p[1], p[2]])
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
        Define a condição inicial padrão:
        partícula em (1,0) no círculo, modo Elástico, simulação pausada.

        Quando: arranque do programa.
        """
        self.pausado = True
        self.primeiro_inicio = True
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
        self.trajetoria_aux_x = []
        self.trajetoria_aux_y = []

        self.lista_t_colisao = []
        self.lista_angulo_colisao = []
        self.cos_angulo = 0.0
        self.reset_all = False

        self.heatmap = None
        self.heatmap_bins = 120

        self.prev_x = []
        self.prev_y = []

    def reset(self):
        """
        Restaura o estado inicial e limpa trajetória, colisões,
        heatmap e previsão.

        Quando: clique em Reset.
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

        self.prev_x = []
        self.prev_y = []

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
      a1 = r(t_anterior)
      a2 = hit_pos
      T  = tangente em a2
      a3 = outra interseção da reta (a1 + λ T) com a fronteira
      nova velocidade = direção (a3 - a2)

    Estratégia:
      1) interseção analítica (equação quadrática);
      2) se falhar, resolve f(s) = <r(s)-a1, N(a2)> = 0;
      3) se ainda falhar, mantém a velocidade (não troca de lei).

    Quando: modo_bilhar == 'Simplético', a cada colisão.
    """
    p_ant = curva(t_anterior)
    a1 = np.array([p_ant[1], p_ant[2]], dtype=float)

    T = curva.get_tangente(t_hit)
    N = curva.get_normal(t_hit)

    # Tentativa 1: interseção analítica
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

    # Tentativa 2: raiz de f(s) = 0
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

    # Falha numérica: mantém velocidade (não usa elástico)
    norma = np.linalg.norm(vel)
    if norma > 1e-12:
        vel = vel / norma
    return vel, [], []


def aplicar_colisao(modo, curva, t_hit, hit_pos, t_anterior, vel):
    """
    Despacha para a lei de colisão correta (Elástico ou Simplético).

    Retorna: (nova_vel, aux_x, aux_y).

    Quando: animação contínua, passo a passo e previsão de N ricochetes.
    """
    if modo == 'Elástico':
        n = curva.get_normal(t_hit)
        nova_vel = refletir_vetor(vel, n)
        norma = np.linalg.norm(nova_vel)
        if norma > 1e-12:
            nova_vel = nova_vel / norma
        return nova_vel, [], []
    return colisao_simpletica_robusta(curva, t_hit, hit_pos, t_anterior, vel)


def simular_uma_colisao(pos, vel, t, curva, modo):
    """
    Avança o estado até a PRÓXIMA colisão (cálculo puro, sem desenhar).

    Retorna: dicionário com pos, vel, t, hit_pos, cos_angulo, aux_x, aux_y, lam;
             ou None se não houver colisão.

    Quando: base do passo a passo e da previsão de trajetória.
    """
    lambdas = curva.intersect_line(pos, vel)
    positive = [lam for lam in lambdas if lam > 1e-8]
    if not positive:
        return None

    lam = min(positive)
    hit_pos = pos + lam * vel
    t_hit = curva.get_t_from_pos(hit_pos)
    nova_vel, aux_x, aux_y = aplicar_colisao(modo, curva, t_hit, hit_pos, t, vel)
    nova_pos = hit_pos + 1e-8 * nova_vel
    tg = curva.get_tangente(t_hit)
    cos_ang = float(np.dot(nova_vel, tg))

    return {
        'pos': nova_pos,
        'vel': nova_vel,
        't': t_hit,
        'hit_pos': hit_pos,
        'cos_angulo': cos_ang,
        'aux_x': aux_x,
        'aux_y': aux_y,
        'lam': lam,
    }


def prever_trajetoria(pos, vel, t, curva, modo, n_ricochetes):
    """
    Simula N colisões à frente SEM alterar o estado real da simulação.

    Retorna: (xs, ys) — poligonal prevista incluindo a posição atual.

    Quando: clique em "Prever N".
    """
    xs = [float(pos[0])]
    ys = [float(pos[1])]
    p, v, tt = pos.copy(), vel.copy(), float(t)

    for _ in range(n_ricochetes):
        res = simular_uma_colisao(p, v, tt, curva, modo)
        if res is None:
            break
        xs.append(float(res['hit_pos'][0]))
        ys.append(float(res['hit_pos'][1]))
        p = res['pos']
        v = res['vel']
        tt = res['t']

    return xs, ys


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

ax = fig.add_subplot(gs_graficos[0])
ax.set_facecolor('#fafafa')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title("Espaço de Configuração", pad=20, fontsize=14)

ax2 = fig.add_subplot(gs_graficos[1])
ax2.set_facecolor('#fafafa')
ax2.grid(True, alpha=0.3)
ax2.set_title("Espaço de Fase + Mapa de Calor", pad=20, fontsize=14)
ax2.set_xlabel("Parâmetro t (× π)")
ax2.set_ylabel("cos θ (ângulo com a tangente)")
ax2.set_xlim(0, 2)
ax2.set_ylim(-1, 1)

ax_controles = fig.add_subplot(gs_main[1])
ax_controles.set_axis_off()

# Artistas gráficos
curva_plot, = ax.plot([], [], 'k-', linewidth=2, alpha=0.8)
bolinha, = ax.plot([], [], 'ro', markersize=6, zorder=3)
trajeto, = ax.plot([], [], 'r-', linewidth=1.2, alpha=0.75)
trajeto_aux, = ax.plot([], [], 'c--', linewidth=1.8, alpha=0.85)
trajeto_prev, = ax.plot([], [], 'g--', linewidth=1.6, alpha=0.8, zorder=2)
vel_linha, = ax.plot([], [], 'g-', linewidth=1.5, alpha=0.8)
tangente_linha, = ax.plot([], [], 'm-', linewidth=1.5, alpha=0.6)
colisao_plot, = ax2.plot([], [], 'ro', markersize=3.5, alpha=0.98, zorder=10)
texto_info = ax.text(
    0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
    bbox=dict(facecolor='white', alpha=0.95, edgecolor='#cccccc'),
)

# Controles
ax_radio = plt.axes([0.05, 0.07, 0.12, 0.10])
radio = RadioButtons(ax_radio, ['Círculo', 'Elipse'], active=0)
ax.text(0.11, 0.18, "Fronteira", transform=fig.transFigure, ha='center', fontsize=9)

ax_texto_a = plt.axes([0.20, 0.14, 0.06, 0.04])
texto_a = TextBox(ax_texto_a, 'a', initial='1.0')
ax_texto_b = plt.axes([0.20, 0.09, 0.06, 0.04])
texto_b = TextBox(ax_texto_b, 'b', initial='1.0')
ax.text(0.23, 0.18, "Parâmetros", transform=fig.transFigure, ha='center', fontsize=9)

ax_radio_modo = plt.axes([0.30, 0.07, 0.12, 0.10])
radio_modo = RadioButtons(ax_radio_modo, ['Elástico', 'Simplético'], active=0)
ax.text(0.36, 0.18, "Colisão", transform=fig.transFigure, ha='center', fontsize=9)

ax_pos_t = plt.axes([0.48, 0.15, 0.14, 0.025])
slider_pos_t = Slider(ax_pos_t, 't (×π)', 0, 2, valinit=0, valstep=0.005)
ax_angulo = plt.axes([0.48, 0.11, 0.14, 0.025])
slider_angulo = Slider(ax_angulo, 'Ângulo (×π)', 0, 1, valinit=0.25, valstep=0.01)
ax_vel = plt.axes([0.48, 0.07, 0.14, 0.025])
slider_vel = Slider(ax_vel, 'Velocidade', 0.5, 4.0, valinit=1.0, valstep=0.1)
ax.text(0.55, 0.19, "Condição Inicial", transform=fig.transFigure, ha='center', fontsize=9)

ax_start = plt.axes([0.68, 0.14, 0.08, 0.035])
botao_start = Button(ax_start, 'Iniciar', color='#ddffdd')
ax_step = plt.axes([0.68, 0.10, 0.08, 0.035])
botao_step = Button(ax_step, 'Passo a passo', color='#cce5ff')
ax_reset = plt.axes([0.68, 0.06, 0.08, 0.035])
botao_reset = Button(ax_reset, 'Reset', color='#ffdddd')

ax_n_prev = plt.axes([0.80, 0.14, 0.06, 0.035])
texto_n_prev = TextBox(ax_n_prev, 'N', initial='10')
ax_prever = plt.axes([0.87, 0.14, 0.08, 0.035])
botao_prever = Button(ax_prever, 'Prever N', color='#e0ffe0')
ax_limpar_prev = plt.axes([0.87, 0.10, 0.08, 0.035])
botao_limpar_prev = Button(ax_limpar_prev, 'Limpar prev.', color='#f0f0f0')
ax_info = plt.axes([0.87, 0.06, 0.08, 0.035])
botao_info = Button(ax_info, 'Info', color='#ddddff')
ax.text(0.87, 0.19, "Previsão / Ajuda", transform=fig.transFigure, ha='center', fontsize=9)


# =====================================================================
# CALLBACKS DA INTERFACE
# =====================================================================

def preparar_simulacao(event):
    """
    Prepara o desenho inicial e cria o heatmap (uma vez).

    Quando: arranque do programa.
    """
    trajeto_aux.set_data([], [])
    trajeto_prev.set_data([], [])
    texto_info.set_text('Pronto para iniciar')
    atualizar_curva_e_bolinha()

    if estado.heatmap is None:
        estado.heatmap = ax2.imshow(
            np.zeros((estado.heatmap_bins, estado.heatmap_bins)),
            origin='lower', extent=[0, 2, -1, 1],
            cmap='inferno', aspect='auto', alpha=0.92,
            interpolation='nearest',
        )
        colisao_plot.set_zorder(10)
        plt.colorbar(
            estado.heatmap, ax=ax2, pad=0.02,
            label='log(1 + colisões)',
        )


def atualizar_curva_e_bolinha():
    """
    Redesenha a mesa, a partícula, tangente e velocidade inicial.

    Quando:
    - mudança de curva / parâmetros / sliders (antes de iniciar);
    - após Reset.
    """
    estado.curva_parametrica.parametro_a = float(texto_a.text)
    estado.curva_parametrica.parametro_b = float(texto_b.text)

    tvals = np.linspace(0, 2 * np.pi, 10000)
    pts = np.array([estado.curva_parametrica(ti) for ti in tvals]).T
    curva_plot.set_data(pts[1], pts[2])
    ax.set_xlim(np.min(pts[1]) - 0.6, np.max(pts[1]) + 0.6)
    ax.set_ylim(np.min(pts[2]) - 0.6, np.max(pts[2]) + 0.6)

    estado.pos = np.array([
        estado.curva_parametrica(estado.t)[1],
        estado.curva_parametrica(estado.t)[2],
    ])

    tng = estado.curva_parametrica.get_tangente(estado.t)
    tangente_linha.set_data(
        [estado.pos[0], estado.pos[0] + tng[0]],
        [estado.pos[1], estado.pos[1] + tng[1]],
    )

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
    estado.traj_x = [float(estado.pos[0])]
    estado.traj_y = [float(estado.pos[1])]
    trajeto.set_data(estado.traj_x, estado.traj_y)
    trajeto_aux.set_data([], [])
    colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)

    texto_info.set_text(
        f"Curva: {estado.curva_parametrica.curva_atual} | Modo: {estado.modo_bilhar}"
    )
    fig.canvas.draw_idle()


def on_curva(label):
    """
    Troca a fronteira (Círculo / Elipse).

    Quando: clique no radio de fronteira, só antes do primeiro Iniciar.
    """
    if estado.primeiro_inicio:
        estado.curva_parametrica.curva_atual = label
        atualizar_curva_e_bolinha()


def on_modo(label):
    """
    Troca o modo de colisão (Elástico / Simplético).

    Quando: clique no radio de colisão, só antes do primeiro Iniciar.
    """
    if estado.primeiro_inicio:
        estado.modo_bilhar = label
        atualizar_curva_e_bolinha()


def on_parametros(val=None):
    """
    Lê a e b dos TextBox e redesenha a curva.

    Quando: usuário confirma a ou b (Enter), só em primeiro_inicio.
    """
    if estado.primeiro_inicio:
        atualizar_curva_e_bolinha()


def on_t(val):
    """
    Atualiza o parâmetro t da condição inicial.

    Quando: movimento do slider t, só em primeiro_inicio.
    """
    if estado.primeiro_inicio:
        estado.t = val * np.pi
        atualizar_curva_e_bolinha()


def on_angulo(val):
    """
    Atualiza o ângulo da velocidade inicial (em relação à tangente).

    Quando: movimento do slider de ângulo, só em primeiro_inicio.
    """
    if estado.primeiro_inicio:
        estado.angulo_vel = val * np.pi
        atualizar_curva_e_bolinha()


def on_vel(val):
    """
    Atualiza o fator de velocidade da animação.

    Quando: movimento do slider de velocidade, só em primeiro_inicio.
    """
    if estado.primeiro_inicio:
        estado.velocidade_simulacao = val


def on_start(event):
    """
    Alterna entre animação contínua rodando e pausada.

    Quando: clique em Iniciar / Pausar / Continuar.
    """
    if estado.pausado:
        estado.pausado = False
        estado.primeiro_inicio = False
        botao_start.label.set_text('Pausar')
        texto_info.set_text('Simulação em andamento...')
        iniciar_animacao()
    else:
        estado.pausado = True
        botao_start.label.set_text('Continuar')
        texto_info.set_text('Simulação pausada')
    fig.canvas.draw_idle()


def on_step(event):
    """
    Passo a passo: avança exatamente 1 colisão e permanece pausado.

    Quando: clique em "Passo a passo".
    """
    estado.pausado = True
    estado.primeiro_inicio = False
    botao_start.label.set_text('Continuar')

    res = simular_uma_colisao(
        estado.pos, estado.vel, estado.t,
        estado.curva_parametrica, estado.modo_bilhar,
    )
    if res is None:
        texto_info.set_text('Passo a passo: nenhuma colisão encontrada.')
        fig.canvas.draw_idle()
        return

    estado.traj_x.append(float(res['hit_pos'][0]))
    estado.traj_y.append(float(res['hit_pos'][1]))
    estado.traj_x.append(float(res['pos'][0]))
    estado.traj_y.append(float(res['pos'][1]))

    estado.pos = res['pos']
    estado.vel = res['vel']
    estado.t = res['t']
    estado.cos_angulo = res['cos_angulo']
    estado.trajetoria_aux_x = res['aux_x']
    estado.trajetoria_aux_y = res['aux_y']

    estado.lista_t_colisao.append(estado.t / np.pi)
    estado.lista_angulo_colisao.append(estado.cos_angulo)

    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data(estado.traj_x, estado.traj_y)
    trajeto_aux.set_data(estado.trajetoria_aux_x, estado.trajetoria_aux_y)
    colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)
    _atualizar_heatmap()

    texto_info.set_text(
        f"Passo a passo | Colisões: {len(estado.lista_t_colisao)} | "
        f"t/π={estado.t / np.pi:.3f} | cosθ={estado.cos_angulo:.3f}"
    )
    fig.canvas.draw_idle()


def on_prever(event):
    """
    Prever N ricochetes a partir do estado atual, sem alterar a simulação.

    Quando: clique em "Prever N".
    """
    try:
        n = int(float(texto_n_prev.text))
        n = max(1, min(n, 500))
    except Exception:
        texto_info.set_text('N inválido. Use um inteiro (ex.: 10).')
        fig.canvas.draw_idle()
        return

    xs, ys = prever_trajetoria(
        estado.pos, estado.vel, estado.t,
        estado.curva_parametrica, estado.modo_bilhar, n,
    )
    estado.prev_x, estado.prev_y = xs, ys
    trajeto_prev.set_data(xs, ys)
    texto_info.set_text(
        f'Previsão: {len(xs) - 1} ricochetes desenhados (verde tracejado).'
    )
    fig.canvas.draw_idle()


def on_limpar_prev(event):
    """
    Apaga apenas a trajetória prevista (verde).

    Quando: clique em "Limpar prev.".
    """
    estado.prev_x, estado.prev_y = [], []
    trajeto_prev.set_data([], [])
    texto_info.set_text('Previsão limpa.')
    fig.canvas.draw_idle()


def on_reset(event):
    """
    Reinicia controles e estado físico.

    Quando: clique em Reset.
    """
    slider_pos_t.set_val(0)
    slider_angulo.set_val(0.25)
    slider_vel.set_val(1.0)
    texto_a.set_val('1.0')
    texto_b.set_val('1.0')
    texto_n_prev.set_val('10')
    botao_start.label.set_text('Iniciar')
    estado.reset()
    trajeto_prev.set_data([], [])
    atualizar_curva_e_bolinha()
    texto_info.set_text('Pronto para iniciar')
    fig.canvas.draw_idle()


def on_info(event):
    """
    Mostra texto de ajuda na área de informação.

    Quando: clique em Info.
    """
    texto_info.set_text(
        "• Iniciar/Pausar: animação contínua\n"
        "• Passo a passo: avança 1 colisão e para\n"
        "• Prever N: desenha N ricochetes futuros (verde) sem alterar o estado\n"
        "• Simplético sem fallback elástico | Círculo e Elipse"
    )
    fig.canvas.draw_idle()


def _atualizar_heatmap():
    """
    Recalcula o histograma 2D das colisões e atualiza o mapa de calor.

    Quando: após novas colisões (passo a passo ou animação).
    """
    if estado.heatmap is None or len(estado.lista_t_colisao) <= 5:
        return
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


def iniciar_animacao():
    """
    Cria o FuncAnimation que chama update a cada frame.

    Quando: clique em Iniciar / Continuar.
    """
    global ani
    ani = FuncAnimation(
        fig, update, frames=None, init_func=init,
        blit=False, interval=10, cache_frame_data=False,
    )
    fig.canvas.draw()


def init():
    """
    Função de inicialização exigida pelo FuncAnimation.

    Quando: criação da animação.
    """
    return (
        curva_plot, bolinha, trajeto, trajeto_aux, trajeto_prev,
        vel_linha, tangente_linha, colisao_plot, texto_info,
    )


def update(frame):
    """
    Núcleo da simulação contínua: avança o tempo e trata colisões.

    Algoritmo:
      1. Avança no máximo dt = 0.012 * velocidade_simulacao.
      2. Calcula interseções da trajetória retilínea com a fronteira.
      3. Se houver colisão neste intervalo, aplica a lei escolhida.
      4. Atualiza posição, listas de colisão, heatmap e desenho.

    Quando: cada frame do FuncAnimation (enquanto não pausado).
    """
    if estado.pausado:
        return (
            curva_plot, bolinha, trajeto, trajeto_aux, trajeto_prev,
            vel_linha, tangente_linha, colisao_plot, texto_info,
        )

    dt = 0.012 * estado.velocidade_simulacao
    time_left = dt

    while time_left > 1e-8:
        lambdas = estado.curva_parametrica.intersect_line(estado.pos, estado.vel)
        positive = [lam for lam in lambdas if lam > 1e-8]

        if not positive:
            estado.pos = estado.pos + estado.vel * time_left
            estado.traj_x.append(float(estado.pos[0]))
            estado.traj_y.append(float(estado.pos[1]))
            break

        lam = min(positive)

        if lam >= time_left:
            estado.pos = estado.pos + estado.vel * time_left
            estado.traj_x.append(float(estado.pos[0]))
            estado.traj_y.append(float(estado.pos[1]))
            break

        hit_pos = estado.pos + lam * estado.vel
        estado.traj_x.append(float(hit_pos[0]))
        estado.traj_y.append(float(hit_pos[1]))
        t_hit = estado.curva_parametrica.get_t_from_pos(hit_pos)

        nova_vel, aux_x, aux_y = aplicar_colisao(
            estado.modo_bilhar,
            estado.curva_parametrica,
            t_hit,
            hit_pos,
            estado.t,
            estado.vel,
        )
        estado.vel = nova_vel
        estado.trajetoria_aux_x = aux_x
        estado.trajetoria_aux_y = aux_y
        trajeto_aux.set_data(aux_x, aux_y)

        estado.pos = hit_pos + 1e-8 * estado.vel
        estado.t = t_hit
        tg = estado.curva_parametrica.get_tangente(estado.t)
        estado.cos_angulo = float(np.dot(estado.vel, tg))

        estado.lista_t_colisao.append(estado.t / np.pi)
        estado.lista_angulo_colisao.append(estado.cos_angulo)
        colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)

        if len(estado.lista_t_colisao) % 2 == 0:
            _atualizar_heatmap()

        estado.traj_x.append(float(estado.pos[0]))
        estado.traj_y.append(float(estado.pos[1]))
        time_left -= lam

    if len(estado.traj_x) > 20000:
        estado.traj_x = estado.traj_x[-10000:]
        estado.traj_y = estado.traj_y[-10000:]

    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data(estado.traj_x, estado.traj_y)

    return (
        curva_plot, bolinha, trajeto, trajeto_aux, trajeto_prev,
        vel_linha, tangente_linha, colisao_plot, texto_info,
    )


# Ligações dos widgets
radio.on_clicked(on_curva)
radio_modo.on_clicked(on_modo)
texto_a.on_submit(on_parametros)
texto_b.on_submit(on_parametros)
slider_pos_t.on_changed(on_t)
slider_angulo.on_changed(on_angulo)
slider_vel.on_changed(on_vel)
botao_start.on_clicked(on_start)
botao_step.on_clicked(on_step)
botao_prever.on_clicked(on_prever)
botao_limpar_prev.on_clicked(on_limpar_prev)
botao_reset.on_clicked(on_reset)
botao_info.on_clicked(on_info)


# =====================================================================
# EXECUÇÃO
# =====================================================================
if __name__ == "__main__":
    # Cria o estado global e desenha a tela inicial.
    # Quando: execução do script (python arquivo.py).
    estado = EstadoBilhar()
    preparar_simulacao(None)
    plt.show()