import random

def rolar_dado():
    return random.randint(1, 6)

def criar_personagem():
    personagem = {
        "habilidade": rolar_dado() + 6,
        "energia": rolar_dado() + rolar_dado() + 12,
        "sorte": rolar_dado() + 6,
        "provisoes": 5,
        "itens": []
    }

    print("🎲 Seu personagem:")
    print(f"Habilidade: {personagem['habilidade']}")
    print(f"energia: {personagem['energia']}")
    print(f"Sorte: {personagem['sorte']}")
    print(f"Provisões: {personagem['provisoes']}")
    return personagem
