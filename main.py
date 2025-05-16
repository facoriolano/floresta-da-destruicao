from js import localStorage
from combate_web import combate
import json
from pyodide.ffi import create_proxy
from js import document

# Carrega história
with open("historia.json", "r", encoding="utf-8") as f:
    historia = json.load(f)

output = document.getElementById("output")
entrada = document.getElementById("entrada")
status_box = document.getElementById("status")
mensagem_final = document.getElementById("mensagem-final")
botao_reiniciar = document.getElementById("reiniciar")

# Personagem padrão
personagem_inicial = {
    "nome": "Aventureiro",
    "habilidade": 10,
    "energia": 20,
    "sorte": 10,
    "provisoes": 5,
    "mochila": []
}

personagem = personagem_inicial.copy()
paragrafo_atual = "1"
esperando_entrada = False
opcoes_disponiveis = []

def exibir(texto):
    output.innerText += "\n" + texto

def atualizar_status():
    status_texto = (
        f"👤 {personagem['nome']}\n"
        f"⚔️ Habilidade: {personagem['habilidade']}\n"
        f"❤️ Energia: {personagem['energia']}\n"
        f"🍀 Sorte: {personagem['sorte']}\n"
        f"🥪 Provisões: {personagem['provisoes']}\n"
        f"🎒 Mochila: {', '.join(personagem['mochila']) if personagem['mochila'] else 'vazia'}"
    )
    status_box.innerText = status_texto

def aplicar_efeitos(conteudo):
    """Aplica efeitos do parágrafo no personagem, lendo as chaves do JSON."""
    mudou_status = False

    # Energia
    if "ganhar_energia" in conteudo:
        personagem["energia"] += conteudo["ganhar_energia"]
        exibir(f"❤️ Você ganhou {conteudo['ganhar_energia']} pontos de energia.")
        mudou_status = True

    if "perder_energia" in conteudo:
        personagem["energia"] -= conteudo["perder_energia"]
        if personagem["energia"] < 0:
            personagem["energia"] = 0
        exibir(f"💔 Você perdeu {conteudo['perder_energia']} pontos de energia.")
        mudou_status = True

    # Provisões
    if "ganhar_provisoes" in conteudo:
        personagem["provisoes"] += conteudo["ganhar_provisoes"]
        exibir(f"🥪 Você ganhou {conteudo['ganhar_provisoes']} provisões.")
        mudou_status = True

    if "perder_provisoes" in conteudo:
        personagem["provisoes"] -= conteudo["perder_provisoes"]
        if personagem["provisoes"] < 0:
            personagem["provisoes"] = 0
        exibir(f"🥪 Você perdeu {conteudo['perder_provisoes']} provisões.")
        mudou_status = True

    # Sorte
    if "ganhar_sorte" in conteudo:
        personagem["sorte"] += conteudo["ganhar_sorte"]
        exibir(f"🍀 Você ganhou {conteudo['ganhar_sorte']} pontos de sorte.")
        mudou_status = True

    if "perder_sorte" in conteudo:
        personagem["sorte"] -= conteudo["perder_sorte"]
        if personagem["sorte"] < 0:
            personagem["sorte"] = 0
        exibir(f"🍀 Você perdeu {conteudo['perder_sorte']} pontos de sorte.")
        mudou_status = True

    # Ganhar item
    if "ganhar_item" in conteudo:
        if conteudo["ganhar_item"] not in personagem["mochila"]:
            personagem["mochila"].append(conteudo["ganhar_item"])
            exibir(f"📦 Você ganhou: {conteudo['ganhar_item']}")
            mudou_status = True

    if mudou_status:
        atualizar_status()

def carregar_progresso():
    global personagem, paragrafo_atual
    progresso_salvo = localStorage.getItem("aventura_progresso")
    if progresso_salvo:
        try:
            dados = json.loads(progresso_salvo)
            paragrafo_atual = dados["paragrafo_atual"]
            personagem.update(dados["personagem"])
            return True
        except Exception as e:
            exibir(f"⚠️ Erro ao carregar progresso: {e}")
    return False

def salvar_progresso():
    progresso = {
        "paragrafo_atual": paragrafo_atual,
        "personagem": personagem
    }
    localStorage.setItem("aventura_progresso", json.dumps(progresso))

def mostrar_mensagem_final(texto):
    mensagem_final.innerText = texto
    mensagem_final.style.display = "block"
    botao_reiniciar.style.display = "inline-block"

def esconder_finais():
    mensagem_final.style.display = "none"
    botao_reiniciar.style.display = "none"

def reiniciar_jogo(event=None):
    global personagem, paragrafo_atual
    personagem = personagem_inicial.copy()
    personagem["mochila"] = []
    paragrafo_atual = "1"
    esconder_finais()
    entrada.disabled = False
    entrada.focus()
    mostrar_paragrafo()
    localStorage.removeItem("aventura_progresso")

def mudar_paragrafo(novo):
    global paragrafo_atual
    paragrafo_atual = novo
    salvar_progresso()
    mostrar_paragrafo()

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
        exibir("⚠️ Parágrafo não encontrado.")
        mostrar_mensagem_final("Erro na história. Fim do jogo.")
        entrada.disabled = True
        return

    aplicar_efeitos(conteudo)
    atualizar_status()
    exibir(f"\n[{paragrafo_atual}] {conteudo['texto']}")

    # Teste de sorte
    if conteudo.get("teste_sorte"):
        if testar_sorte(personagem):
            mudar_paragrafo(conteudo["se_sorte"])
        else:
            mudar_paragrafo(conteudo["se_azar"])
        return

    # Combate
    if "combate" in conteudo:
        inimigo = conteudo["combate"]
        resultado = combate(personagem, inimigo, exibir=exibir)
        if not resultado:
            exibir("💀 Você perdeu o combate e morreu.")
            mostrar_mensagem_final("☠️ Fim da aventura.")
            entrada.disabled = True
            return

    # Opções de escolha
    if "escolhas" in conteudo:
        opcoes_disponiveis = list(conteudo["escolhas"].items())
        for i, (texto, _) in enumerate(opcoes_disponiveis, 1):
            exibir(f"{i}. {texto}")
        esperando_entrada = True
    else:
        exibir("🔚 Fim do caminho.")
        mostrar_mensagem_final("✨ Parabéns, você completou sua jornada!")
        entrada.disabled = True

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
botao_reiniciar.addEventListener("click", create_proxy(reiniciar_jogo))

# Começa o jogo
if not carregar_progresso():
    reiniciar_jogo()
else:
    esconder_finais()
    mostrar_paragrafo()
