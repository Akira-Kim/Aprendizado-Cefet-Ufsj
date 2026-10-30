import pygame
import sys
import math
import time

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA_TELA, ALTURA_TELA = 800, 600  # Define o tamanho da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))  # Cria a tela
pygame.display.set_caption("Simulação: Bolinha Ricocheteando nos Cantos")  # Título da janela

# Cores
BRANCO = (255, 255, 255)  # Cor branca
PRETO = (0, 0, 0)  # Cor preta
VERMELHO = (255, 0, 0)  # Cor vermelha para a bolinha
CINZA = (200, 200, 200)  # Cor cinza para a sombra da bolinha
AMARELO = (255, 255, 0)  # Cor amarela para o efeito de ricochete
CINZA_CLARO = (211, 211, 211)  # Cor cinza claro para a sombra da bolinha

# Função para exibir texto na tela
def desenhar_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.Font(None, tamanho)  # Cria uma fonte com o tamanho especificado
    superficie_texto = fonte.render(texto, True, cor)  # Renderiza o texto com a cor
    tela.blit(superficie_texto, (x, y))  # Desenha o texto na tela na posição (x, y)

# Função do menu de configuração
def menu():
    tamanho = 500  # Tamanho inicial da forma
    ricochetes = 10  # Número inicial de ricochetes
    angulo = 45  # Ângulo inicial de movimento da bolinha
    tempo_simulacao = 10  # Tempo de simulação em segundos
    num_lados = 3  # Número inicial de lados da forma (começando com triângulo)
    velocidade_bola = 5  # Velocidade inicial da bolinha
    raio_bola = 15  # Raio inicial da bolinha
    cor_rastro = (255, 0, 0)  # Cor inicial do rastro (vermelho)
    largura_rastro = 5  # Largura inicial do rastro

    # Loop do menu para alterar configurações
    while True:
        tela.fill(BRANCO)  # Limpa a tela com a cor branca
        desenhar_texto("MENU DE CONFIGURAÇÃO", 50, PRETO, 200, 50)  # Exibe título
        desenhar_texto(f"Tamanho da Forma: {tamanho} (Setas Cima/Baixo)", 30, PRETO, 50, 150)
        desenhar_texto(f"Número de Ricochetes: {ricochetes} (Setas Esquerda/Direita)", 30, PRETO, 50, 200)
        desenhar_texto(f"Ângulo Inicial: {angulo}° (A/D para ajustar)", 30, PRETO, 50, 250)
        desenhar_texto(f"Tempo de Simulação: {tempo_simulacao} s (W/S para ajustar)", 30, PRETO, 50, 300)
        desenhar_texto(f"Lados da Forma: {num_lados} (Q/E para ajustar)", 30, PRETO, 50, 350)
        desenhar_texto(f"Velocidade da Bolinha: {velocidade_bola} (Z/X para ajustar)", 30, PRETO, 50, 400)
        desenhar_texto(f"Tamanho da Bolinha: {raio_bola} (C/V para ajustar)", 30, PRETO, 50, 450)
        desenhar_texto(f"Cor do Rastro: {cor_rastro} (R para vermelho, G para verde, B para azul)", 30, PRETO, 50, 500)
        desenhar_texto(f"Largura do Rastro: {largura_rastro} (F para diminuir, G para aumentar)", 30, PRETO, 50, 550)
        desenhar_texto("Pressione ENTER para começar", 30, PRETO, 200, 570)
        desenhar_texto("ESC para sair", 20, CINZA, 10, 570)

        # Processa eventos de teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and tamanho < 500:
                    tamanho += 10  # Aumenta o tamanho da forma
                if evento.key == pygame.K_DOWN and tamanho > 50:
                    tamanho -= 10  # Diminui o tamanho da forma
                if evento.key == pygame.K_LEFT:
                    ricochetes = max(1, ricochetes - 1)  # Diminui o número de ricochetes
                if evento.key == pygame.K_RIGHT:
                    ricochetes += 1  # Aumenta o número de ricochetes
                if evento.key == pygame.K_w:
                    tempo_simulacao += 1  # Aumenta o tempo de simulação
                if evento.key == pygame.K_s:
                    tempo_simulacao = max(1, tempo_simulacao - 1)  # Diminui o tempo de simulação
                if evento.key == pygame.K_a:
                    angulo = (angulo - 5) % 360  # Diminui o ângulo de movimento da bolinha
                if evento.key == pygame.K_d:
                    angulo = (angulo + 5) % 360  # Aumenta o ângulo de movimento da bolinha
                if evento.key == pygame.K_q and num_lados > 3:
                    num_lados -= 1  # Diminui o número de lados da forma
                if evento.key == pygame.K_e:
                    num_lados += 1  # Aumenta o número de lados da forma
                if evento.key == pygame.K_z:
                    velocidade_bola = max(1, velocidade_bola - 1)  # Diminui a velocidade da bolinha
                if evento.key == pygame.K_x:
                    velocidade_bola += 1  # Aumenta a velocidade da bolinha
                if evento.key == pygame.K_c:
                    raio_bola = max(5, raio_bola - 1)  # Diminui o tamanho da bolinha
                if evento.key == pygame.K_v:
                    raio_bola += 1  # Aumenta o tamanho da bolinha
                if evento.key == pygame.K_r:
                    cor_rastro = (255, 0, 0)  # Muda a cor do rastro para vermelho
                if evento.key == pygame.K_g:
                    cor_rastro = (0, 255, 0)  # Muda a cor do rastro para verde
                if evento.key == pygame.K_b:
                    cor_rastro = (0, 0, 255)  # Muda a cor do rastro para azul
                if evento.key == pygame.K_f and largura_rastro > 1:
                    largura_rastro -= 1  # Diminui a largura do rastro
                if evento.key == pygame.K_g and largura_rastro < 20:
                    largura_rastro += 1  # Aumenta a largura do rastro
                if evento.key == pygame.K_RETURN:
                    return tamanho, ricochetes, angulo, tempo_simulacao, num_lados, velocidade_bola, raio_bola, cor_rastro, largura_rastro
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()  # Atualiza a tela

