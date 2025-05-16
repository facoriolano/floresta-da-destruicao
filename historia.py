import json
from combate import combate

def carregar_historia():
    with open("historia.json", "r", encoding="utf-8") as f:
        return json.load(f)

def iniciar_jogo(personagem, historia):
    paragrafo = "1"
    while paragrafo in historia:
        conteudo = historia[paragrafo]
        print(f"\n[{paragrafo}] {conteudo['texto']}\n")

        if "combate" in conteudo:
            inimigo = conteudo["combate"]
            resultado = combate(personagem, inimigo)
            if not resultado:
                print("Fim de jogo.")
                return

        if "escolhas" in conteudo:
            for i, (opcao, destino) in enumerate(conteudo["escolhas"].items(), 1):
                print(f"{i}. {opcao}")
            escolha = int(input("Escolha: ")) - 1
            paragrafo = list(conteudo["escolhas"].values())[escolha]
        else:
            break
