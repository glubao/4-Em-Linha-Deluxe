import pygame
import random

pygame.init()

clock = pygame.time.Clock()

# Carregar fonte e imagens
fonte_padrao = pygame.font.SysFont('comic sans', 30, bold=True)
amarelo = pygame.image.load('./assets/amarelo.png')
amarelo = pygame.transform.scale(amarelo, (80, 80))
vermelho = pygame.image.load('./assets/vermelho.png')
vermelho = pygame.transform.scale(vermelho, (80, 80))
botao = pygame.image.load('./assets/botao.png')

pygame.display.set_icon(amarelo)

# Carregar efeitos sonoros e música 
ficha_sfx = pygame.mixer.Sound('./assets/som ficha caindo.mp3')
vitoria_sfx = pygame.mixer.Sound('./assets/vitoria.mp3')
vitoria_sfx.set_volume(0.6)

musica = pygame.mixer.music.load('./assets/musica.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Classe de botão
class Button():
    def __init__(self, img, pos_x, pos_y, texto_botao, janela, fonte):
        self.img = img
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.img.get_rect(center=(self.pos_x,self.pos_y))
        self.texto_botao = texto_botao
        self.fonte = fonte
        self.texto = fonte.render(self.texto_botao, True, 'white')
        self.texto_rect = self.texto.get_rect(center=(self.pos_x, self.pos_y))
        self.janela = janela

    def update(self):
        self.janela.blit(self.img, self.rect)
        self.janela.blit(self.texto, self.texto_rect)

    def checarInput(self, posicao):
        if posicao[0] in range(self.rect.left, self.rect.right) and posicao[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

    def hover(self, posicao):
        if posicao[0] in range(self.rect.left, self.rect.right) and posicao[1] in range(self.rect.top, self.rect.bottom):
            self.texto = self.fonte.render(self.texto_botao, True, 'yellow')
        else:
            self.texto = self.fonte.render(self.texto_botao, True, 'white')

# Função main
def main():
    pygame.init()

    # Configuração da janela
    pygame.display.set_caption('4 Em Linha Deluxe')

    # Variável de rodando
    run = True

    while run:
        run = menu_principal()

    pygame.quit()

# Menu
def menu_principal():
    largura_fundo = 900
    altura_fundo = 800
    janela = pygame.display.set_mode((largura_fundo, altura_fundo))

    # Redefine as vitórias de ambos os jogadores
    vitoriasJ1 = 0
    vitoriasJ2 = 0

    fundo = pygame.image.load('./assets/fundo_menu.png')
    fundo = pygame.transform.scale(fundo, (largura_fundo, altura_fundo))

    fonte = pygame.font.SysFont('comic sans', 15, bold=True)
    copyright_fm = fonte.render('©2024 francisco matheus', True, 'white')

    botao_base = pygame.image.load('./assets/botao.png')
    botao_base = pygame.transform.scale(botao_base, (200, 75))

    botao_iniciar = Button(botao_base, largura_fundo // 2, altura_fundo // 2 + 50, 'iniciar', janela, fonte_padrao)
    botao_sair = Button(botao_base, largura_fundo // 2, altura_fundo // 2 + 150, 'sair', janela, fonte_padrao)

    # SUBSTITUIR PELA LOGO DEPOIS
    logo = pygame.image.load('./assets/logo.png')
    # fonte = pygame.font.SysFont('comic sans', 100, bold=True)
    # texto_principal = fonte.render('4 em linha', True, 'white')

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.checarInput(pygame.mouse.get_pos()):
                    run = play(vitoriasJ1, vitoriasJ2)

                if botao_sair.checarInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()

        janela.blit(fundo, (0,0))
        janela.blit(logo, (450 - 549, 100))
        janela.blit(copyright_fm, (5, 780))

        botao_iniciar.update()
        botao_iniciar.hover(pygame.mouse.get_pos())

        botao_sair.update()
        botao_sair.hover(pygame.mouse.get_pos())

        pygame.display.update()
    
    pygame.quit()

    return False

# Função do jogo
def play(vitoriasJ1, vitoriasJ2):
    # Linhas
    circ_largura = 100
    circ_altura = 100
    linhas = 6
    colunas = 7
    largura_janela = colunas * circ_largura
    altura_janela = linhas * circ_altura
    largura_fundo = largura_janela + 200 # 900
    altura_fundo = altura_janela + 200 # 800
    janela = pygame.display.set_mode((largura_fundo, altura_fundo))

    # Fundo
    fundo_imagem = pygame.image.load('./assets/fundo_jogo.png')
    fundo_imagem = pygame.transform.scale(fundo_imagem, (largura_fundo, altura_fundo))

    #fundo = pygame.Surface((largura_janela, altura_janela))
    #fundo.fill("black")
    esqueleto = pygame.image.load('./assets/esqueleto.png')

    fonte = pygame.font.SysFont('comic sans', 30, bold=True)

    # Lógica do tabuleiro
    tabuleiro = []
    for i in range(6):
        tabuleiro.append([])
        for j in range(7):
            tabuleiro[i].append(0)

    # Função de desenhar pop-up na tela
    def desenharPopupVitoria(janela, vencedor):
        largura_popup = 350
        altura_popup = 200
        popup_x = (largura_fundo - largura_popup) // 2
        popup_y = (altura_fundo - altura_popup) // 2

        amarelo = pygame.image.load('./assets/amarelo.png')
        vermelho = pygame.image.load('./assets/vermelho.png')
        amarelo = pygame.transform.scale(amarelo, (50,50))
        vermelho = pygame.transform.scale(vermelho, (50,50))

        popup_surf = pygame.Surface((largura_popup, altura_popup), pygame.SRCALPHA)
        popup_surf.fill((0,0,0,190))

        fonte = pygame.font.SysFont('comic sans', 25, bold=True)
        if vencedor != 3:
            texto = fonte.render(f'vitória do jogador {vencedor}!', True, 'white')
            vitoria_sfx.play()
        else:
            texto = fonte.render('empate!', True, 'white')
        texto_rect = texto.get_rect(center=(largura_popup // 2, 25))
        popup_surf.blit(texto, texto_rect)

        popup_surf.blit(vermelho, (largura_popup // 2 - 100, 50))
        popup_surf.blit(amarelo, (largura_popup // 2 + 50, 50))
        vitJ1 = fonte.render(f'{vitoriasJ1}', True, 'white')
        vitJ2 = fonte.render(f'{vitoriasJ2}', True, 'white')
        vitJ1_rect = vitJ1.get_rect(center=(largura_popup // 2 - 25, 75))
        vitJ2_rect = vitJ2.get_rect(center=(largura_popup // 2 + 25, 75))
        x = fonte.render('x', True, 'white')
        x_rect = x.get_rect(center=(largura_popup // 2, 75))
        popup_surf.blit(x, x_rect)
        popup_surf.blit(vitJ1, vitJ1_rect)
        popup_surf.blit(vitJ2, vitJ2_rect)

        popup_surf.set_alpha(190)

        botao_base = pygame.image.load('./assets/botao.png')
        botao_base1 = pygame.transform.scale(botao_base, (100, 50))
        botao_base2 = pygame.transform.scale(botao_base, (130, 50))

        botao_voltar = Button(botao_base1, popup_x + largura_popup // 2 - 100, popup_y + altura_popup - 50, 'menu', janela, fonte)
        botao_jogarnov = Button(botao_base2, popup_x + largura_popup // 2 + 85, popup_y + altura_popup - 50, 'revanche', janela, fonte)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botao_voltar.checarInput(pygame.mouse.get_pos()):
                        return menu_principal()
                    
                    if botao_jogarnov.checarInput(pygame.mouse.get_pos()):
                        return play(vitoriasJ1, vitoriasJ2)

            janela.blit(popup_surf, (popup_x, popup_y))

            botao_voltar.update()
            botao_voltar.hover(pygame.mouse.get_pos())

            botao_jogarnov.update()
            botao_jogarnov.hover(pygame.mouse.get_pos())

            pygame.display.update()

    # Função para menu de pausa
    def menuPausa(janela):
        largura_fundo = 900
        altura_fundo = 800
        janela = pygame.display.set_mode((largura_fundo, altura_fundo))

        fundo = fundo_imagem

        botao_base = pygame.image.load('./assets/botao.png')
        botao_base1 = pygame.transform.scale(botao_base, (200, 75))
        botao_base2 = pygame.transform.scale(botao_base, (200, 75))
        botao_base3 = pygame.transform.scale(botao_base, (200, 75))

        fonte = pygame.font.SysFont('comic sans', 50, bold=True)
        texto_pausado = fonte.render('pausado', True, 'white')
        texto_pausado_rect = texto_pausado.get_rect(center=(largura_fundo // 2, altura_fundo // 2 - 200))

        botao_continuar = Button(botao_base1, largura_fundo // 2, altura_fundo // 2 - 100, 'continuar', janela, fonte_padrao)
        botao_reiniciar = Button(botao_base2, largura_fundo // 2, altura_fundo // 2, 'reiniciar', janela, fonte_padrao)
        botao_voltar = Button(botao_base3, largura_fundo // 2, altura_fundo // 2 + 100, 'menu', janela, fonte_padrao)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botao_continuar.checarInput(pygame.mouse.get_pos()):
                        return True

                    if botao_reiniciar.checarInput(pygame.mouse.get_pos()):
                        return play(vitoriasJ1, vitoriasJ2)

                    if botao_voltar.checarInput(pygame.mouse.get_pos()):
                        return menu_principal()

            janela.blit(fundo, (0,0))
            janela.blit(texto_pausado, texto_pausado_rect)

            # printar pontuação
            janela.blit(vermelho, (largura_fundo // 2 - 170, 20))
            janela.blit(amarelo, (largura_fundo // 2 + 95, 20))
            vitJ1 = fonte.render(f'{vitoriasJ1}', True, 'white')
            vitJ2 = fonte.render(f'{vitoriasJ2}', True, 'white')
            vitJ1_rect = vitJ1.get_rect(center=(largura_fundo // 2 - 50, 60))
            vitJ2_rect = vitJ2.get_rect(center=(largura_fundo // 2 + 50, 60))
            x = fonte.render('x', True, 'white')
            x_rect = x.get_rect(center=(largura_fundo // 2, 60))
            janela.blit(x, x_rect)
            janela.blit(vitJ1, vitJ1_rect)
            janela.blit(vitJ2, vitJ2_rect)

            botao_continuar.update()
            botao_continuar.hover(pygame.mouse.get_pos())

            botao_reiniciar.update()
            botao_reiniciar.hover(pygame.mouse.get_pos())

            botao_voltar.update()
            botao_voltar.hover(pygame.mouse.get_pos())

            pygame.display.update()
        
        return True

    # Funções do funcionamento do jogo
    def fazerJogada(jogador, coluna, tabuleiro):
        for i in range(5, -1, -1):
            if tabuleiro[i][coluna] == 0:   
                tabuleiro[i][coluna] = jogador
                ficha_sfx.play()
                return tabuleiro, 2 if jogador == 1 else 1
        return tabuleiro, jogador

    def verificarVitoria(tabuleiro):
        linhas = len(tabuleiro)
        colunas = len(tabuleiro[0])

        for i in range(linhas):
            for j in range(colunas - 3):
                # Horizontal
                if tabuleiro[i][j] == tabuleiro[i][j+1] == tabuleiro[i][j+2] == tabuleiro[i][j+3] != 0:
                    return tabuleiro[i][j]

        for j in range(colunas):
            for i in range(linhas - 3):
                # Vertical
                if tabuleiro[i][j] == tabuleiro[i+1][j] == tabuleiro[i+2][j] == tabuleiro[i+3][j] != 0:
                    return tabuleiro[i][j]

        for i in range(linhas - 3):
            for j in range(colunas - 3):
                # Diagonal principal
                if tabuleiro[i][j] == tabuleiro[i+1][j+1] == tabuleiro[i+2][j+2] == tabuleiro[i+3][j+3] != 0:
                    return tabuleiro[i][j]

                # Diagonal secundária
                if tabuleiro[i][j+3] == tabuleiro[i+1][j+2] == tabuleiro[i+2][j+1] == tabuleiro[i+3][j] != 0:
                    return tabuleiro[i][j+3]

        tem_zero = False
        for i in range(linhas):
            for j in range(colunas):
                if tabuleiro[i][j] == 0:
                    tem_zero = True
        
        if not tem_zero:
            return 3

        return 0

    def desenharCirculos(linhas, colunas, tabuleiro):
        for i in range(linhas):
            for j in range(colunas):
                x = j * circ_largura + 100  # Ajustar a posição X
                y = i * circ_altura + 100  # Ajustar a posição Y
                cor = 'white'
                if tabuleiro[i][j] == 1:
                    cor = 'red'
                    janela.blit(vermelho, (x + 9, y + 9))
                if tabuleiro[i][j] == 2:
                    cor = 'yellow'
                    janela.blit(amarelo, (x + 9, y + 9))

                #if cor == 'white':
                    #pygame.draw.circle(janela, cor, (x + 50, y + 50), 40,)

    def circuloSuspenso(colunas):
        mouse = pygame.mouse.get_pos()
        coluna = (mouse[0] - 100) // 100
        #cor = 'white'
        if jogador == 1:
            # cor = 'red'
            cor = vermelho
        elif jogador == 2:
            # cor = 'yellow'
            cor = amarelo
        if 0 <= coluna < colunas:
            janela.blit(cor, ((coluna * 100 + 110), 7))
            #pygame.draw.circle(janela, cor, (coluna * 100 + 150, 50), 40)

    def printarMatriz(tabuleiro):
        print([1,2,3,4,5,6,7])
        for linha in tabuleiro:
            print(linha)

    click = False
    pausado = False
    jogador = random.randint(1, 2)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Pausar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausado = True

            if not pausado:
                # Obter clique
                if event.type == pygame.MOUSEBUTTONDOWN and not click:
                    click = True
                    posicao_mouse = pygame.mouse.get_pos()
                    coluna = (posicao_mouse[0] - 100) // circ_largura  # posição da coluna
                    if 0 <= coluna < colunas:
                        tabuleiro, jogador = fazerJogada(jogador, coluna, tabuleiro)
                        vitoria = verificarVitoria(tabuleiro)
                        if vitoria != 0:
                            desenharCirculos(linhas, colunas, tabuleiro)
                            if vitoria == 1:
                                vitoriasJ1 += 1
                            elif vitoria == 2:
                                vitoriasJ2 += 1
                            run = desenharPopupVitoria(janela, vitoria)
                        printarMatriz(tabuleiro)

                if event.type == pygame.MOUSEBUTTONUP:
                    click = False

        if pausado:
            run = menuPausa(janela)
            pausado = False

        if not pausado: 
            # Texto
            texto_jogador = fonte.render(f'jogador {jogador}', True, 'black')
            texto_jrect = texto_jogador.get_rect(center=(450, 730))

            # Desenhar fundo
            janela.blit(fundo_imagem, (0, 0))
            janela.blit(esqueleto, (0,0))
            janela.blit(texto_jogador, texto_jrect)

            # Desenhar os círculos
            desenharCirculos(linhas, colunas, tabuleiro)

            # Desenhar o círculo suspenso, para mostrar a coluna que o jogador vai jogar
            circuloSuspenso(colunas)

        pygame.display.update()
        clock.tick(60)

    return True

# Loop principal
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    main()

pygame.quit()