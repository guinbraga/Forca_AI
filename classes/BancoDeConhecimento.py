import json
import os


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