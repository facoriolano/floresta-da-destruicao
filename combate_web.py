from random import randint
from js import console

def rolar_dado():
    return randint(1, 6) + randint(1, 6)

def combate(personagem, inimigo):
    console.log(f"⚔️ Começa combate contra {inimigo['nome']}")

    habilidade_personagem = personagem["habilidade"] + rolar_dado()
    habilidade_inimigo = inimigo["habilidade"] + rolar_dado()

    if habilidade_personagem > habilidade_inimigo:
        personagem["energia"] -= inimigo["forca"]
        print(f"Você ganhou! Energia atual: {personagem['energia']}")
        return personagem["energia"] > 0
    else:
        personagem["energia"] -= inimigo["forca"]
        print(f"Você perdeu! Energia atual: {personagem['energia']}")
        return personagem["energia"] > 0
