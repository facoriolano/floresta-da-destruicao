from combate_web import combate
import json
from pyodide.ffi import create_proxy
from js import document, localStorage

# Carrega história
with open("historia.json", "r", encoding="utf-8") as f:
    historia = json.load(f)

output = document.getElementById("output")
entrada = document.getElementById("entrada")
status_box = document.getElementById("status")  # precisa criar na página
botao_reiniciar = document.getElementById("reiniciar")  # botão oculto para reinício

# Estado inicial
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

def atualizar_status():
    status = f"❤️ Energia: {personagem['energia']}  💪 Habilidade: {personagem['habilidade']}  🍀 Sorte: {personagem['sorte']}  🥪 Provisões: {personagem['provisoes']}"
    status_box.innerText = status

def mudar_paragrafo(novo):
    global paragrafo_atual
    paragrafo_atual = novo
    salvar_progresso()
    mostrar_paragrafo()

def adicionar_item(item):
    personagem["mochila"].append(item)
    exibir(f"📦 Você ganhou: {item}")

def comer_provisao():
    if personagem["provisoes"] > 0:
        personagem["energia"] += 4
        personagem["provisoes"] -= 1
        exibir("🍞 Você comeu uma provisão (+4 energia).")
    else:
        exibir("❌ Você não tem provisões.")
    atualizar_status()

def testar_sorte():
    from random import randint
    dado = randint(2, 12)
    exibir(f"🎲 Teste de sorte! Você tirou {dado}")
    personagem["sorte"] -= 1
    atualizar_status()
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

    atualizar_status()

    # Verifica morte por energia
    if personagem["energia"] <= 0:
        exibir("💀 Sua energia chegou a zero. Você morreu. Fim de jogo.")
        botao_reiniciar.style.display = "block"
        return

    conteudo = historia.get(paragrafo_atual)
    if not conteudo:
        exibir("Fim da aventura.")
        return

    exibir(f"\n[{paragrafo_atual}] {conteudo['texto']}")

    if "ganhar_item" in conteudo:
        adicionar_item(conteudo["ganhar_item"])

    if conteudo.get("comer"):
        comer_provisao()

    if conteudo.get("teste_sorte"):
        if testar_sorte():
            mudar_paragrafo(conteudo["se_sorte"])
        else:
            mudar_paragrafo(conteudo["se_azar"])
        return

    if "combate" in conteudo:
        inimigo = conteudo["combate"]
        resultado = combate(personagem, inimigo, exibir=exibir)
        atualizar_status()
        if not resultado:
            exibir("💀 Você perdeu o combate e morreu. Fim de jogo.")
            botao_reiniciar.style.display = "block"
            return

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

# Salvar e carregar
def salvar_progresso():
    localStorage.setItem("paragrafo", paragrafo_atual)
    localStorage.setItem("personagem", json.dumps(personagem))

def carregar_progresso():
    global paragrafo_atual, personagem
    p = localStorage.getItem("paragrafo")
    dados = localStorage.getItem("personagem")
    if p and dados:
        paragrafo_atual = p
        personagem = json.loads(dados)

def reiniciar_aventura(event=None):
    global personagem, paragrafo_atual
    personagem = {
        "nome": "Aventureiro",
        "habilidade": 10,
        "energia": 20,
        "sorte": 10,
        "provisoes": 5,
        "mochila": []
    }
    paragrafo_atual = "1"
    salvar_progresso()
    botao_reiniciar.style.display = "none"
    mostrar_paragrafo()

entrada.addEventListener("keypress", create_proxy(lambda e: processar_entrada(e) if e.key == "Enter" else None))
botao_reiniciar.addEventListener("click", create_proxy(reiniciar_aventura))

carregar_progresso()
mostrar_paragrafo()
