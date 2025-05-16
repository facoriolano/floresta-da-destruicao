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
    personagem["mochila"] = []  # necessário copiar lista
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
    atualizar_status()

    if not conteudo:
        exibir("⚠️ Parágrafo não encontrado.")
        mostrar_mensagem_final("Erro na história. Fim do jogo.")
        entrada.disabled = True
        return

    exibir(f"\n[{paragrafo_atual}] {conteudo['texto']}")

    # Itens
    if "ganhar_item" in conteudo:
        adicionar_item(personagem, conteudo["ganhar_item"])

    # Provisões
    if conteudo.get("comer"):
        comer_provisao(personagem)

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
# Começa o jogo: tenta carregar o progresso salvo
if not carregar_progresso():
    reiniciar_jogo()
else:
    esconder_finais()
    mostrar_paragrafo()

