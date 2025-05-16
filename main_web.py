from combate_web import combate
import json
from pyodide.ffi import create_proxy
from js import document

# Carrega história
with open("historia.json", "r", encoding="utf-8") as f:
    historia = json.load(f)

output = document.getElementById("output")
entrada = document.getElementById("entrada")

personagem = {
    "nome": "Aventureiro",
    "habilidade": 10,
    "energia": 20,
    "sorte": 10,
    "provisoes": 5,
    "mochila": []
}

paragrafo_atual = "1"
esperando_entrada = False
opcoes_disponiveis = []

def exibir(texto):
    output.innerText += "\n" + texto

def mudar_paragrafo(novo):
    global paragrafo_atual
    paragrafo_atual = novo
    mostrar_paragrafo()

def adicionar_item(personagem, item):
    personagem["mochila"].append(item)
    exibir(f"📦 Você ganhou: {item}")

def comer_provisao(personagem):
    if personagem["provisoes"] > 0:
        personagem["energia"] += 4
        personagem["provisoes"] -= 1
        exibir("🍞 Você comeu uma provisão (+4 energia).")
    else:
        exibir("❌ Você não tem provisões.")

def testar_sorte(personagem):
    from random import randint
    dado = randint(2, 12)
    exibir(f"🎲 Teste de sorte! Você tirou {dado}")
    personagem["sorte"] -= 1
    if dado <= personagem["sorte"]:
        exibir("🍀 Sorte! Você ganhou o teste.")
        return True
    else:
        exibir("💀 Azar! Você perdeu o teste.")
        return False

def mostrar_paragrafo():
    global esperando_entrada, opcoes_disponiveis
    esperando_entrada = False
    output.innerText = ""  # Limpa a tela a cada parágrafo
    conteudo = historia.get(paragrafo_atual)
    if not conteudo:
        exibir("Fim da aventura.")
        return

    exibir(f"\n[{paragrafo_atual}] {conteudo['texto']}")

    # Itens
    if "ganhar_item" in conteudo:
        adicionar_item(personagem, conteudo["ganhar_item"])

    # Provisões
    if "comer" in conteudo and conteudo["comer"]:
        comer_provisao(personagem)

    # Teste de sorte
    if "teste_sorte" in conteudo and conteudo["teste_sorte"]:
        if testar_sorte(personagem):
            mudar_paragrafo(conteudo["se_sorte"])
        else:
            mudar_paragrafo(conteudo["se_azar"])
        return

    # Combate
    if "combate" in conteudo:
        inimigo = conteudo["combate"]
        resultado = combate(personagem, inimigo)
        if not resultado:
            exibir("💀 Você perdeu o combate e morreu. Fim de jogo.")
            esperando_entrada = False
            return

    # Opções de escolha
    if "escolhas" in conteudo:
        opcoes_disponiveis = list(conteudo["escolhas"].items())
        for i, (texto, _) in enumerate(opcoes_disponiveis, 1):
            exibir(f"{i}. {texto}")
        esperando_entrada = True
    else:
        exibir("🔚 Fim do caminho.")

def processar_entrada(evt):
    global esperando_entrada
    if not esperando_entrada:
        return

    valor = entrada.value.strip()
    entrada.value = ""

    if valor.isdigit():
        escolha = int(valor) - 1
        if 0 <= escolha < len(opcoes_disponiveis):
            _, destino = opcoes_disponiveis[escolha]
            mudar_paragrafo(destino)

entrada.addEventListener("keypress", create_proxy(lambda e: processar_entrada(e) if e.key == "Enter" else None))

mostrar_paragrafo()
