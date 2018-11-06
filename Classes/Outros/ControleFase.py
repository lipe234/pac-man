from Classes.Outros.GameComponent import GameComponent, estado, direcao
from Classes.Personagens.Pacman import Pacman
from Classes.Personagens.Blinky import Blinky
from Classes.Personagens.Pinky import Pinky
from Classes.Personagens.Inky import Inky
from Classes.Personagens.Clyde import Clyde

class ControleFase(GameComponent):
    """ Realiza o controle da pontuação e das vidas. """
    def __init__(self, posicao: list, controle_fase=None, fase_atual=None):
        # referencia para a fase atual
        self.fase_atual = fase_atual

        # construtor base
        super().__init__(posicao, "Nenhum", None, True)

        # controle de fim de fase
        self.fim_fase = False

        if controle_fase is None:
            # pontuacao e vidas da fase.
            self.pontuacao = 0
            self.vidas = 3

        else:
            # pontuacao e vidas da fase.
            self.pontuacao = controle_fase.pontuacao
            self.vidas = controle_fase.vidas      



    def sistema_itens_pontuacao(self, elementos_fase):
        # apelido dos eixos 
        x, y = 0, 1

        # ordena os pacdots pela proximidade
        elementos_fase.pacdots.sort(key=lambda elemento: abs(elemento.movimento.posicao[x] - self.movimento.posicao[x]) +\
                                                                      abs(elemento.movimento.posicao[y] - self.movimento.posicao[y]))

        # verifica se pacman colidiu com algum objeto (itens, pacdots e powerpills)
        # se colidiu, incrementa a pontuacao e exclui o item
        # copy() serve para iterar uma cópia da lista, pois não posso iterar e alterar a própria lista
        if elementos_fase.item is not None and elementos_fase.pacman.bounding_box().colliderect(elementos_fase.item.bounding_box()):

            # incrementa pontuacao
            self.pontuacao += elementos_fase.item.pontuacao

            # exclui o item
            elementos_fase.item = None

            # toca a musica de comer item
            elementos_fase.fase_atual.sons.pacman_eatfruit.play()
        
        for pacdot in elementos_fase.pacdots.copy():
            if elementos_fase.pacman.bounding_box().colliderect(pacdot.bounding_box()):

                # incrementa pontuacao
                self.pontuacao += pacdot.pontuacao

                # exclui a pacdot
                elementos_fase.pacdots.remove(pacdot)

                # ativa o audio do pacman comendo uma pacdot
                elementos_fase.fase_atual.sons.pacman_chomp.play()

                # sai do laço
                break
        
        # se o pacman colidiu com uma powerpill, incrementa a pontuacao e muda o estado dos fantasmas
        for powerpill in elementos_fase.powerpills.copy():
            if elementos_fase.pacman.bounding_box().colliderect(powerpill.bounding_box()):

                # incrementa pontuacao
                self.pontuacao += powerpill.pontuacao

                # muda o estado dos fantasmas
                elementos_fase.blinky.movimento.estado = estado.modo_fuga
                elementos_fase.pinky.movimento.estado = estado.modo_fuga
                elementos_fase.inky.movimento.estado = estado.modo_fuga
                elementos_fase.clyde.movimento.estado = estado.modo_fuga

                # exclui a powerpill
                elementos_fase.powerpills.remove(powerpill)

                # ativa o audio de modo fuga dos fantasmas
                elementos_fase.fase_atual.sons.ghost_frightened.play()

                # sai do laço
                break

        # se acabou os pacdots, insere a chave para passar de fase
        if not elementos_fase.pacdots and elementos_fase.chave is None:
            elementos_fase.chave = Chave(elementos_fase.posicao_chave)

        # se pacman colidir com uma chave, ele passa de fase e incrementa pontuacao
        if elementos_fase.chave is not None and elementos_fase.pacman.bounding_box().colliderect(elementos_fase.chave.bounding_box()):
            self.pontuacao += elementos_fase.chave.pontuacao
            self.fim_fase = True
            elementos_fase.chave = None
            
            # toca a musica de comer item
            elementos_fase.fase_atual.sons.pacman_eatfruit.play()

        # se pontuacao for igual a 20000 pontos, ganha uma vida extra
        if self.pontuacao == 20000: 
            self.vida += 1

            # toca a musica de vida extra
            elementos_fase.fase_atual.sons.pacman_extrapac.play()


    def sistema_colisao_fantasmas(self, elementos_fase):
        # testa se pacman colidiu com cada fantasma, se ele nao estiver morto ou morrendo.
        if elementos_fase.pacman.movimento.estado not in [estado.morrendo, estado.morto]:

            # se houve colisao
            if elementos_fase.pacman.bounding_box().colliderect(elementos_fase.blinky.bounding_box()):

                # se o fantasma estiver em modo fuga, come ele, incrementa pontuacao e muda o estado dele para morto
                if elementos_fase.blinky.movimento.estado == estado.modo_fuga:
                    self.pontuacao += elementos_fase.blinky.pontuacao
                    elementos_fase.blinky.movimento.estado = estado.morto

                # se ele nao estiver morto, pacman morre
                elif elementos_fase.blinky.movimento.estado != estado.morto:
                    elementos_fase.pacman.movimento.estado = estado.morrendo
                    self.vidas -= 1

            elif elementos_fase.pacman.bounding_box().colliderect(elementos_fase.pinky.bounding_box()):
                if elementos_fase.pinky.movimento.estado == estado.modo_fuga:
                    self.pontuacao += elementos_fase.pinky.pontuacao
                    elementos_fase.pinky.movimento.estado = estado.morto
                elif elementos_fase.pinky.movimento.estado != estado.morto:
                    elementos_fase.pacman.movimento.estado = estado.morrendo
                    self.vidas -= 1

            elif elementos_fase.pacman.bounding_box().colliderect(elementos_fase.inky.bounding_box()):
                if elementos_fase.inky.movimento.estado == estado.modo_fuga:
                    self.pontuacao += elementos_fase.inky.pontuacao
                    elementos_fase.inky.movimento.estado = estado.morto
                elif elementos_fase.inky.movimento.estado != estado.morto:
                    elementos_fase.pacman.movimento.estado = estado.morrendo
                    self.vidas -= 1

            elif elementos_fase.pacman.bounding_box().colliderect(elementos_fase.clyde.bounding_box()):
                if elementos_fase.clyde.movimento.estado == estado.modo_fuga:
                    self.pontuacao += elementos_fase.clyde.pontuacao
                    elementos_fase.clyde.movimento.estado = estado.morto
                elif elementos_fase.clyde.movimento.estado != estado.morto:
                    elementos_fase.pacman.movimento.estado = estado.morrendo
                    self.vidas -= 1

            # se pacman estiver morrendo, toca a música de morte do pacman
            if elementos_fase.pacman.movimento.estado == estado.morrendo:
                elementos_fase.fase_atual.sons.pacman_death.play()

            # se algum fantasma estiver morto, toca a música de morte dos fantasmas
            if elementos_fase.blinky.movimento.estado == estado.morto or \
                elementos_fase.pinky.movimento.estado == estado.morto or \
                elementos_fase.inky.movimento.estado == estado.morto or \
                elementos_fase.clyde.movimento.estado == estado.morto:
                elementos_fase.fase_atual.sons.ghost_return_to_home.play()
                

    def atualiza_sprite_frame(self, sprite_objeto):
        # apelido dos eixos
        x, y = 0, 1

        if type(sprite_objeto.game_component) is Pacman:
            # se parado, fica travado em sprite frame específico
            if sprite_objeto.game_component.movimento.estado == estado.parado:
                sprite_objeto.game_component.sprite.sprite_frame = [1, sprite_objeto.game_component.movimento.direcao_atual]

            # se andando, itera uma linha do sprite sheet, com os sprite frames da direcao escolhida.
            elif sprite_objeto.game_component.movimento.estado == estado.andando:
                if sprite_objeto.game_component.sprite.sprite_frame[x] == 2:
                    sprite_objeto.game_component.sprite.sprite_frame = [0, sprite_objeto.game_component.movimento.direcao_atual]
                else:
                    sprite_objeto.game_component.sprite.sprite_frame = [sprite_objeto.game_component.sprite.sprite_frame[x]+1, sprite_objeto.game_component.movimento.direcao_atual]
            
            # se morreu, realiza a animação de morte
            elif sprite_objeto.game_component.movimento.estado == estado.morrendo:
                if sprite_objeto.game_component.sprite.sprite_frame[x] == 10:
                    sprite_objeto.game_component.sprite.sprite_frame = [9, 4]
                    sprite_objeto.game_component.movimento.estado = estado.morto
                else:
                    sprite_objeto.game_component.sprite.sprite_frame = [sprite_objeto.game_component.sprite.sprite_frame[x]+1, 4]

                return

        if type(sprite_objeto.game_component) in [Blinky, Pinky, Inky, Clyde]:
            # se parado, fica travado em sprite frame específico
            if sprite_objeto.game_component.movimento.estado == estado.parado:
                sprite_objeto.game_component.sprite.sprite_frame = [0, sprite_objeto.game_component.movimento.direcao_atual]

            # se andando, itera uma linha do sprite sheet, com os sprite frames da direcao escolhida.
            elif sprite_objeto.game_component.movimento.estado == estado.andando:
                if sprite_objeto.game_component.sprite.sprite_frame[x] == 1:
                    sprite_objeto.game_component.sprite.sprite_frame = [0, sprite_objeto.game_component.movimento.estado]
                else:
                    sprite_objeto.game_component.sprite.sprite_frame = [sprite_objeto.game_component.sprite.sprite_frame[x]+1, sprite_objeto.game_component.movimento.estado]

            # se modo fuga (quando pacman come uma powerpill), itera uma linha do sprite sheet, com os sprite frames.
            elif sprite_objeto.game_component.movimento.estado == estado.modo_fuga:
                if sprite_objeto.game_component.sprite.sprite_frame[x] == 3:
                    sprite_objeto.game_component.sprite.sprite_frame = [0, 4]
                else:
                    sprite_objeto.game_component.sprite.sprite_frame = [sprite_objeto.game_component.sprite.sprite_frame[x]+1, 4]

            # se morreu, realiza a animação de morte
            elif sprite_objeto.game_component.movimento.estado == estado.morto:
                if sprite_objeto.game_component.movimento.direcao_atual == direcao.cima:
                    sprite_objeto.game_component.sprite.sprite_frame = [2, 5]

                elif sprite_objeto.game_component.movimento.direcao_atual == direcao.baixo:
                    sprite_objeto.game_component.sprite.sprite_frame = [3, 5]

                elif sprite_objeto.game_component.movimento.direcao_atual == direcao.esquerda:
                    sprite_objeto.game_component.sprite.sprite_frame = [1, 5]

                elif sprite_objeto.game_component.movimento.direcao_atual == direcao.direita:
                    sprite_objeto.game_component.sprite.sprite_frame = [0, 5]


    def resetar_posicoes_personagens(self, elementos_fase):
        elementos_fase.pacman.resetar(elementos_fase.posicao_inicial_pacman)
        elementos_fase.blinky.resetar(elementos_fase.posicao_inicial_blinky)
        elementos_fase.pinky.resetar(elementos_fase.posicao_inicial_pinky)
        elementos_fase.inky.resetar(elementos_fase.posicao_inicial_inky)
        elementos_fase.clyde.resetar(elementos_fase.posicao_inicial_clyde)