import pygame
import random

WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 600
POS_INIT_X = WINDOWS_WIDTH // 2
POS_INIT_Y = WINDOWS_HEIGHT // 2
BLOCK = 10

pontos = 0
velocidade = 10

pygame.font.init()  # Inicializa o módulo de fontes do Pygame
# Cria uma fonte do sistema Arial, tamanho 35, negrito e itálico
fonte = pygame.font.SysFont('Arial', 35, True,  True)


def game_over():
    # Cria uma fonte maior para a mensagem de game over
    fonte = pygame.font.SysFont('Arial', 60, True,  True)
    mensagem = 'Game Over!'  # Cria a mensagem de game over com a pontuação
    # Formata o texto da mensagem de game over
    texto_formatado = fonte.render(mensagem, True, (255, 0, 0))
    windows.blit(texto_formatado, (110, 300))  # Desenha a mensagem na janela
    pygame.display.update()  # Atualiza a janela para mostrar a mensagem
    pygame.time.delay(3000)  # Aguarda 3 segundos antes de encerrar o jogo
    pygame.quit()
    exit()


def verifica_colisao_maca(cobra_pos, maca_pos):
    # Verifica se a cabeça da cobra está na mesma posição da maçã
    return cobra_pos == maca_pos


def gera_pos_aleatoria():
    # Gera uma posição x aleatória dentro da largura da janela
    x = random.randint(0, (WINDOWS_WIDTH))
    # Gera uma posição y aleatória dentro da altura da janela
    y = random.randint(0, (WINDOWS_HEIGHT))
    # Garante que a posição esteja alinhada com o tamanho do bloco
    # Evita que a maçã seja gerada em cima de um obstáculo ou da cobra
    if (x, y) in obstaculos or (x, y) in cobra_pos:
        gera_pos_aleatoria()
    return x // BLOCK * BLOCK, y // BLOCK * BLOCK


def verifica_colisao(cobra_pos):
    # Verifica se a posição está dentro dos limites da janela
    if 0 <= cobra_pos[0] < WINDOWS_WIDTH and 0 <= cobra_pos[1] < WINDOWS_HEIGHT:
        return False  # Não houve colisão
    else:
        return True  # Houve colisão


pygame.init()
windows = pygame.display.set_mode(
    (WINDOWS_WIDTH, WINDOWS_HEIGHT))  # Cria a janela do jogo
pygame.display.set_caption("Jogo da Cobrinha")  # Define o título da janela

cobra_pos = [(POS_INIT_X, POS_INIT_Y), (POS_INIT_X + BLOCK, POS_INIT_Y),
             (POS_INIT_X + 2 * BLOCK, POS_INIT_Y)]  # Posição inicial da cobra
cobra_surfece = pygame.Surface((BLOCK, BLOCK))  # Cria a superfície da cobra
# Preenche a superfície da cobra com a cor cinza escuro
cobra_surfece.fill((53, 59, 72))
direcao = pygame.K_LEFT

obstaculos = []  # Lista de obstáculos (não utilizada no momento)
# Cria a superfície dos obstáculos
obstaculos_surface = pygame.Surface((BLOCK, BLOCK))
# Preenche a superfície dos obstáculos com a cor preta
obstaculos_surface.fill((0, 0, 0))

maca_surfece = pygame.Surface((BLOCK, BLOCK))  # Cria a superfície da maçã
# Preenche a superfície da maçã com a cor vermelha
maca_surfece.fill((255, 0, 0))
maca_pos = gera_pos_aleatoria()

while True:
    # Controla a taxa de atualização do jogo
    pygame.time.Clock().tick(velocidade)
    windows.fill((68, 189, 50))         # Preenche a janela com a cor verde

    mensagem = f'Pontos: {pontos}'          # Cria a mensagem de pontuação
    # Formata o texto da pontuação
    texto_formatado = fonte.render(mensagem, True, (255, 255, 255))

    for event in pygame.event.get():    # Verifica os eventos
        if event.type == pygame.QUIT:   # Se o evento for fechar a janela
            pygame.quit()               # Encerra o pygame
            exit()

        elif event.type == pygame.KEYDOWN:                                # Se uma tecla for pressionada
            # Se a tecla for uma das setas
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                if event.key == pygame.K_UP and direcao == pygame.K_DOWN:
                    continue  # Ignora se a direção atual é para baixo
                elif event.key == pygame.K_DOWN and direcao == pygame.K_UP:
                    continue  # Ignora se a direção atual é para cima
                elif event.key == pygame.K_LEFT and direcao == pygame.K_RIGHT:
                    continue  # Ignora se a direção atual é para a direita
                elif event.key == pygame.K_RIGHT and direcao == pygame.K_LEFT:
                    continue  # Ignora se a direção atual é para a esquerda
                else:
                    # Atualiza a direção da cobra
                    direcao = event.key

    windows.blit(maca_surfece, maca_pos)  # Desenha a maçã na janela

    # Verifica se a cobra comeu a maçã
    if verifica_colisao_maca(cobra_pos[0], maca_pos):
        cobra_pos.append((-10, -10))  # Adiciona um novo segmento à cobra
        maca_pos = gera_pos_aleatoria()  # Gera uma nova posição para a maçã
        obstaculos.append(gera_pos_aleatoria())  # Adiciona um novo obstáculo
        pontos += 1                  # Incrementa a pontuação
        if pontos % 3 == 0:          # A cada 3 pontos
            velocidade += 3          # Aumenta a velocidade do jogo

    for pos in obstaculos:              # Desenha os obstáculos na janela
        # Verifica se a cobra colidiu com um obstáculo
        if verifica_colisao_maca(cobra_pos[0], pos):
            game_over()                 # Encerra o jogo se houve colisão
        # Desenha a superfície do obstáculo na posição atual
        windows.blit(obstaculos_surface, pos)

    for pos in cobra_pos:                # Desenha a cobra na janela
        # Desenha a superfície da cobra na posição atual
        windows.blit(cobra_surfece, pos)

    for item in range(len(cobra_pos) - 1, 0, -1):
        # Verifica se a cobra colidiu consigo mesma
        if verifica_colisao_maca(cobra_pos[0], cobra_pos[item]):
            game_over()                     # Encerra o jogo se houve colisão
        # Move cada segmento da cobra para a posição do segmento anterior
        cobra_pos[item] = cobra_pos[item - 1]

    if verifica_colisao(cobra_pos[0]):  # Verifica se houve colisão
        game_over()                     # Encerra o jogo se houve colisão

    if direcao == pygame.K_RIGHT:
        # Move a cabeça da cobra para a direita
        cobra_pos[0] = (cobra_pos[0][0] + BLOCK, cobra_pos[0][1])

    elif direcao == pygame.K_LEFT:
        cobra_pos[0] = (cobra_pos[0][0] - BLOCK, cobra_pos[0]
                        [1])  # Move a cabeça da cobra para a

    elif direcao == pygame.K_UP:
        # Move a cabeça da cobra para cima
        cobra_pos[0] = (cobra_pos[0][0], cobra_pos[0][1] - BLOCK)

    elif direcao == pygame.K_DOWN:
        # Move a cabeça da cobra para baixo
        cobra_pos[0] = (cobra_pos[0][0], cobra_pos[0][1] + BLOCK)

    # Desenha o texto da pontuação na janela
    windows.blit(texto_formatado, (10, 10))
    pygame.display.update()              # Atualiza a janela
