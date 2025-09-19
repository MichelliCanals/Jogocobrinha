# Configurações iniciais
import pygame
import random

pygame.init()
pygame.display.set_caption('Jogo snake python')
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Definição de cores (RGB)
cinza_claro = (211, 211, 211)
azul_claro = (32, 69, 97)
laranja_vibrante = (255, 92, 0)
verde_escuro = (6, 64, 43)

# Parametros da cobra
tamanho_quadrado = 20
velocidade_jogo = 10  # Velocidade do jogo diminuída para 10

# Fonte para a pontuação e mensagens
fonte_pontuacao = pygame.font.SysFont("Helvetica", 25)
fonte_game_over = pygame.font.SysFont("Helvetica", 40)


def desenhar_pontuacao(pontuacao):
    texto = fonte_pontuacao.render("Pontos: " + str(pontuacao), True, verde_escuro)
    tela.blit(texto, [0, 0])


def desenhar_game_over(pontuacao):
    msg_fim_jogo = "Game Over"
    texto_pontos = f"Pontuação final: {pontuacao}"
    texto_instrucoes = "Pressione C para jogar novamente ou Q para sair"

    texto_fim_jogo = fonte_game_over.render(msg_fim_jogo, True, verde_escuro)
    texto_final_pontos = fonte_pontuacao.render(texto_pontos, True, azul_claro)
    texto_final_instrucoes = fonte_pontuacao.render(texto_instrucoes, True, azul_claro)

    tela.blit(texto_fim_jogo, [largura / 2 - texto_fim_jogo.get_width() / 2, altura / 3])
    tela.blit(texto_final_pontos, [largura / 2 - texto_final_pontos.get_width() / 2, altura / 3 + 50])
    tela.blit(texto_final_instrucoes, [largura / 2 - texto_final_instrucoes.get_width() / 2, altura / 3 + 90])
    pygame.display.update()


def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    return comida_x, comida_y


def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, laranja_vibrante, [comida_x, comida_y, tamanho, tamanho])


def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, azul_claro, [pixel[0], pixel[1], tamanho, tamanho])


def rodar_jogo():
    while True:
        fim_jogo = False

        x = largura / 2
        y = altura / 2

        velocidade_x = 0
        velocidade_y = 0

        tamanho_cobra = 1
        pixels_da_cobra = []

        comida_x, comida_y = gerar_comida()

        while not fim_jogo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and velocidade_x != tamanho_quadrado:
                        velocidade_x = -tamanho_quadrado
                        velocidade_y = 0
                    elif event.key == pygame.K_RIGHT and velocidade_x != -tamanho_quadrado:
                        velocidade_x = tamanho_quadrado
                        velocidade_y = 0
                    elif event.key == pygame.K_UP and velocidade_y != tamanho_quadrado:
                        velocidade_y = -tamanho_quadrado
                        velocidade_x = 0
                    elif event.key == pygame.K_DOWN and velocidade_y != -tamanho_quadrado:
                        velocidade_y = tamanho_quadrado
                        velocidade_x = 0

            if x >= largura or x < 0 or y >= altura or y < 0:
                fim_jogo = True

            # Velocidade da cobra
            x += velocidade_x
            y += velocidade_y

            # Tela do jogo
            tela.fill(cinza_claro)
            desenhar_comida(tamanho_quadrado, comida_x, comida_y)

            pixels_da_cobra.append([x, y])

            # Tamanho da cobra
            if len(pixels_da_cobra) > tamanho_cobra:
                del pixels_da_cobra[0]

            for pixel in pixels_da_cobra[:-1]:
                if pixel == [x, y]:
                    fim_jogo = True

            desenhar_cobra(tamanho_quadrado, pixels_da_cobra)
            desenhar_pontuacao(tamanho_cobra - 1)

            if x == comida_x and y == comida_y:
                tamanho_cobra += 1
                comida_x, comida_y = gerar_comida()

            pygame.display.update()
            relogio.tick(velocidade_jogo)

        # Loop da tela de Game Over
        while fim_jogo:
            desenhar_game_over(tamanho_cobra - 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        fim_jogo = False  # Sai do loop de Game Over para reiniciar
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

            relogio.tick(velocidade_jogo)


rodar_jogo()