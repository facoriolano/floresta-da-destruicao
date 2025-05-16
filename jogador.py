import random

def criar_personagem():
    print("Criação do personagem...")
    habilidade = random.randint(1, 6) + 6
    energia = random.randint(2, 6) + 12
    sorte = random.randint(1, 6) + 6

    personagem = {
        "habilidade": habilidade,
        "energia": energia,
        "sorte": sorte,
        "mochila": [],
    }

    print(f"Habilidade: {habilidade}")
    print(f"Energia: {energia}")
    print(f"Sorte: {sorte}")
    return personagem
