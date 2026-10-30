import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox, RadioButtons
from matplotlib import gridspec, patches

# === Sistema de Funções Paramétricas ===
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

    def intersect_line(self, point, direction):
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

        sd = np.sqrt(disc)
        l1 = (-B + sd) / (2 * A)
        l2 = (-B - sd) / (2 * A)
        return [l1, l2]

    def get_tangente(self, t):
        if self.curva_atual == 'Círculo':
            return np.array([-np.sin(t), np.cos(t)])
        else:
            a, b = self.parametro_a, self.parametro_b
            d = np.array([-a * np.sin(t), b * np.cos(t)])
            norm = np.linalg.norm(d)
            return d / norm if norm > 1e-12 else np.array([1.0, 0.0])

    def get_normal(self, t):
        tng = self.get_tangente(t)
        return np.array([-tng[1], tng[0]])

    def get_t_from_pos(self, pos_plane):
        x, y = pos_plane
        if self.curva_atual == 'Círculo':
            t = np.arctan2(y, x)
        else:
            a, b = self.parametro_a, self.parametro_b
            t = np.arctan2(y / b, x / a)
        return t if t >= 0 else t + 2 * np.pi


# === Estado da Simulação ===
class EstadoBilhar:
    def __init__(self):
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

        # === MAPA DE CALOR (versão corrigida) ===
        self.heatmap = None
        self.heatmap_bins = 120   # mais bins + interpolação nearest = linha nítida e colorida

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


# === Funções de Utilidade ===
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
ax2.set_title("Espaço de Fase + Mapa de Calor (inferno)", pad=20, fontsize=14)
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
trajeto_aux, = ax.plot([], [], 'c--', linewidth=1.8, alpha=0.85)
normal_linha, = ax.plot([], [], 'b--', linewidth=1.5, alpha=0.6)
vel_linha, = ax.plot([], [], 'g-', linewidth=1.5, alpha=0.8)
tangente_linha, = ax.plot([], [], 'm-', linewidth=1.5, alpha=0.6)

colisao_plot, = ax2.plot([], [], 'ro', markersize=3.5, alpha=0.98, zorder=10)
texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                     bbox=dict(facecolor='white', alpha=0.95, edgecolor='#cccccc'))


# === Controles ===
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

    # === MAPA DE CALOR CORRIGIDO: inferno + nearest (linha nítida e colorida) ===
    if estado.heatmap is None:
        initial_hist = np.zeros((estado.heatmap_bins, estado.heatmap_bins))
        estado.heatmap = ax2.imshow(initial_hist, origin='lower',
                                    extent=[0, 2, -1, 1],
                                    cmap='inferno',               # preto → roxo → vermelho → laranja → amarelo
                                    aspect='auto',
                                    alpha=0.92,
                                    interpolation='nearest')      # ← ESSA MUDANÇA elimina o "bloco sólido"
        colisao_plot.set_zorder(10)
        estado.heatmap.set_zorder(1)
        
        plt.colorbar(estado.heatmap, ax=ax2, pad=0.02, 
                     label='log(1 + nº de colisões por bin)')


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


def atualizar_parametros(val=None):
    if estado.primeiro_inicio:
        atualizar_curva_e_bolinha()


def atualizar_curva_e_bolinha():
    estado.curva_parametrica.parametro_a = float(texto_a.text)
    estado.curva_parametrica.parametro_b = float(texto_b.text)

    t = np.linspace(0, 2 * np.pi, 10000)
    pontos = np.array([estado.curva_parametrica(ti) for ti in t]).T
    curva_plot.set_data(pontos[1], pontos[2])
    estado.curve_points = pontos

    ax.set_xlim(np.min(pontos[1]) - 0.6, np.max(pontos[1]) + 0.6)
    ax.set_ylim(np.min(pontos[2]) - 0.6, np.max(pontos[2]) + 0.6)

    estado.pos = np.array([estado.curva_parametrica(estado.t)[1],
                           estado.curva_parametrica(estado.t)[2]])

    tng = estado.curva_parametrica.get_tangente(estado.t)
    tangente_linha.set_data([estado.pos[0], estado.pos[0] + tng[0]],
                            [estado.pos[1], estado.pos[1] + tng[1]])

    estado.vel = np.array([
        tng[0] * np.cos(estado.angulo_vel) - tng[1] * np.sin(estado.angulo_vel),
        tng[1] * np.cos(estado.angulo_vel) + tng[0] * np.sin(estado.angulo_vel)
    ])
    vel_linha.set_data([estado.pos[0], estado.pos[0] + estado.vel[0]],
                       [estado.pos[1], estado.pos[1] + estado.vel[1]])

    bolinha.set_data([estado.pos[0]], [estado.pos[1]])

    estado.traj_x = [estado.pos[0]]
    estado.traj_y = [estado.pos[1]]
    estado.trajetoria_aux_x = []
    estado.trajetoria_aux_y = []
    trajeto.set_data(estado.traj_x, estado.traj_y)
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
                        blit=False, interval=10, cache_frame_data=False)
    fig.canvas.draw()


