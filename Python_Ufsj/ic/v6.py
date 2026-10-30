import pygame
import sys
import math
import time

# Inicialização do Pygame
pygame.init()

# Obter as dimensões da tela
LARGURA_TELA, ALTURA_TELA = pygame.display.Info().current_w, pygame.display.Info().current_h

# Criar a tela em modo fullscreen
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.FULLSCREEN)
pygame.display.set_caption("Simulação: Bilhares Simpleticos")

# Cores baseadas no gradiente solicitado
VERMELHO_ESCURO = (128, 0, 128)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)

# Função para criar gradiente de fundo
def gradiente_fundo(tela, cor1, cor2, largura, altura):
    for y in range(altura):
        cor_intermediaria = [
            cor1[i] + (cor2[i] - cor1[i]) * y // altura for i in range(3)
        ]
        pygame.draw.line(tela, cor_intermediaria, (0, y), (largura, y))

# Função para exibir texto centralizado
def centralizar_texto(texto, tamanho, cor, y):
    fonte = pygame.font.Font(None, tamanho)
    superficie_texto = fonte.render(texto, True, cor)
    largura_texto = superficie_texto.get_width()
    x = (LARGURA_TELA - largura_texto) // 2
    tela.blit(superficie_texto, (x, y))

# Função para desenhar um botão
def desenhar_botao(texto, x, y, largura, altura, cor_normal, cor_hover, cor_texto_hover=PRETO):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x < mouse_x < x + largura and y < mouse_y < y + altura:
        cor = cor_hover
        cor_texto = cor_texto_hover
    else:
        cor = cor_normal
        cor_texto = PRETO
    pygame.draw.rect(tela, cor, (x, y, largura, altura))
    desenhar_texto(texto, 30, cor_texto, x + 20, y + 15)

# Função para desenhar texto
def desenhar_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.Font(None, tamanho)
    superficie_texto = fonte.render(texto, True, cor)
    tela.blit(superficie_texto, (x, y))

# Função para desenhar o polígono
def desenhar_poligono(lados, tamanho, centro_x, centro_y):
    pontos = []
    for i in range(lados):
        angulo = i * (2 * math.pi / lados)
        x = centro_x + tamanho * math.cos(angulo)
        y = centro_y + tamanho * math.sin(angulo)
        pontos.append((x, y))
    pygame.draw.polygon(tela, PRETO, pontos, 3)  # Linhas pretas para contraste
    return pontos

# Função para calcular a normal de uma aresta
def calcular_normal(x1, y1, x2, y2):
    normal_x = y2 - y1
    normal_y = x1 - x2
    norma = math.sqrt(normal_x ** 2 + normal_y ** 2)
    return normal_x / norma, normal_y / norma

# Função para aplicar a reflexão de acordo com o tipo
def aplicar_reflexao(tipo_reflexao, dx, dy, normal_x, normal_y):
    produto_escalar = dx * normal_x + dy * normal_y
    ajuste = 2 if tipo_reflexao == 0 else (1.5 if tipo_reflexao == 2 else 2)  # Tangente Nova é equivalente à Perfeita
    dx -= ajuste * produto_escalar * normal_x
    dy -= ajuste * produto_escalar * normal_y
    return dx, dy

# Função para adicionar pontos ao rastro
def adicionar_rastro(rastro, x_bola, y_bola):
    rastro.append((x_bola, y_bola))

# Função para desenhar o rastro da bolinha
def desenhar_rastro(rastro, tela):
    for i in range(len(rastro) - 1):
        # Obtemos a posição de cada ponto do rastro
        x1, y1 = rastro[i]
        x2, y2 = rastro[i + 1]
        
        # Calculando a cor do rastro com base na distância percorrida
        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        cor_rastro = (max(0, 255 - int(distancia)), max(0, 255 - int(distancia)), max(0, 255 - int(distancia)))
        
        # Desenhando a linha com o gradiente de cinza
        pygame.draw.line(tela, cor_rastro, (x1, y1), (x2, y2), 2)

