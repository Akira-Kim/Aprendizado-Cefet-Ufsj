import pygame
import sys
import math
import numpy as np

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bilhar com Opções de Reflexão")

# Cores
BACKGROUND = (20, 30, 50)
BALL_COLOR = (255, 215, 0)
RED = (255, 50, 50)
GREEN = (50, 200, 100)
BLUE = (70, 130, 230)
CYAN = (0, 200, 200)
MAGENTA = (200, 50, 150)
YELLOW = (255, 255, 0)
WHITE = (240, 240, 240)
GRAY = (180, 180, 180)
DARK_GRAY = (40, 40, 60)

# Parâmetros da bola
BALL_RADIUS = 10
BALL_SPEED = 4

# Classe para a bola
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade_x = BALL_SPEED
        self.velocidade_y = 0
        self.velocidade = BALL_SPEED
        self.em_movimento = True
        self.ultimo_ponto_colisao = None

    def mover(self):
        if self.em_movimento:
            self.x += self.velocidade_x
            self.y += self.velocidade_y

    def desenhar(self, tela):
        pygame.draw.circle(tela, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)
        pygame.draw.circle(tela, (200, 150, 0), (int(self.x), int(self.y)), BALL_RADIUS - 4)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.velocidade_x = BALL_SPEED
        self.velocidade_y = 0
        self.em_movimento = True
        self.ultimo_ponto_colisao = None

# Classe para o botão
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.SysFont(None, 28)
        self.current_color = color
        self.toggled = False

    def draw(self, tela):
        pygame.draw.rect(tela, self.current_color, self.rect, border_radius=12)
        pygame.draw.rect(tela, DARK_GRAY, self.rect, 3, border_radius=12)
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        tela.blit(text_surf, text_rect)

    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False

    def toggle(self):
        self.toggled = not self.toggled
        self.color = GREEN if self.toggled else BLUE
        self.hover_color = (min(self.color[0] + 30, 255), min(self.color[1] + 30, 255), min(self.color[2] + 30, 255))

# Função para calcular a reflexão simplética (baseada no artigo)
def reflexao_simpletica(x, y, circle_center, circle_radius):
    # Vetor do centro do círculo ao ponto de colisão
    cx, cy = circle_center
    vetor_centro = (y[0] - cx, y[1] - cy)
    
    # Calcular vetor tangente (perpendicular ao vetor normal)
    tang_x = -vetor_centro[1]
    tang_y = vetor_centro[0]
    magnitude = math.sqrt(tang_x**2 + tang_y**2)
    
    if magnitude > 0:
        tang_x /= magnitude
        tang_y /= magnitude
    
    # Encontrar o próximo ponto z na borda tal que (z - x) seja paralelo à tangente
    # Equação: (x + t * tangente) está no círculo
    dx, dy = tang_x, tang_y
    a = dx**2 + dy**2
    b = 2 * (dx * (x[0] - cx) + dy * (x[1] - cy))
    c = (x[0] - cx)**2 + (x[1] - cy)**2 - circle_radius**2
    
    # Resolver equação quadrática
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return x  # Fallback
    
    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
    t2 = (-b - math.sqrt(discriminant)) / (2 * a)
    
    # Dois pontos de interseção: um é x, o outro é z
    p1 = (x[0] + t1 * dx, x[1] + t1 * dy)
    p2 = (x[0] + t2 * dx, x[1] + t2 * dy)
    
    # Distância para determinar qual é o novo ponto
    dist1 = math.hypot(p1[0] - x[0], p1[1] - x[1])
    dist2 = math.hypot(p2[0] - x[0], p2[1] - x[1])
    
    # Escolher o ponto mais distante (não é o ponto de origem x)
    z = p1 if dist1 > dist2 else p2
    return z

# Função para calcular reflexão convencional
def reflexao_convencional(vel_x, vel_y, normal_x, normal_y):
    dot_product = vel_x * normal_x + vel_y * normal_y
    vel_x_ref = vel_x - 2 * dot_product * normal_x
    vel_y_ref = vel_y - 2 * dot_product * normal_y
    
    magnitude = math.sqrt(vel_x_ref**2 + vel_y_ref**2)
    if magnitude > 0:
        vel_x_ref = vel_x_ref / magnitude * BALL_SPEED
        vel_y_ref = vel_y_ref / magnitude * BALL_SPEED
    
    return vel_x_ref, vel_y_ref