def mostrar_info(event):
    texto_info.set_text(
        "Simulação de Bilhares - Versão FINAL (corrigida)\n"
        "• Mapa de calor INFERNO (preto→roxo→vermelho→amarelo)\n"
        "• Interpolação 'nearest' (sem bloco sólido)\n"
        "• Linha nítida e colorida mesmo em órbitas periódicas\n"
        "• 120 bins + atualização otimizada"
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
texto_a.on_submit(atualizar_parametros)
texto_b.on_submit(atualizar_parametros)
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
    time_left = dt

    while time_left > 1e-8:
        lambdas = estado.curva_parametrica.intersect_line(estado.pos, estado.vel)
        positive_lams = [lam for lam in lambdas if lam > 1e-8]
        if not positive_lams:
            estado.pos += estado.vel * time_left
            estado.traj_x.append(estado.pos[0])
            estado.traj_y.append(estado.pos[1])
            break

        lam = min(positive_lams)

        if lam >= time_left:
            estado.pos += estado.vel * time_left
            estado.traj_x.append(estado.pos[0])
            estado.traj_y.append(estado.pos[1])
            break

        hit_pos = estado.pos + lam * estado.vel
        estado.traj_x.append(hit_pos[0])
        estado.traj_y.append(hit_pos[1])

        t_hit = estado.curva_parametrica.get_t_from_pos(hit_pos)

        if estado.modo_bilhar == 'Elástico':
            n = estado.curva_parametrica.get_normal(t_hit)
            estado.vel = refletir_vetor(estado.vel, n)
            estado.trajetoria_aux_x = []
            estado.trajetoria_aux_y = []
            trajeto_aux.set_data([], [])

        else:
            x_pos = np.array([estado.curva_parametrica(estado.t)[1],
                              estado.curva_parametrica(estado.t)[2]])
            T = estado.curva_parametrica.get_tangente(t_hit)
            lambdas_sym = estado.curva_parametrica.intersect_line(x_pos, T)
            other_lambda = 0.0
            for l in lambdas_sym:
                if abs(l) > 1e-6:
                    other_lambda = l
                    break
            z_pos = x_pos + other_lambda * T

            if np.linalg.norm(z_pos - hit_pos) < 1e-8:
                n = estado.curva_parametrica.get_normal(t_hit)
                estado.vel = refletir_vetor(estado.vel, n)
            else:
                estado.vel = z_pos - hit_pos
                estado.vel /= np.linalg.norm(estado.vel)

            estado.trajetoria_aux_x = [x_pos[0], z_pos[0]]
            estado.trajetoria_aux_y = [x_pos[1], z_pos[1]]
            trajeto_aux.set_data(estado.trajetoria_aux_x, estado.trajetoria_aux_y)

        estado.pos = hit_pos.copy() + 1e-8 * estado.vel
        estado.t = t_hit

        tg = estado.curva_parametrica.get_tangente(estado.t)
        estado.cos_angulo = float(np.dot(estado.vel, tg))

        estado.lista_t_colisao.append(estado.t / np.pi)
        estado.lista_angulo_colisao.append(estado.cos_angulo)
        colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)

        # === MAPA DE CALOR: atualização mais frequente + inferno ===
        if len(estado.lista_t_colisao) % 2 == 0 and len(estado.lista_t_colisao) > 5:
            hist, _, _ = np.histogram2d(
                estado.lista_t_colisao,
                estado.lista_angulo_colisao,
                bins=estado.heatmap_bins,
                range=[[0, 2], [-1, 1]]
            )
            log_hist = np.log1p(hist)
            estado.heatmap.set_data(log_hist.T)
            if np.max(log_hist) > 0:
                estado.heatmap.set_clim(0, np.max(log_hist) * 1.05)

        estado.traj_x.append(estado.pos[0])
        estado.traj_y.append(estado.pos[1])

        time_left -= lam

    if len(estado.traj_x) > 20000:
        estado.traj_x = estado.traj_x[-10000:]
        estado.traj_y = estado.traj_y[-10000:]

    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data(estado.traj_x, estado.traj_y)

    return (curva_plot, bolinha, trajeto, trajeto_aux,
            normal_linha, vel_linha, tangente_linha,
            colisao_plot, texto_info)


# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    estado = EstadoBilhar()
    preparar_simulacao(None)
    plt.show()