import json

def salvar_jogo(personagem, paragrafo):
    dados = {
        "personagem": personagem,
        "paragrafo": paragrafo
    }
    with open("savegame.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)
    print("💾 Jogo salvo com sucesso.")

def carregar_jogo():
    try:
        with open("savegame.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            print("🔄 Jogo carregado com sucesso.")
            return dados["personagem"], dados["paragrafo"]
    except FileNotFoundError:
        print("🚫 Nenhum jogo salvo encontrado.")
        return None, None