# Função para desenhar um polígono regular
def desenhar_poligono(lados, raio, centro_x, centro_y):
    passo_angulo = 2 * math.pi / lados  # Calcula o ângulo de cada lado do polígono
    pontos = [
        (
            centro_x + raio * math.cos(i * passo_angulo),  # Calcula a posição x de cada ponto
            centro_y + raio * math.sin(i * passo_angulo)   # Calcula a posição y de cada ponto
        )
        for i in range(lados)
    ]
    pygame.draw.polygon(tela, PRETO, pontos, 3)  # Desenha o polígono com os pontos calculados
    return pontos

# Função para calcular o novo ângulo da bolinha após o ricochete
def calcular_novo_angulo(dx_bola, dy_bola, angulo_aresta):
    angulo_bola = math.atan2(dy_bola, dx_bola)  # Calcula o ângulo atual da bolinha
    angulo_novo = 2 * angulo_aresta - angulo_bola  # Calcula o novo ângulo de acordo com a física de reflexão
    return math.cos(angulo_novo), math.sin(angulo_novo)

# Função principal da simulação
def principal():
    while True:
        tamanho, ricochetes, angulo, tempo_simulacao, num_lados, velocidade_bola, raio_bola, cor_rastro, largura_rastro = menu()

        # Inicialização das variáveis da bolinha
        x_bola = LARGURA_TELA // 2
        y_bola = ALTURA_TELA // 2
        dx_bola = velocidade_bola * math.cos(math.radians(angulo))  # Velocidade horizontal
        dy_bola = velocidade_bola * math.sin(math.radians(angulo))  # Velocidade vertical
        tempo_inicio = time.time()  # Início do tempo de simulação
        pontos_bola = []  # Lista para armazenar as posições anteriores da bolinha

        # Loop da simulação
        executando = True
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False

            # Atualiza a posição da bolinha
            x_bola += dx_bola
            y_bola += dy_bola

            # Verifica se a bolinha saiu da tela e faz o efeito de ricochete
            if x_bola - raio_bola < 0 or x_bola + raio_bola > LARGURA_TELA:
                dx_bola = -dx_bola
                ricochetes += 1
            if y_bola - raio_bola < 0 or y_bola + raio_bola > ALTURA_TELA:
                dy_bola = -dy_bola
                ricochetes += 1

            # Adiciona a posição atual da bolinha na lista de rastros
            pontos_bola.append((int(x_bola), int(y_bola)))
            if len(pontos_bola) > 200:  # Limita o tamanho da lista de rastros
                pontos_bola.pop(0)

            # Desenha a tela
            tela.fill(BRANCO)  # Preenche a tela com a cor branca
            pontos = desenhar_poligono(num_lados, tamanho // 2, LARGURA_TELA // 2, ALTURA_TELA // 2)  # Desenha a forma

            # Desenha o rastro da bolinha
            for ponto in pontos_bola:
                pygame.draw.circle(tela, cor_rastro, ponto, largura_rastro)  # Desenha cada ponto do rastro

            # Desenha a bolinha
            pygame.draw.circle(tela, VERMELHO, (int(x_bola), int(y_bola)), raio_bola)

            # Exibe o número de ricochetes e o tempo de simulação
            desenhar_texto(f"Ricochetes: {ricochetes}", 30, PRETO, 10, 10)
            desenhar_texto(f"Tempo: {int(time.time() - tempo_inicio)} / {tempo_simulacao}s", 30, PRETO, 10, 40)

            # Verifica se a bolinha colidiu com a forma
            for i in range(len(pontos)):
                x1, y1 = pontos[i]
                x2, y2 = pontos[(i + 1) % len(pontos)]

                # Vetor da aresta
                dx_aresta = x2 - x1
                dy_aresta = y2 - y1
                comprimento_aresta = math.hypot(dx_aresta, dy_aresta)

                # Vetor normalizado da aresta
                nx_aresta = dx_aresta / comprimento_aresta
                ny_aresta = dy_aresta / comprimento_aresta

                # Vetor da bolinha para o ponto inicial da aresta
                bola_para_aresta_x = x_bola - x1
                bola_para_aresta_y = y_bola - y1

                # Projeção do vetor bolinha-aresta na aresta
                projecao = bola_para_aresta_x * nx_aresta + bola_para_aresta_y * ny_aresta

                # Ponto mais próximo na aresta
                ponto_mais_proximo_x = x1 + projecao * nx_aresta
                ponto_mais_proximo_y = y1 + projecao * ny_aresta

                # Verifica se a bolinha tocou a aresta
                distancia = math.hypot(ponto_mais_proximo_x - x_bola, ponto_mais_proximo_y - y_bola)
                if distancia <= raio_bola:
                    dx_bola, dy_bola = calcular_novo_angulo(dx_bola, dy_bola, math.atan2(dy_aresta, dx_aresta))
                    ricochetes += 1

            # Verifica o tempo de simulação
            if time.time() - tempo_inicio >= tempo_simulacao:
                executando = False  # Termina a simulação após o tempo passar

            pygame.display.flip()  # Atualiza a tela
            pygame.time.Clock().tick(60)  # Limita a taxa de quadros para 60 FPS

        pygame.time.delay(1000)  # Aguarda 1 segundo antes de voltar ao menu

if __name__ == "__main__":
    principal()  # Inicia a simulação
