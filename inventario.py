def comer_provisao(personagem):
    if personagem["provisoes"] > 0:
        personagem["provisoes"] -= 1
        personagem["energia"] += 4
        print("🍗 Você come uma provisão e recupera 4 de energia.")
        print(f"energia atual: {personagem['energia']} | Provisões restantes: {personagem['provisoes']}")
    else:
        print("⚠️ Você não tem mais provisões!")

def adicionar_item(personagem, item):
    personagem["itens"].append(item)
    print(f"🎒 Você recebeu: {item}")

def mostrar_inventario(personagem):
    print("\n🎒 Inventário:")
    print(f"- Provisões: {personagem['provisoes']}")
    print("- Itens:")
    if personagem["itens"]:
        for item in personagem["itens"]:
            print(f"  • {item}")
    else:
        print("  (vazio)")
