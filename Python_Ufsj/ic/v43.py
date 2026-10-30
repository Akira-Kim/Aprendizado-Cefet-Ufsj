import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox, RadioButtons
from matplotlib import gridspec, patches
from scipy.optimize import minimize_scalar


# === Sistema de Funções Paramétricas ===
erro = 1e-2
num_pontos_da_curva = 10000

class CurvaParametrica:
    def __init__(self):
        self.curvas = {
            'Círculo': self.circulo,	
            'Elipse': self.elipse            
        }
        self.parametro_a = 1
        self.parametro_b = 1
        self.curva_atual = 'Círculo'
       
    def __call__(self, t):
        try:
            return self.curvas[self.curva_atual](t)
        except:
            return np.array([0, 0, 0])    
        
    def circulo(self,t):
        a, b = 1, 1
        return np.array([t, a * np.cos(t), b * np.sin(t)])

    def elipse(self, t):
        a, b = self.parametro_a, self.parametro_b
        return np.array([t, a * np.cos(t), b * np.sin(t)])

    def colisao(self, pos):
        if self.curva_atual == 'Círculo' and np.abs(pos[0]**2+pos[1]**2 - 1)<erro: return True
        if self.curva_atual == 'Elipse' and np.abs((pos[0]**2)/(self.parametro_a**2)+(pos[1]**2)/(self.parametro_b**2) - 1)<erro: return True
        return False
    
# === Estado da Simulação ===
class EstadoBilhar:
    def __init__(self):
        self.pausado = True
        self.novadirecao = True
        self.primeiro_inicio = True        
        self.modo_bilhar = 'Elástico'  # 'Elástico' ou 'Simpletico'
        self.pos = np.array([1.0, 0])
        self.t = 0 
        self.vel = np.array([-1, 1]) *(1/math.sqrt(2))
        self.angulo_vel = 0.25*np.pi
        self.velocidade_simulacao = 1
        self.curva_parametrica = CurvaParametrica()
        self.curve_points = None #pontos
        self.trajetoria = [self.pos]
        self.trajetoria_aux = [self.pos]
    
        self.cos_angulo = 1 # Armazena os parâmetros cos angulo da última colisão
        self.lista_t_colisao = []# [self.t]  # lista com os parâmetros t das colisão
        self.lista_angulo_colisao = [] #[self.cos_angulo] #lista com cosenos do angulos das colisões
        self.erro = 1e-5        
        self.reset_all = False
        self.t_proximo = None

    def reset(self):
        self.pausado = True
        self.novadirecao = True
        self.primeiro_inicio = True
        self.pos = np.array([1.0, 0])
        self.t = 0 
        self.vel = np.array([-1, 1]) *(1/math.sqrt(2))
        self.angulo_vel = 0.25*np.pi
        self.velocidade_simulacao = 1
        self.curva_parametrica = CurvaParametrica()
        self.curve_points = None #pontos
        self.trajetoria = [self.pos]
        self.trajetoria_aux = [self.pos]
        self.cos_angulo = 1 # Armazena os parâmetros cos angulo da última colisão
        self.erro = 1e-5     
        self.t_proximo = None   
    

# === Funções de Utilidade ===

def derivada(t):
    h=1e-5
    """Calcula a derivada numericamente com tratamento de contorno"""
    t1 = t - h #if t > h else t + 2*np.pi - h
    t2 = t + h #if t < 2*np.pi - h else t - 2*np.pi + h
    p1 = estado.curva_parametrica(t1)
    p2 = estado.curva_parametrica(t2)
    p1 = np.array([p1[1], p1[2]])
    p2 = np.array([p2[1], p2[2]])
    return (p2 - p1) / (2*h)

def tangente(t):
    """Calcula o vetor tangente unitário"""
    deriv = derivada(t)
    norm = np.linalg.norm(deriv)
    return deriv/norm

def normal(t): #pra dentro
    tng = tangente(t)
    return np.array([-tng[1], tng[0]])

def refletir_vetor(v, normal):
    """Reflete o vetor v em relação à normal"""
    return v - 2 * np.dot(v, normal) * normal


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
ax.set_title("Espaço de Configuração", pad=20, fontsize=14, color='#333333')

ax2 = fig.add_subplot(gs_graficos[1])
ax2.set_facecolor('#fafafa')
ax2.grid(True, alpha=0.3)
ax2.set_title("Espaço de Fase", pad=20, fontsize=14)
ax2.set_xlabel("Parâmetro t (0 a 2)x π", fontsize=10)
ax2.set_ylabel("Coseno Ângulo de Colisão com a Tangente (-1 a 1)", fontsize=10)
ax2.set_xlim(0, 2)
ax2.set_ylim(-1, 1)

