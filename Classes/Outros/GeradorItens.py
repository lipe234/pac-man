from Classes.Fase import *
from Classes.Outros.Objeto import *
from Classes.Outros.ElementosFase import *
from random import shuffle, choice

class GeradorItens(object):
    """ Sorteia itens que aparecerão de tempos em tempos. """

    def __init__(self):
        # defino a quantidade e tipo de fichas de itens
        self.num_fichas  = [512, 64, 32, 16, 8, 4, 2, 1]
        self.tipo_fichas = ["nenhum", "cherry", "strawberry", "orange", "apple", "melon", "galaxy boss", "bell"]


    def sortear(self, elementos_fase: ElementosFase):
        # crio uma lista de fichas
        for num_fichas, tipo_ficha in zip(self.num_fichas, self.tipo_fichas):
            fichas += [tipo_ficha] * num_fichas

        # embaralha e sorteia uma ficha
        shuffle(fichas)
        tipo_item = choice(fichas)

        # crio o item sorteado
        if tipo_item != "nenhum": elementos_fase.item = Objeto(self.posicao_itens, tipo_item)