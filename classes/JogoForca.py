import os
import unicodedata

from classes.AgenteForca import AgenteForca
from classes.BancoDeConhecimento import BancoDeConhecimento


class JogoForca:
    def __init__(self, temperatura):
        self.aprendizado = BancoDeConhecimento()
        self.agente = AgenteForca(self.aprendizado, temperatura=temperatura)
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

        print("\n" + "=" * 40)
        print(estagios[self.tentativas_restantes])
        print(f"Tentativas restantes: {self.tentativas_restantes}")
        print(f"Palavra: {' '.join(self.estado_visual)}")
        print(f"Erros: {', '.join(self.letras_erradas)}")
        print("=" * 40 + "\n")

    def jogar(self):
        print(">>> JOGO DA FORCA - AGENTE INTELIGENTE UEL <<<")

        entrada = input("Digite a palavra secreta para o Agente tentar adivinhar: ")
        while not entrada.isalpha():
            entrada = input("Digite uma palavra secreta válida para o Agente tentar adivinhar: ")
        self.palavra_secreta = self.normalizar(entrada.strip())

        temperatura = input("Escolha a temperatura do agente, de 0 a 10: ")
        while (not temperatura.isnumeric()) or float(temperatura) < 0 or float(temperatura) > 10 :
            temperatura = input("Digite um número válido para a temperatura (0 a 10): ")

        self.agente.temperatura = float(temperatura)/10


        if not self.palavra_secreta:
            print("Palavra inválida.")
            return

        # Inicializa estado
        self.estado_visual = ['_' for _ in self.palavra_secreta]
        self.tentativas_restantes = 6
        self.letras_erradas = []

        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa tela para esconder a palavra

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
                    self.estado_visual = list(self.palavra_secreta)  # Ganhou
                else:
                    self.tentativas_restantes = 0  # Perdeu direto ao arriscar tudo

            else:  # Tipo LETRA
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
            import time;
            time.sleep(1.5)

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