# Configuração do círculo central
circle_center = (WIDTH // 2, HEIGHT // 2)
circle_radius = 200

# Criação dos objetos
bola = Ball(WIDTH // 4, HEIGHT // 2)
bilhar_simpletico_btn = Button(WIDTH - 200, 30, 180, 50, "Bilhar Simplético", BLUE, CYAN)
reset_btn = Button(WIDTH - 200, 100, 180, 50, "Reiniciar Bola", RED, MAGENTA)

# Lista para armazenar a trajetória
trajetoria = []
simulacao_ativa = False

# Função para desenhar informações na tela
def desenhar_informacoes():
    font = pygame.font.SysFont(None, 28)
    mode_text = "Modo: BILHAR SIMPLÉTICO" if bilhar_simpletico_btn.toggled else "Modo: Bilhar Convencional"
    mode_surf = font.render(mode_text, True, GREEN if bilhar_simpletico_btn.toggled else YELLOW)
    screen.blit(mode_surf, (20, 20))
    
    # Instruções
    inst_font = pygame.font.SysFont(None, 22)
    instructions = [
        "CLIQUE E ARRASTE para lançar a bola",
        "BILHAR SIMPLÉTICO: reflexão por área do triângulo",
        "BILHAR CONVENCIONAL: ângulo de incidência = reflexão"
    ]
    
    for i, text in enumerate(instructions):
        inst_surf = inst_font.render(text, True, WHITE)
        screen.blit(inst_surf, (20, HEIGHT - 100 + i * 25))

# Loop principal
clock = pygame.time.Clock()
dragging = False
start_pos = (0, 0)

while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if reset_btn.rect.collidepoint(mouse_pos):
                bola.reset(WIDTH // 4, HEIGHT // 2)
                trajetoria = []
                simulacao_ativa = False
            
            elif bilhar_simpletico_btn.rect.collidepoint(mouse_pos):
                bilhar_simpletico_btn.toggle()
            
            elif not bola.em_movimento:
                dragging = True
                start_pos = mouse_pos
        
        if event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False
            end_pos = mouse_pos
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            
            magnitude = math.sqrt(dx**2 + dy**2)
            if magnitude > 0:
                bola.velocidade_x = dx / magnitude * BALL_SPEED
                bola.velocidade_y = dy / magnitude * BALL_SPEED
            
            bola.em_movimento = True
            trajetoria = []
            simulacao_ativa = True
    
    # Atualizar estados dos botões
    reset_btn.check_hover(mouse_pos)
    bilhar_simpletico_btn.check_hover(mouse_pos)
    
    # Mover a bola
    bola.mover()
    
    # Verificar colisão com o círculo central
    distancia_centro = math.sqrt((bola.x - circle_center[0])**2 + (bola.y - circle_center[1])**2)
    if distancia_centro + BALL_RADIUS > circle_radius:
        # Calcular vetor normal
        normal_x = (bola.x - circle_center[0]) / distancia_centro
        normal_y = (bola.y - circle_center[1]) / distancia_centro
        
        # Reposicionar a bola
        bola.x = circle_center[0] + normal_x * (circle_radius - BALL_RADIUS - 1)
        bola.y = circle_center[1] + normal_y * (circle_radius - BALL_RADIUS - 1)
        
        # Registrar ponto de colisão
        ponto_colisao = (bola.x, bola.y)
        trajetoria.append(ponto_colisao)
        
        if bilhar_simpletico_btn.toggled and len(trajetoria) >= 2:
            # Bilhar simplético: usar os dois últimos pontos para calcular o próximo
            x = trajetoria[-2]  # Ponto anterior
            y = trajetoria[-1]  # Ponto atual
            z = reflexao_simpletica(x, y, circle_center, circle_radius)
            
            # Calcular nova direção (de y para z)
            nova_direcao_x = z[0] - y[0]
            nova_direcao_y = z[1] - y[1]
            
            # Normalizar e aplicar velocidade
            magnitude = math.sqrt(nova_direcao_x**2 + nova_direcao_y**2)
            if magnitude > 0:
                bola.velocidade_x = nova_direcao_x / magnitude * BALL_SPEED
                bola.velocidade_y = nova_direcao_y / magnitude * BALL_SPEED
        else:
            # Reflexão convencional
            bola.velocidade_x, bola.velocidade_y = reflexao_convencional(
                bola.velocidade_x, bola.velocidade_y, normal_x, normal_y
            )
    
    # Verificar colisão com as bordas da tela
    if bola.x - BALL_RADIUS < 0 or bola.x + BALL_RADIUS > WIDTH:
        bola.velocidade_x *= -1
        bola.x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, bola.x))
    
    if bola.y - BALL_RADIUS < 0 or bola.y + BALL_RADIUS > HEIGHT:
        bola.velocidade_y *= -1
        bola.y = max(BALL_RADIUS, min(HEIGHT - BALL_RADIUS, bola.y))
    
    # Desenhar tudo
    screen.fill(BACKGROUND)
    
    # Desenhar círculo central
    pygame.draw.circle(screen, DARK_GRAY, circle_center, circle_radius)
    pygame.draw.circle(screen, (50, 60, 80), circle_center, circle_radius, 3)
    
    # Desenhar trajetória
    if len(trajetoria) > 1:
        pontos_suavizados = []
        for i in range(len(trajetoria)):
            if i == 0 or i == len(trajetoria) - 1:
                pontos_suavizados.append(trajetoria[i])
            else:
                x = (trajetoria[i-1][0] + trajetoria[i][0] + trajetoria[i+1][0]) / 3
                y = (trajetoria[i-1][1] + trajetoria[i][1] + trajetoria[i+1][1]) / 3
                pontos_suavizados.append((x, y))
        
        pygame.draw.lines(screen, GREEN, False, pontos_suavizados, 2)
        
        # Desenhar pontos de colisão
        for ponto in trajetoria:
            pygame.draw.circle(screen, RED, (int(ponto[0]), int(ponto[1])), 5)
    
    # Desenhar bola
    bola.desenhar(screen)
    
    # Desenhar botões
    reset_btn.draw(screen)
    bilhar_simpletico_btn.draw(screen)
    
    # Desenhar informações
    desenhar_informacoes()
    
    pygame.display.flip()
    clock.tick(60)