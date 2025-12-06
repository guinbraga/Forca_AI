import random
from collections import Counter


class AgenteForca:
    def __init__(self, banco_conhecimento, temperatura):
        self.aprendizado = banco_conhecimento
        self.letras_tentadas = set()
        self.letras_erradas = set()
        self.padrao_atual = []  # Ex: ['C', '_', 'S', 'A']
        self.candidatos = []  # Palavras possíveis baseadas no filtro atual
        self.temperatura = temperatura

    def perceber_ambiente(self, tamanho_palavra, letras_reveladas, letras_erradas_jogo):
        # Coleta informações do estado atual do jogo
        self.padrao_atual = letras_reveladas
        self.letras_erradas = set(letras_erradas_jogo)
        self.letras_tentadas = set(letras_reveladas).union(self.letras_erradas) - {'_'}

        # Filtra candidatos do banco de conhecimento que batem com o tamanho e letras reveladas
        todas_palavras = self.aprendizado.palavras
        self.candidatos = [
            palavr for palavr in todas_palavras
            if len(palavr) == tamanho_palavra and self.bater_padrao(palavr, self.padrao_atual)
        ]

        # Filtra palavras que contêm letras que já sabemos que estão erradas
        self.candidatos = [
            p for p in self.candidatos
            if not any(l in p for l in self.letras_erradas)
        ]

    def bater_padrao(self, palavra, padrao):
        # Verifica se a palavra candidata encaixa no padrão visual atual.
        for i, char in enumerate(padrao):
            if char != '_' and char != palavra[i]:
                return False
        return True

    def tomar_decisao(self):
        # Decide se chuta uma letra ou a palavra inteira.

        # Se só sobrou 1 candidato lógico, o agente arrisca a palavra inteira (Autonomia)
        if len(self.candidatos) == 1:
            return "PALAVRA", self.candidatos[0]

        # Se não há candidatos conhecidos, chuta vogais ou consoantes comuns (Fallback)
        if not self.candidatos:
            comuns = "AEOSRINDMU"
            for letra in comuns:
                if letra not in self.letras_tentadas:
                    return "LETRA", letra
            # Se tudo falhar, aleatório
            alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            escolha = random.choice([l for l in alfabeto if l not in self.letras_tentadas])
            return "LETRA", escolha

        # Estratégia de Frequência: Analisa qual letra aparece mais vezes nos candidatos restantes
        contador = Counter()
        for palavra in self.candidatos:
            for letra in set(palavra):  # set para contar apenas presença na palavra
                if letra not in self.letras_tentadas:
                    contador[letra] += 1

        # ordenamos as letras possíveis por contagem e depois alfabeticamente
        opcoes_ordenadas = sorted(contador.items(), key=lambda x: (-x[1], x[0]))

        # extraímos somente as letras
        letras_rankeadas = [item[0] for item in opcoes_ordenadas]

        probabilidade = random.random()
        limite = self.temperatura
        indice_escolhido = 0


        while probabilidade < limite:
            #verificamos se ainda há letras candidatas, não deixamos o índice passar
            if indice_escolhido < len(letras_rankeadas) - 1:
                indice_escolhido += 1
                limite = limite / 2.0
            else:
                break

        return "LETRA", letras_rankeadas[indice_escolhido]