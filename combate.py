import random

def rolar_dados(qtd=2):
    return sum(random.randint(1, 6) for _ in range(qtd))

def testar_sorte(personagem):
    rolagem = rolar_dados()
    sucesso = rolagem <= personagem["sorte"]
    personagem["sorte"] = max(0, personagem["sorte"] - 1)
    print(f"Teste de sorte: rolou {rolagem} → {'SUCESSO' if sucesso else 'FALHA'}")
    return sucesso

def combate(personagem, inimigo):
    print(f"\n⚔️ Você entra em combate com {inimigo['nome']}!")
    while personagem["energia"] > 0 and inimigo["energia"] > 0:
        input("\nPressione Enter para rolar os dados...")

        ataque_jogador = rolar_dados() + personagem["habilidade"]
        ataque_inimigo = rolar_dados() + inimigo["habilidade"]

        print(f"Você: {ataque_jogador}  |  {inimigo['nome']}: {ataque_inimigo}")

        if ataque_jogador > ataque_inimigo:
            print(f"Você acerta {inimigo['nome']}!")
            dano = 2
            if usar_sorte():
                if testar_sorte(personagem):
                    dano = 4
                else:
                    dano = 1
            inimigo["energia"] -= dano
            print(f"{inimigo['nome']} perde {dano} de energia.")
        elif ataque_inimigo > ataque_jogador:
            print(f"{inimigo['nome']} acerta você!")
            dano = 2
            if usar_sorte():
                if not testar_sorte(personagem):
                    dano = 3
                else:
                    dano = 1
            personagem["energia"] -= dano
            print(f"Você perde {dano} de energia.")
        else:
            print("Empate! Ninguém acerta.")

        print(f"Você: {personagem['energia']} de energia | {inimigo['nome']}: {inimigo['energia']} de energia")

    if personagem["energia"] <= 0:
        print("\n💀 Você foi derrotado...")
        return False
    else:
        print(f"\n✅ Você derrotou {inimigo['nome']}!")
        return True

def usar_sorte():
    escolha = input("Quer testar a SORTE? (s/n): ").lower()
    return escolha == "s"
