import json
import unicodedata
with open("lexico.txt", "r", encoding="utf-8") as arquivo:
    palavras_normalizadas = []
    for linha in arquivo:
        palavra_bruta = linha.strip().upper()
        palavra_separada_acentos = unicodedata.normalize('NFD', palavra_bruta)
        palavra_limpa = "".join([c for c in palavra_separada_acentos if not unicodedata.category(c) == 'Mn'])
        palavras_normalizadas.append(palavra_limpa)
    set_palavras_normalizadas = list(set(palavras_normalizadas)) # Remove duplicatas
    with open("conhecimento.json", "w", encoding="utf-8") as conhecimento:
        json.dump(set_palavras_normalizadas, conhecimento, ensure_ascii=False, indent=4)
