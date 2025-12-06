import json
import os
import random
import unicodedata
from collections import Counter

# SEÇÃO 1: CONFIGURAÇÃO E PERSISTÊNCIA DE DADOS

class BancoDeConhecimento:
    def __init__(self, arquivo='conhecimento.json'):
        self.arquivo = arquivo
        self.palavras = self.carregar_conhecimento()

    def carregar_conhecimento(self):
        # Carrega palavras do arquivo ou inicia com um conjunto básico pré-definido.
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except:
                return self.iniciar_padrao()
        else:
            return self.iniciar_padrao()

    def iniciar_padrao(self):
        padrao = ["COMPUTADOR", "ALGORITMO", "INTELIGENCIA", "PYTHON", "PROGRAMACAO", "UEL", "LONDRINA"]
        self.salvar_conhecimento(padrao)
        return padrao

    def salvar_conhecimento(self, dados=None):
        """Persiste o conhecimento no disco."""
        if dados is not None:
            self.palavras = dados
        
        # Remove duplicatas e normaliza
        self.palavras = list(set([p.upper() for p in self.palavras]))
        
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.palavras, f, ensure_ascii=False, indent=4)

    def aprender_palavra(self, nova_palavra):
        # Adiciona nova palavra ao banco de dados
        nova_palavra = nova_palavra.upper().strip()
        if nova_palavra and nova_palavra not in self.palavras:
            self.palavras.append(nova_palavra)
            self.salvar_conhecimento()
            return True
        return False

# SEÇÃO 2: O AGENTE INTELIGENTE

class AgenteForca:
    def __init__(self, banco_conhecimento):
        self.aprendizado = banco_conhecimento
        self.letras_tentadas = set()
        self.letras_erradas = set()
        self.padrao_atual = [] # Ex: ['C', '_', 'S', 'A']
        self.candidatos = []   # Palavras possíveis baseadas no filtro atual

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
            for letra in set(palavra): # set para contar apenas presença na palavra
                if letra not in self.letras_tentadas:
                    contador[letra] += 1
        
        if not contador:
            return "LETRA", random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") # Fallback raro

        melhor_letra = contador.most_common(1)[0][0]
        return "LETRA", melhor_letra

# SEÇÃO 3: MOTOR DO JOGO E VISUALIZAÇÃO

class JogoForca:
    def __init__(self):
        self.aprendizado = BancoDeConhecimento()
        self.agente = AgenteForca(self.aprendizado)
        self.palavra_secreta = ""
        self.tentativas_restantes = 6
        self.estado_visual = []
        self.letras_erradas = []

    def normalizar(self, texto):
        # Remove acentos para simplificar a comparação.
        return ''.join(c for c in unicodedata.normalize('NFD', texto)
                      if unicodedata.category(c) != 'Mn').upper()

    def exibir_forca(self):
        """Apresentação visual da evolução."""
        estagios = [  # ASCII Art
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / \\
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / 
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |      
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|
               |      |
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |      |
               |      |
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |    
               |      
               |     
               -
            """,
            """
               --------
               |      |
               |      
               |    
               |      
               |     
               -
            """
        ]
        
        print("\n" + "="*40)
        print(estagios[self.tentativas_restantes])
        print(f"Tentativas restantes: {self.tentativas_restantes}")
        print(f"Palavra: {' '.join(self.estado_visual)}")
        print(f"Erros: {', '.join(self.letras_erradas)}")
        print("="*40 + "\n")

    def jogar(self):
        print(">>> JOGO DA FORCA - AGENTE INTELIGENTE UEL <<<")
        entrada = input("Digite a palavra secreta para o Agente tentar adivinhar: ")
        self.palavra_secreta = self.normalizar(entrada.strip())
        
        if not self.palavra_secreta:
            print("Palavra inválida.")
            return

        # Inicializa estado
        self.estado_visual = ['_' for _ in self.palavra_secreta]
        self.tentativas_restantes = 6
        self.letras_erradas = []
        
        os.system('cls' if os.name == 'nt' else 'clear') # Limpa tela para esconder a palavra

        # Loop principal do jogo
        while self.tentativas_restantes > 0 and '_' in self.estado_visual:
            self.exibir_forca()
            
            # 1. Agente percebe o ambiente
            self.agente.perceber_ambiente(len(self.palavra_secreta), self.estado_visual, self.letras_erradas)
            
            # 2. Agente decide
            tipo, valor = self.agente.tomar_decisao()
            
            print(f"Agente decidiu: {tipo} -> {valor}")
            
            # 3. Processa a jogada
            if tipo == "PALAVRA":
                if valor == self.palavra_secreta:
                    self.estado_visual = list(self.palavra_secreta) # Ganhou
                else:
                    self.tentativas_restantes = 0 # Perdeu direto ao arriscar tudo
            
            else: # Tipo LETRA
                if valor in self.palavra_secreta:
                    print(f"-> O agente ACERTOU a letra '{valor}'!")
                    for i, letra in enumerate(self.palavra_secreta):
                        if letra == valor:
                            self.estado_visual[i] = valor
                else:
                    print(f"-> O agente ERROU a letra '{valor}'...")
                    self.letras_erradas.append(valor)
                    self.tentativas_restantes -= 1
            
            # Pausa breve para visualização
            import time; time.sleep(1.5)

        # Finalização e Aprendizado 
        self.exibir_forca()
        if '_' not in self.estado_visual:
            print(f"O AGENTE VENCEU! A palavra era: {self.palavra_secreta}")
            # Mesmo ganhando, verifica se é palavra nova para garantir consistência
            if self.aprendizado.aprender_palavra(self.palavra_secreta):
                print(f"[Aprendizado] A palavra '{self.palavra_secreta}' foi aprendida.")
        else:
            print(f"GAME OVER. O agente perdeu. A palavra era: {self.palavra_secreta}")
            # Aprendizado Crítico: Aprende a palavra que não sabia
            if self.aprendizado.aprender_palavra(self.palavra_secreta):
                print(f"[Aprendizado] O agente aprendeu a palavra '{self.palavra_secreta}' para a próxima vez!")
            else:
                print("[Memória] O agente já conhecia a palavra, mas falhou na estratégia.")

# SEÇÃO 4: EXECUÇÃO PRINCIPAL

if __name__ == "__main__":
    game = JogoForca()
    game.jogar()