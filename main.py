from jogador import criar_personagem
from historia import carregar_historia, iniciar_jogo

def main():
    print("🌲 A FLORESTA DA DESTRUIÇÃO 🌲")
    print("Baseado no livro-jogo de Ian Livingstone
")

    personagem = criar_personagem()
    historia = carregar_historia()

    iniciar_jogo(personagem, historia)

if __name__ == "__main__":
    main()
