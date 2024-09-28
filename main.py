# 1. IMPORT ---------------

# pip install pygame
import pygame
import random

from shoot import Shoot
from ghost import Ghost
from bat import Bat

# 2. INICIALIZAÇÃO ----------------
# Iniciar o Pygame
pygame.init()

# Inciando a janela com a confirguração de resolução de 840 x 480

# Constantes de largura e altura
WIDTH_SCREEN = 840  # Largura
HEIGHT_SCREEN = 480  # Altura

display = pygame.display.set_mode([WIDTH_SCREEN, HEIGHT_SCREEN])

# Preenche o fundo da janela com a cor em RGB
display.fill([252, 207, 3])

# Muda o titulo da janela
pygame.display.set_caption("Game SENAI - Python")

# Carregar a imagem para criar o icone, converter a imagem em formato icone
icone = pygame.image.load("data/icone.png")
pygame.display.set_icon(icone)

# 3. Elementos de Tela ---------

# 3 .1 Personagens

# Criando um grupo de imagem para carregar e desenhar todas as imagens de uma unica vez
objectGroup = pygame.sprite.Group()
batGroup = pygame.sprite.Group()
shootGroup = pygame.sprite.Group()

# Criar um fundo (background) para o fanstama
bg  = pygame.sprite.Sprite(objectGroup)
bg.image = pygame.image.load("data/background.jpg")
bg.image = pygame.transform.scale(bg.image, [840, 480])
bg.rect = bg.image.get_rect()

# Criar o objeto Ghost - fanstasma
ghost = Ghost(objectGroup)

bat = Bat(objectGroup, batGroup)

shoot = Shoot(objectGroup, shootGroup)

# 3.2 Fonte ----------
score_font = pygame.font.Font("font/Pixeltype.ttf", 50)
gameOver_font = pygame.font.Font("font/Pixeltype.ttf", 200)

# 3.3 Música
pygame.mixer.music.load("data/alienblues.wav")
pygame.mixer.music.play(-1)

# 3.4 Som -------
attack = pygame.mixer.Sound("data/magic1.wav")

# 4. VARIAVEIS GLOBAIS ---------------

# Variavel para controlar o loop
gameLoop = True
gameOver = False

timer = 20
pontos = 0
# Criar um clock para ajustar os frames por segundo (FPS)
clock = pygame.time.Clock()

# 5. FUNÇAO PRINCIPAL --------------


def main():
    global gameLoop
    global gameOver
    global timer
    global pontos

    while gameLoop:
        # Clock para 60fps
        clock.tick(60)
        # Loop para verificar os possíveis eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    attack.play()
                    newShoot = Shoot(objectGroup, shootGroup)
                    newShoot.rect.center = ghost.rect.center

        if not gameOver:
            # A cor de fundo da janela
            display.fill([252, 207, 3])

            # Criação de varios morcegos
            timer += 1
            if timer > 30:
                timer = 0
                if random.random() < 0.3:
                    newBat = Bat(objectGroup, batGroup)

            # Colisão dos morcegos com o fantasma
            colisao = pygame.sprite.spritecollide(
                ghost, batGroup, False, pygame.sprite.collide_mask)

            if colisao:
                print("GAME OVER!!!!")
                gameOver = True

            # Colisão do tiro com morcego
            tiros = pygame.sprite.groupcollide(shootGroup, batGroup, True, True, pygame.sprite.collide_mask)

            # Contagem de morcegos mortos
            if tiros:
                pontos += 1
                print("SCORE:", pontos)

            objectGroup.update()
        
        # Desenhando os elementos do grupo na janela
        objectGroup.draw(display)

        # Inserir a pontuação na tela

        score_render = score_font.render(f'Score: {pontos}', False, 'White')
        display.blit(score_render, (650 ,50))

        # Inserir o GAME OVER na tela
        if gameOver:
            gameOverMsg = gameOver_font.render('GAME OVER', False, 'White')
            display.blit(gameOverMsg, (100, 150))


        pygame.display.update()


if __name__ == "__main__":
    main()