# Área para controles 
ax_controles = fig.add_subplot(gs_main[1])
ax_controles.set_axis_off()
ax_controles.set_visible(True)

# === Elementos Visuais ===
curva_plot, = ax.plot([], [], 'k-', linewidth=2, alpha=0.8)
bolinha, = ax.plot([], [], 'ro', markersize=5, zorder=3)
trajeto, = ax.plot([], [], 'r-', linewidth=1, alpha=0.7)
trajeto_aux, = ax.plot([], [], 'g:', linewidth=1, alpha=0.7)
normal_linha, = ax.plot([], [], 'b--', linewidth=1.5, alpha=0.7)
vel_linha, = ax.plot([], [], 'g-', linewidth=1.5, alpha=0.7)
tangente_linha, = ax.plot([], [], 'm-', linewidth=1.5, alpha=0.7)  # Para bilhar simplético
proxima_linha, = ax.plot([], [], 'c-', linewidth=1.5, alpha=0.7)    # Para bilhar simplético
colisao_plot, = ax2.plot([], [], 'ro', markersize=2, alpha=0.7)


texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.9, edgecolor='#cccccc'))


# --- Grupo 1: Rótulo para Funções
ax.add_patch(patches.Rectangle((0.05, 0.15), 0.15, 0.07, transform=fig.transFigure, facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax_radio = plt.axes([0.05, 0.07, 0.13, 0.1])
radio = RadioButtons(ax_radio, ['Círculo', 'Elipse'], active=0)
ax_radio.set_visible(True)
ax.text(0.095, 0.18, "Fronteira", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

# --- Parâmetros da curva ---
ax.add_patch(patches.Rectangle((0.25, 0.15), 0.20, 0.07, transform=fig.transFigure, facecolor='#f0f0f5', edgecolor='#cccccc', alpha=#
0.7))
ax.text(0.25, 0.18, "Parâmetros da Curva", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

ax_texto_a = plt.axes([0.24, 0.14, 0.06, 0.04])
texto_a = TextBox(ax_texto_a, 'a', initial='1.0')
ax_texto_a.set_visible(True)

ax_texto_b = plt.axes([0.24, 0.1, 0.06, 0.04])
texto_b = TextBox(ax_texto_b, 'b', initial='1.0')
ax_texto_b.set_visible(True)

# Rótulo para Modo de Bilhar
ax.add_patch(patches.Rectangle((0.35, 0.15), 0.15, 0.07, transform=fig.transFigure, facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax_radio_modo = plt.axes([0.34, 0.07, 0.13, 0.1])
radio_modo = RadioButtons(ax_radio_modo, ['Elástica', 'Simplética'], active=0)
ax_radio_modo.set_visible(True)
ax.text(0.385, 0.18, "Colisão", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

ax.text(0.65, 0.18, "Condição Inicial", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')
# Slider para posição na borda (modo borda)
ax_pos_t = plt.axes([0.6, 0.15, 0.15, 0.02])
slider_pos_t = Slider(ax_pos_t, 't (x π)', 0, 2, valinit=0, valstep=0.01)
ax_pos_t.set_visible(True)

# Slider de ângulo
ax_angulo = plt.axes([0.6, 0.11, 0.15, 0.02])
slider_angulo = Slider(ax_angulo, 'Ângulo (x π)', 0, 1, valinit=0.25, valstep=0.01)
ax_angulo.set_visible(True)

# Slider de velocidade
ax_vel = plt.axes([0.6, 0.07, 0.15, 0.02])
slider_vel = Slider(ax_vel, 'Velocidade', 1, 3.0, valinit=1.0, valstep=0.1)
ax_vel.set_visible(True)

# --- Grupo 4: Botões de Controle ---
ax.add_patch(patches.Rectangle((0.50, 0.05), 0.48, 0.09, transform=fig.transFigure, facecolor='#f0f0f5', edgecolor='#cccccc', alpha=0.7))
ax.text(0.86, 0.18, "Controles da Simulação", transform=fig.transFigure, ha='center', fontsize=9, color='#333333')

ax_botao_start_pause = plt.axes([0.82, 0.13, 0.08, 0.04])
botao_start_pause = Button(ax_botao_start_pause, 'Iniciar', color='#ddffdd')
ax_botao_start_pause.set_visible(True)

ax_botao_reset = plt.axes([0.82, 0.08, 0.08, 0.04])
botao_reset = Button(ax_botao_reset, 'Reset', color='#ffdddd')
ax_botao_reset.set_visible(True)

ax_botao_info = plt.axes([0.82, 0.03, 0.08, 0.04])
botao_info = Button(ax_botao_info, 'Info', color='#ddddff')
ax_botao_info.set_visible(True)


def preparar_simulacao(event):

    normal_linha.set_data([], [])
    vel_linha.set_data([], [])
    tangente_linha.set_data([], [])
    texto_info.set_text('Pronto para iniciar')
    bolinha = np.array( [estado.curva_parametrica(0)[1], estado.curva_parametrica(0)[2]])
    trajeto.set_data([], [])
    colisao_plot.set_data([], [])
    atualizar_curva_e_bolinha()
    

def reset_simulacao(event):
    
    # Reset dos controles
    slider_pos_t.set_val(0)
    slider_angulo.set_val(0.25)
    
    slider_vel.set_val(1.0)
    texto_a.set_val('1.0')
    texto_b.set_val('1.0')
    botao_start_pause.label.set_text('Iniciar')
    texto_info.set_text('Pronto para iniciar')
    estado.reset()
    bolinha = np.array( [estado.curva_parametrica(0)[1], estado.curva_parametrica(0)[2]])
    trajeto.set_data([], [])
    trajeto_aux.set_data([], [])
        
    if (estado.reset_all):
        botao_reset.label.set_text("Reset")  
        estado.lista_t_colisao = []# [self.t]  # lista com os parâmetros t das colisão
        estado.lista_angulo_colisao = [] #[self.cos_angulo] #lista com cosenos do angulos das colisões
        colisao_plot.set_data([], []) 
        estado.reset_all = False        
    else: 
        estado.reset_all = True
        botao_reset.label.set_text("Reset all")      
       
    atualizar_curva_e_bolinha()



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
    t = np.linspace(0, 2*np.pi, num_pontos_da_curva)
    pontos = np.array([estado.curva_parametrica(ti) for ti in t]).T
    curva_plot.set_data(pontos[1], pontos[2])
    estado.curve_points = pontos
    ax.set_xlim(np.min(pontos[1])-0.5, np.max(pontos[1])+0.5)
    ax.set_ylim(np.min(pontos[2])-0.5, np.max(pontos[2])+0.5)
    texto_info.set_text(f"Curva: {estado.curva_parametrica.curva_atual}")
    estado.pos = np.array([estado.curva_parametrica(estado.t)[1],estado.curva_parametrica(estado.t)[2]])
    tng = tangente(estado.t) 
    tangente_linha.set_data([[estado.pos[0],estado.pos[0]+tng[0]], [estado.pos[1],estado.pos[1]+tng[1]]])
    estado.vel = np.array([tng[0]*np.cos(estado.angulo_vel)-tng[1]*np.sin(estado.angulo_vel),
              tng[1]*np.cos(estado.angulo_vel)+tng[0]*np.sin(estado.angulo_vel) ]) 
    vel_linha.set_data([[estado.pos[0],estado.pos[0]+estado.vel[0]], [estado.pos[1],estado.pos[1]+estado.vel[1]]]) 
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    estado.trajetoria = [estado.pos.copy()]

    estado.cos_angulo = float(np.dot(tangente(estado.t), estado.vel)) 
    colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)
        
    fig.canvas.draw_idle()

def continuar_ou_pausar_simulacao(event):

    if estado.pausado:
        estado.pausado = False
        texto_info.set_text('Simulação em andamento')
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
     
    # Criar a animação somente agora (após tornar os eixos visíveis)
    ani = FuncAnimation(
        fig, 
        update, 
        frames=None, 
        init_func=init, 
        blit=False, #True, 
        interval=1, 
        cache_frame_data=False
    )
 
    fig.canvas.draw()

def mostrar_info(event):
    texto_info.set_text(
        "Trabalho de iniciação científica de Akira Kim com o título\n"
        "Simulação de Bilhares e orientado por Ivana Latosinski."
    )

radio.on_clicked(atualizar_curva)
radio_modo.on_clicked(atualizar_modo)

botao_reset.on_clicked(reset_simulacao)
botao_start_pause.on_clicked(continuar_ou_pausar_simulacao)
botao_info.on_clicked(mostrar_info)

def update_posicao_t(val):
    if estado.primeiro_inicio:
         estado.t = val*np.pi
         estado.pos = np.array([estado.curva_parametrica(estado.t)[1],estado.curva_parametrica(estado.t)[2]])
         atualizar_curva_e_bolinha()
    
def update_angulo(val):
    if estado.primeiro_inicio:
       estado.angulo_vel = val*np.pi
       atualizar_curva_e_bolinha()

def update_vel(val):
    if estado.primeiro_inicio:
        estado.velocidade_simulacao = val
        #atualizar_curva_e_bolinha()

slider_pos_t.on_changed(update_posicao_t)
slider_angulo.on_changed(update_angulo)
slider_vel.on_changed(update_vel)

def init():
    
    return (curva_plot, bolinha, trajeto, normal_linha, vel_linha, 
            tangente_linha, proxima_linha, colisao_plot, 
            texto_info)


def update(frame):
    """Função de atualização"""
    
    if estado.pausado:
        return (curva_plot, bolinha, trajeto, normal_linha, vel_linha, 
                tangente_linha, proxima_linha, colisao_plot, 
                texto_info)
    
    
    dt = 0.015 * estado.velocidade_simulacao
        
    if estado.novadirecao : 
        estado.lista_t_colisao.append(estado.t/np.pi)
        estado.lista_angulo_colisao.append(estado.cos_angulo)
        colisao_plot.set_data(estado.lista_t_colisao, estado.lista_angulo_colisao)
        nova_pos = estado.pos + 0.1 * estado.vel * dt #faz a bolinha se afastar da fronteira mais rapidamente
        estado.novadirecao = False
    
    parametro = estado.curve_points[0,:]
    x = estado.curve_points[1,:]
    y = estado.curve_points[2,:]
    
    estado.pos = estado.pos + estado.vel * dt
    estado.trajetoria.append(estado.pos.copy())
    
    if estado.curva_parametrica.colisao(estado.pos) : 
        if estado.modo_bilhar == 'Elástico':
            dist2 = (x - estado.pos[0])**2 + (y - estado.pos[1])**2
            i_min = np.argmin(dist2)
            t_min = parametro[i_min]
            estado.vel = refletir_vetor( estado.vel, normal(t_min))
            estado.t = float(t_min)
            estado.cos_angulo = float(np.dot(tangente(estado.t), estado.vel)) 
            estado.novadirecao = True

        else: #simplético
         
            dist2 = (x - estado.pos[0])**2 + (y - estado.pos[1])**2
            i_min = np.argmin(dist2)
            t_min = parametro[i_min]
            
            vel_aux = tangente(t_min)
            pos_aux = np.array([estado.curva_parametrica(estado.t)[1],estado.curva_parametrica(estado.t)[2]]) + 1 * vel_aux * dt    
            
            estado.t = t_min
            
            estado.trajetoria_aux = [pos_aux]
            while not estado.curva_parametrica.colisao(pos_aux): 
                pos_aux = pos_aux + vel_aux * dt
                estado.trajetoria_aux.append(pos_aux)
                #bolinha.set_data([pos_aux[0]], [pos_aux[1]])
                trajeto_aux.set_data([p[0] for p in estado.trajetoria_aux], [p[1] for p in estado.trajetoria_aux])
     
            dist2 = (x - pos_aux[0])**2 + (y - pos_aux[1])**2
            i_min = np.argmin(dist2)
            t_min = parametro[i_min]
            
            estado.t_proximo = t_min
            estado.pos = np.array([estado.curva_parametrica(estado.t)[1],estado.curva_parametrica(estado.t)[2]])
            vetor_aux = (np.array([estado.curva_parametrica(t_min)[1],estado.curva_parametrica(t_min)[2]])-estado.pos)
            estado.vel = vetor_aux / np.linalg.norm(vetor_aux)
            estado.cos_angulo = float(np.dot(estado.vel, tangente(estado.t))) 
            estado.novadirecao = True

     
        #testar o simpletico maximizando a area!
  
    # Limitar o tamanho da trajetória
    
    #if len(estado.trajetoria) > 10000:
    #    estado.trajetoria.pop(0)
    
    # Atualiza gráficos
    bolinha.set_data([estado.pos[0]], [estado.pos[1]])
    trajeto.set_data([p[0] for p in estado.trajetoria], [p[1] for p in estado.trajetoria])

    return (curva_plot, bolinha, trajeto, normal_linha, vel_linha, 
            tangente_linha, proxima_linha, colisao_plot, 
            texto_info)


# === Execução Principal ===
if __name__ == "__main__":

    # Inicialização
    estado = EstadoBilhar()
    preparar_simulacao(None)
    
    plt.show()
    