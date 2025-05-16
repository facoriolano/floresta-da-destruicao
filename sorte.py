import random

def testar_sorte(personagem):
    dado = random.randint(2, 12)
    print(f"\n🎲 Você rola os dados e tira: {dado}")
    if dado <= personagem["sorte"]:
        print("🍀 Você teve SORTE!")
        resultado = True
    else:
        print("💀 Você NÃO teve sorte.")
        resultado = False

    personagem["sorte"] -= 1
    print(f"Sorte restante: {personagem['sorte']}")
    return resultado
