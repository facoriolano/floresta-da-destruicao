import json
from combate import combate
from inventario import adicionar_item, comer_provisao, mostrar_inventario
from sorte import testar_sorte
from salvar import salvar_jogo

def carregar_historia():
    with open("historia.json", "r", encoding="utf-8") as f:
        return json.load(f)

def iniciar_jogo(personagem, historia, paragrafo="1"):
    while paragrafo in historia:
        conteudo = historia[paragrafo]
        print(f"\n[{paragrafo}] {conteudo['texto']}\n")

        if "combate" in conteudo:
            inimigo = conteudo["combate"]
            resultado = combate(personagem, inimigo)
            if not resultado:
                print("Fim de jogo.")
                return

        if "ganhar_item" in conteudo:
            adicionar_item(personagem, conteudo["ganhar_item"])

        if "comer" in conteudo and conteudo["comer"]:
            comer_provisao(personagem)

        if "teste_sorte" in conteudo and conteudo["teste_sorte"]:
            if testar_sorte(personagem):
                paragrafo = conteudo["se_sorte"]
            else:
                paragrafo = conteudo["se_azar"]
            continue

        mostrar_inventario(personagem)

        if "escolhas" in conteudo:
            opcoes = list(conteudo["escolhas"].items())
            for i, (opcao, destino) in enumerate(opcoes, 1):
                print(f"{i}. {opcao}")
            print(f"{len(opcoes)+1}. Salvar e sair")
            escolha = int(input("Escolha: ")) - 1

            if escolha == len(opcoes):
                salvar_jogo(personagem, paragrafo)
                return
            else:
                paragrafo = opcoes[escolha][1]
        else:
            break