def menu():
    # Definindo valores iniciais
    config = {
        'tamanho': 500,
        'ricochetes': 10,
        'angulo': 45,
        'tempo_simulacao': 10,
        'num_lados': 6,
        'velocidade_bola': 5,
        'raio_bola': 15,
        'tipo_reflexao': 0  # 0: Reflexão Perfeita, 1: Reflexão com Tangente Nova, 2: Reflexão Suave
    }

    editar_valor = None
    texto_digitado = ""

    while True:
        gradiente_fundo(tela, VERMELHO_ESCURO, BRANCO, LARGURA_TELA, ALTURA_TELA)

        # Cabeçalho Superior
        centralizar_texto("Bilhares Simpleticos", 70, PRETO, 20)

        # Desenhando botões interativos para ajustar os parâmetros
        y = 150
        for key, value in config.items():
            if key == 'tipo_reflexao':
                tipo_reflexao_texto = ['Perfeita', 'Tangente Nova', 'Suave'][value]
                desenhar_botao(f"Tipo de Reflexão: {tipo_reflexao_texto}", 600, y, 500, 60, BRANCO, VERMELHO)
            else:
                desenhar_botao(f"{key.capitalize()}: {value}", 50, y, 500, 60, BRANCO, VERMELHO)
            y += 70

        # Botões de navegação para menu
        desenhar_botao("Iniciar", 600, 500, 500, 60, BRANCO, VERMELHO)
        desenhar_botao("Sair", 600, 570, 500, 60, BRANCO, VERMELHO)

        # Captura de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detecção de clique de mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Verificando qual botão foi pressionado
                if 50 < mouse_x < 550:
                    y = 150
                    for key in config.keys():
                        if y < mouse_y < y + 60:
                            editar_valor = key
                            texto_digitado = str(config[key])
                            break
                        y += 70

                # Ajustando o tipo de reflexão
                if 600 < mouse_x < 1100 and 150 < mouse_y < 210:
                    config['tipo_reflexao'] = (config['tipo_reflexao'] + 1) % 3

                # Iniciar a simulação
                if 600 < mouse_x < 1100 and 500 < mouse_y < 560:
                    return config.values()
                
                # Sair
                if 600 < mouse_x < 1100 and 570 < mouse_y < 630:
                    pygame.quit()
                    sys.exit()

            # Captura de eventos de teclado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    texto_digitado = texto_digitado[:-1]  # Apagar o último caractere digitado
                elif evento.key == pygame.K_RETURN:
                    if editar_valor:
                        try:
                            config[editar_valor] = int(texto_digitado)
                        except ValueError:
                            pass  # Tratar erro de conversão
                        editar_valor = None  # Finaliza a edição
                else:
                    texto_digitado += evento.unicode  # Adiciona o caractere digitado

        # Exibe o valor que está sendo editado
        if editar_valor:
            desenhar_texto(f"Digite o valor de {editar_valor}: {texto_digitado}", 30, PRETO, 50, 650)

        pygame.display.flip()

# Função principal
def principal():
    while True:
        # Chama o menu para obter as configurações
        tamanho, max_ricochetes, angulo, tempo_simulacao, num_lados, velocidade_bola, raio_bola, tipo_reflexao = menu()

        # Configurações iniciais da bolinha
        x_bola, y_bola = LARGURA_TELA // 2, ALTURA_TELA // 2
        dx_bola = velocidade_bola * math.cos(math.radians(angulo))
        dy_bola = velocidade_bola * math.sin(math.radians(angulo))

        # Configurações da forma
        centro_x, centro_y = LARGURA_TELA // 2, ALTURA_TELA // 2

        ricochetes = 0
        relogio = pygame.time.Clock()
        tempo_inicio = time.time()
        tempo_fim = tempo_inicio + tempo_simulacao
        executando = True

        rastro = []  # Lista para armazenar os pontos do rastro

        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Atualiza a posição da bolinha
            x_bola += dx_bola
            y_bola += dy_bola

            # Adiciona o ponto atual ao rastro
            adicionar_rastro(rastro, x_bola, y_bola)

            # Desenha a tela
            gradiente_fundo(tela, VERMELHO, BRANCO, LARGURA_TELA, ALTURA_TELA)

            # Cabeçalho Superior
            centralizar_texto("Bilhares Simpleticos", 70, PRETO, 20)

            # Desenha o rastro da bolinha
            desenhar_rastro(rastro, tela)

            pontos = desenhar_poligono(num_lados, tamanho // 2, centro_x, centro_y)

            # Sombra da bolinha
            pygame.draw.circle(tela, PRETO, (int(x_bola) + 3, int(y_bola) + 3), raio_bola)
            pygame.draw.circle(tela, VERMELHO, (int(x_bola), int(y_bola)), raio_bola)

            # Verifica a colisão com as arestas do polígono
            for i in range(len(pontos)):
                x1, y1 = pontos[i]
                x2, y2 = pontos[(i + 1) % len(pontos)]
                
                # Verifica se há colisão
                dist = abs((y2 - y1) * x_bola - (x2 - x1) * y_bola + x2 * y1 - y2 * x1) / math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
                if dist <= raio_bola:
                    normal_x, normal_y = calcular_normal(x1, y1, x2, y2)
                    dx_bola, dy_bola = aplicar_reflexao(tipo_reflexao, dx_bola, dy_bola, normal_x, normal_y)
                    ricochetes += 1

                    if ricochetes >= max_ricochetes:
                        executando = False

            desenhar_texto(f"Ricochetes: {ricochetes}/{max_ricochetes}", 30, PRETO, 10, 10)
            desenhar_texto(f"Tempo: {int(time.time() - tempo_inicio)} / {tempo_simulacao}s", 30, PRETO, 10, 40)

            # Verifica o tempo restante
            if time.time() >= tempo_fim:
                executando = False

            pygame.display.flip()
            relogio.tick(60)

# Iniciar a simulação
if __name__ == "__main__":
    principal()
