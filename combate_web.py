from random import randint
from js import console

def rolar_dado():
    return randint(1, 6) + randint(1, 6)

def combate(personagem, inimigo, exibir=None):
    # exibir é uma função para mostrar texto na tela (do main_web.py)
    console.log(f"⚔️ Começa combate contra {inimigo['nome']}")

    habilidade_personagem = personagem["habilidade"] + rolar_dado()
    habilidade_inimigo = inimigo["habilidade"] + rolar_dado()

    if exibir:
        exibir(f"⚔️ Seu valor de combate: {habilidade_personagem}")
        exibir(f"⚔️ Valor de combate do inimigo {inimigo['nome']}: {habilidade_inimigo}")

    if habilidade_personagem > habilidade_inimigo:
        personagem["energia"] -= inimigo["forca"]
        if exibir:
            exibir(f"🏆 Você ganhou o combate! Energia restante: {personagem['energia']}")
        return personagem["energia"] > 0
    else:
        personagem["energia"] -= inimigo["forca"]
        if exibir:
            exibir(f"💥 Você perdeu o combate! Energia restante: {personagem['energia']}")
        return personagem["energia"] > 0
