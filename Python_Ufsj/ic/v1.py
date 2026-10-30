import pygame
import sys
import math
import time

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulação: Bolinha Ricocheteando nos Cantos")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Função para exibir texto
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Função do menu
def menu():
    size = 500
    bounces = 10
    angle = 45
    simulation_time = 10  # Tempo de simulação em segundos
    num_sides = 3  # Número de lados da forma inicial (quadrado)
    ball_speed = 5  # Velocidade da bolinha
    ball_radius = 15  # Tamanho da bolinha

    while True:
        screen.fill(WHITE)
        draw_text("MENU DE CONFIGURAÇÃO", 50, BLACK, 200, 50)
        draw_text(f"Tamanho da Forma: {size} (Setas Cima/Baixo)", 30, BLACK, 50, 150)
        draw_text(f"Número de Ricochetes: {bounces} (Setas Esquerda/Direita)", 30, BLACK, 50, 200)
        draw_text(f"Ângulo Inicial: {angle}° (A/D para ajustar)", 30, BLACK, 50, 250)
        draw_text(f"Tempo de Simulação: {simulation_time} s (W/S para ajustar)", 30, BLACK, 50, 300)
        draw_text(f"Lados da Forma: {num_sides} (Q/E para ajustar)", 30, BLACK, 50, 350)
        draw_text(f"Velocidade da Bolinha: {ball_speed} (Z/X para ajustar)", 30, BLACK, 50, 400)
        draw_text(f"Tamanho da Bolinha: {ball_radius} (C/V para ajustar)", 30, BLACK, 50, 450)
        draw_text("Pressione ENTER para começar", 30, BLACK, 200, 500)
        draw_text("ESC para sair", 20, GRAY, 10, 570)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and size < 500:
                    size += 10
                if event.key == pygame.K_DOWN and size > 50:
                    size -= 10
                if event.key == pygame.K_LEFT:
                    bounces = max(1, bounces - 1)
                if event.key == pygame.K_RIGHT:
                    bounces += 1
                if event.key == pygame.K_w:
                    simulation_time += 1
                if event.key == pygame.K_s:
                    simulation_time = max(1, simulation_time - 1)
                if event.key == pygame.K_a:
                    angle = (angle - 5) % 360
                if event.key == pygame.K_d:
                    angle = (angle + 5) % 360
                if event.key == pygame.K_q and num_sides > 3:
                    num_sides -= 1
                if event.key == pygame.K_e:
                    num_sides += 1
                if event.key == pygame.K_z:
                    ball_speed = max(1, ball_speed - 1)
                if event.key == pygame.K_x:
                    ball_speed += 1
                if event.key == pygame.K_c:
                    ball_radius = max(5, ball_radius - 1)
                if event.key == pygame.K_v:
                    ball_radius += 1
                if event.key == pygame.K_RETURN:
                    return size, bounces, angle, simulation_time, num_sides, ball_speed, ball_radius
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Função para desenhar um polígono regular
def draw_polygon(sides, radius, center_x, center_y):
    angle_step = 2 * math.pi / sides
    points = [
        (
            center_x + radius * math.cos(i * angle_step),
            center_y + radius * math.sin(i * angle_step)
        )
        for i in range(sides)
    ]
    pygame.draw.polygon(screen, BLACK, points, 3)
    return points

# Função para calcular o novo ângulo de saída
def calculate_new_angle(ball_dx, ball_dy, edge_angle):
    ball_angle = math.atan2(ball_dy, ball_dx)
    relative_angle = ball_angle - edge_angle
    new_angle = edge_angle - relative_angle
    return math.cos(new_angle) * math.hypot(ball_dx, ball_dy), math.sin(new_angle) * math.hypot(ball_dx, ball_dy)

# Função principal
def main():
    size, max_bounces, angle, simulation_time, num_sides, ball_speed, ball_radius = menu()

    # Configurações da esfera
    ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    ball_dx = ball_speed * math.cos(math.radians(angle))
    ball_dy = ball_speed * math.sin(math.radians(angle))

    # Configurações da forma
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    bounces = 0
    clock = pygame.time.Clock()
    running = True
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualizar posição da bola
        ball_x += ball_dx
        ball_y += ball_dy

        # Desenhar elementos
        screen.fill(WHITE)
        points = draw_polygon(num_sides, size // 2, center_x, center_y)
        pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
        draw_text(f"Ricochetes nos Cantos: {bounces}/{max_bounces}", 30, BLACK, 10, 10)
        draw_text(f"Tempo: {int(time.time() - start_time)} / {simulation_time}s", 30, BLACK, 10, 40)

        # Detectar colisão com os lados do polígono
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]

            # Vetor da aresta
            edge_dx = x2 - x1
            edge_dy = y2 - y1
            edge_length = math.hypot(edge_dx, edge_dy)

            # Vetor normalizado da aresta
            edge_nx = edge_dx / edge_length
            edge_ny = edge_dy / edge_length

            # Vetor do centro da bola para o ponto inicial da aresta
            ball_to_edge_x = ball_x - x1
            ball_to_edge_y = ball_y - y1

            # Projeção do vetor bola-aresta na aresta
            projection = ball_to_edge_x * edge_nx + ball_to_edge_y * edge_ny

            # Ponto mais próximo na aresta
            closest_x = x1 + projection * edge_nx
            closest_y = y1 + projection * edge_ny

            # Distância do ponto mais próximo até a bola
            distance = math.hypot(closest_x - ball_x, closest_y - ball_y)

            if distance <= ball_radius and 0 <= projection <= edge_length:
                edge_angle = math.atan2(edge_dy, edge_dx)
                ball_dx, ball_dy = calculate_new_angle(ball_dx, ball_dy, edge_angle)
                bounces += 1
                break

        # Verificar condições de parada
        if time.time() - start_time >= simulation_time or bounces >= max_bounces:
            running = False

        pygame.display.flip()
        clock.tick(60)

    # Exibir mensagem final
    screen.fill(WHITE)
    if time.time() - start_time >= simulation_time:
        draw_text("Tempo de simulação esgotado!", 50, BLACK, 150, 250)
    elif bounces >= max_bounces:
        draw_text("Número máximo de ricochetes atingido!", 50, BLACK, 100, 250)
    else:
        draw_text("Simulação Encerrada", 50, BLACK, 200, 250)

    pygame.display.flip()
    pygame.time.wait(3000)  # Pausa de 3 segundos antes de fechar
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
