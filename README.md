# Floresta da Sombra Negra - Livro-Jogo

Um jogo web interativo inspirado na série **Fighting Fantasy** de Ian Livingstone e Steve Jackson. Jogue como um herói aventureiro em busca do lendário **Olho de Gárgula** na perigosa **Floresta da Sombra Negra**.

## Características

- **Criação de Personagem:** Role os dados para determinar sua Habilidade, Energia e Sorte
- **Sistema de Combate:** Enfrente inimigos em combates baseados em dados (2d6)
- **Testes de Sorte:** Use sua sorte para evitar armadilhas e superar desafios
- **Narrativa Ramificada:** Suas escolhas determinam o caminho da aventura
- **Gráficos 8-bit:** Estilo visual retrô nostálgico
- **Interface Terminal:** Design inspirado em computadores dos anos 80

## Como Jogar

1. **Abra o arquivo `index.html` em seu navegador web**
2. **Clique em "INICIAR JOGO"**
3. **Role os dados para criar seu personagem**
4. **Confirme seus atributos e comece a aventura**
5. **Faça escolhas e enfrente desafios**

## Mecânicas do Jogo

### Atributos do Personagem

- **HABILIDADE:** Determina sua eficácia em combate
- **ENERGIA:** Sua saúde (quando chega a 0, você morre)
- **SORTE:** Sua capacidade de ter sorte em testes de sorte

### Combate

1. Você e o inimigo rolam 2 dados (2d6) e somam à sua Habilidade
2. O combatente com o maior resultado vence a rodada
3. O perdedor perde 2 pontos de Energia
4. O combate continua até que um dos combatentes morra

### Teste de Sorte

1. Role 2 dados (2d6)
2. Se o resultado for **igual ou menor** à sua Sorte, você tem sucesso
3. Se for **maior**, você falha
4. Cada teste custa 1 ponto de Sorte (permanentemente)

## Estrutura do Projeto

```
fighting-fantasy-game/
├── index.html              # Página principal
├── style.css               # Estilos CSS
├── script.js               # Lógica do jogo (JavaScript)
├── data/
│   └── story.json          # Narrativa do jogo
├── assets/
│   └── images/             # Imagens 8-bit
│       ├── forest_entrance.png
│       ├── goblin.png
│       ├── troll.png
│       ├── gargoyle_eye.png
│       └── combat_background.png
└── README.md               # Este arquivo
```

## Como Publicar no GitHub Pages

### Passo 1: Criar um Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique em **"New"** para criar um novo repositório
3. Nomeie o repositório como `fighting-fantasy-game` (ou outro nome de sua escolha)
4. Escolha **"Public"** para que o jogo seja acessível
5. Clique em **"Create repository"**

### Passo 2: Fazer Upload dos Arquivos

#### Opção A: Usando Git (Recomendado)

```bash
# Clone o repositório (substitua USERNAME pelo seu usuário do GitHub)
git clone https://github.com/USERNAME/fighting-fantasy-game.git
cd fighting-fantasy-game

# Copie todos os arquivos do jogo para este diretório
# (index.html, style.css, script.js, data/, assets/)

# Adicione os arquivos ao Git
git add .

# Faça um commit
git commit -m "Adicionar jogo Fighting Fantasy"

# Envie para o GitHub
git push origin main
```

#### Opção B: Usando a Interface Web do GitHub

1. No repositório do GitHub, clique em **"Add file"** → **"Upload files"**
2. Arraste e solte os arquivos ou selecione-os
3. Clique em **"Commit changes"**

### Passo 3: Ativar GitHub Pages

1. Vá para **Settings** do repositório
2. Procure por **"Pages"** no menu lateral esquerdo
3. Em **"Source"**, selecione **"main"** como branch
4. Clique em **"Save"**
5. Aguarde alguns minutos e seu jogo estará disponível em:
   ```
   https://USERNAME.github.io/fighting-fantasy-game/
   ```

## Requisitos

- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexão com a internet (para carregar os arquivos JSON e imagens)

## Tecnologias Utilizadas

- **HTML5:** Estrutura da página
- **CSS3:** Estilização e efeitos visuais
- **JavaScript (ES6):** Lógica do jogo
- **JSON:** Armazenamento de dados da narrativa

## Inspiração

Este jogo é inspirado na série **Fighting Fantasy** de Ian Livingstone e Steve Jackson, particularmente no livro **"The Forest of Doom"** (Floresta da Destruição). A narrativa é original e criada especificamente para este projeto.

## Licença

Este projeto é fornecido como está, para fins educacionais e de entretenimento.

## Autor

Desenvolvido com ❤️ usando Manus AI

---

**Divirta-se na Floresta da Sombra Negra!** 🎮🗡️

