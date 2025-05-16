from historia import carregar_historia, iniciar_jogo
from jogador import criar_personagem
from salvar import carregar_jogo

def main():
    print("=== A FLORESTA DA DESTRUIÇÃO ===")
    print("1. Novo jogo")
    print("2. Continuar jogo salvo")
    escolha = input("Escolha: ")

    historia = carregar_historia()

    if escolha == "1":
        personagem = criar_personagem()
        iniciar_jogo(personagem, historia)
    elif escolha == "2":
        personagem, paragrafo = carregar_jogo()
        if personagem:
            iniciar_jogo(personagem, historia, paragrafo)
        else:
            print("Começando novo jogo.")
            personagem = criar_personagem()
            iniciar_jogo(personagem, historia)
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
