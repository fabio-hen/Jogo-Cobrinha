import pygame
import random

WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 600
POS_INIT_X = WINDOWS_WIDTH / 2
POS_INIT_Y = WINDOWS_HEIGHT / 2
BLOCK = 10


def game_over():
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
    return x // BLOCK * BLOCK, y // BLOCK * BLOCK


def verifica_colisao(cobra_pos):
    # Verifica se a posição está dentro dos limites da janela
    if 0 <= pos[0] < WINDOWS_WIDTH and 0 <= pos[1] < WINDOWS_HEIGHT:
        return False  # Não houve colisão
    else:
        return True  # Houve colisão


pygame.init()
windows = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))

cobra_pos = [(POS_INIT_X, POS_INIT_Y)]  # Posição inicial da cobra
cobra_surfece = pygame.Surface((BLOCK, BLOCK))  # Cria a superfície da cobra
# Preenche a superfície da cobra com a cor cinza escuro
cobra_surfece.fill((53, 59, 72))
direcao = pygame.K_LEFT

maca_surfece = pygame.Surface((BLOCK, BLOCK))  # Cria a superfície da maçã
# Preenche a superfície da maçã com a cor vermelha
maca_surfece.fill((255, 0, 0))
maca_pos = gera_pos_aleatoria()


while True:
    pygame.time.Clock().tick(10)        # Controla a taxa de atualização do jogo
    windows.fill((68, 189, 50))         # Preenche a janela com a cor verde

    for event in pygame.event.get():    # Verifica os eventos
        if event.type == pygame.QUIT:   # Se o evento for fechar a janela
            pygame.quit()               # Encerra o pygame
            exit()

        elif event.type == pygame.KEYDOWN:                                # Se uma tecla for pressionada
            # Se a tecla for uma das setas
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                # Atualiza a direção da cobra
                direcao = event.key

    windows.blit(maca_surfece, maca_pos)  # Desenha a maçã na janela

    # Verifica se a cobra comeu a maçã
    if verifica_colisao_maca(cobra_pos[0], maca_pos):
        maca_pos = gera_pos_aleatoria()  # Gera uma nova posição para a maçã

    for pos in cobra_pos:                # Desenha a cobra na janela
        # Desenha a superfície da cobra na posição atual
        windows.blit(cobra_surfece, pos)

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

    pygame.display.update()              # Atualiza a janela
