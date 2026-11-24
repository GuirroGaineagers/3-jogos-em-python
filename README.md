# Mini Arcade

**Disciplina:** Oficina de Multimédia - 12.º Ano - CRSI
**Ano Letivo:** 2026/2027
**Autor:** Guilherme Sousa
**Turma:** 12.º A3
**Link da Aplicação Web:** file:///Users/guisousa_niga/Downloads/mini_arcade_pyscript/index.html

---

## 1. Visão Geral do Projeto

**Descrição:** O Mini Arcade é uma aplicação web com três jogos — 2048, Adivinha o Número e Adivinha a Idade — cuja lógica é executada em Python (Flask) no servidor. O navegador mostra apenas HTML e CSS, sem JavaScript. Os melhores resultados de cada jogo são guardados e apresentados numa tabela de Best Scores.

**Proposta Escolhida:** Proposta 1

---

## 2. Estrutura do Código e Funcionalidades Integradas

Os exercícios das fichas foram **adaptados** e ampliados com apoio da IA, sendo integrados numa única aplicação Flask.

**`app.py` — lógica e rotas**
- Uma única rota `/` (GET e POST) recebe as ações dos formulários através do campo `action`.
- O estado de cada jogo fica guardado na `session` do Flask (`game2048`, `number_game`, `age_game`).
- **2048:** a função `compress_line` junta peças iguais e calcula os pontos; `move_2048` aplica o movimento nas quatro direções, adiciona uma nova peça e verifica vitória (2048) e fim de jogo (`can_move`).
- **Adivinha o Número:** três níveis (Fácil 1–20 com 10 tentativas, Médio 1–50 com 7, Difícil 1–100 com 5). Valida o palpite, impede repetições e calcula a pontuação consoante as tentativas usadas e a dificuldade.
- **Adivinha a Idade:** o computador usa pesquisa binária (1–120) com perguntas de sim/não e pede confirmação no fim.
- **Best Scores:** `load_scores`, `save_scores` e `update_best` guardam o melhor resultado de cada jogo em `best_scores.json` (para a idade, quanto menos perguntas, melhor). Existe ainda a opção de limpar os recordes.

**`templates/index.html` — interface**
- Template Jinja com cabeçalho, secção de apresentação, cartões dos jogos, área de jogo (muda consoante `?game=`) e tabela de Best Scores.
- Os controlos são formulários HTML (`POST`), sem JavaScript, e inclui ligação "Saltar para o conteúdo" e atributos ARIA para acessibilidade.

**`static/estilos.css` — design**
- Tema escuro com variáveis CSS (`:root`), gradientes azul/roxo, layout em grelha e *flexbox*.
- Design responsivo (pontos de quebra a 850px e 620px) e respeito por `prefers-reduced-motion`.
- Cores diferentes por valor das peças do 2048.

**`requirements.txt`**
- `Flask>=3.0,<4.0`

---

## 3. Registo de Utilização da IA

**1. Prompt para conversão Web/HTML**
> "Tenho três jogos feitos em Python que correm no terminal: 2048, adivinha o número e adivinha a idade. Quero transformá-los numa aplicação web com Flask, mantendo a lógica em Python e usando só HTML e CSS no navegador, sem JavaScript. Cria o `app.py`, o `index.html` com Jinja e o `estilos.css`."

**2. Prompt para ampliação e construção de funcionalidades**
> "Agora quero melhorar a aplicação: o jogo de adivinhar o número deve ter três níveis de dificuldade (fácil, médio e difícil) com um número de tentativas diferente em cada um e uma pontuação no fim. Adiciona também uma tabela de Best Scores guardada num ficheiro JSON e um botão para limpar os recordes. No jogo da idade, o computador deve usar pesquisa binária e pedir confirmação no final."

**3. Dificuldades e erros corrigidos com a IA**
> "Quando clico num botão do 2048 e depois atualizo a página, o movimento repete-se. Porquê?"

- Resolvido com o padrão *Post/Redirect/Get*: depois de cada ação, a página faz `redirect` para evitar o reenvio do formulário.

> "O estado do jogo perde-se sempre que a página recarrega. Como o guardo?"

- Resolvido com a `session` do Flask e `session.modified = True`, porque o Flask não deteta alterações dentro de listas e dicionários.

> "No 2048, como faço para mover para a direita e para baixo sem repetir o código todo?"

- Em vez de escrever quatro versões, a linha é invertida para direita/baixo, processada pela mesma função `compress_line` e invertida de novo.

> "No jogo da idade, o melhor resultado é o que tem menos perguntas, mas o Best Score guardava sempre o valor mais alto."

- Resolvido com o parâmetro `lower_is_better` na função `update_best`.

> "O jogo do número dá erro se eu escrever texto ou um número fora do intervalo."

- Resolvido com `try/except` na conversão para inteiro e com validação do intervalo, de números repetidos e de jogo já terminado.

**4. Otimização de Layout**
> "Quero um tema escuro e moderno, com azul e roxo como cores principais, cartões com cantos arredondados e um aspeto de arcade. Usa variáveis CSS para as cores."

> "Os botões estão pequenos para telemóvel. Aumenta-os e adiciona um efeito quando passo o rato por cima."

> "Faz o layout adaptar-se a ecrãs pequenos: três colunas no computador, duas no tablet e uma no telemóvel. Dá a cada valor do 2048 uma cor diferente."

- Alterações pedidas: paleta de cores (azul, roxo e verde), margens e largura máxima do conteúdo, tipo de letra Inter com títulos maiores e botões com tamanho mínimo de 44px e contorno visível ao navegar com o teclado.

---

## 4. Estrutura de Ficheiros do Repositório

1. `templates/index.html` – página principal da Web App
2. `app.py` – ficheiro principal da aplicação (lógica Python, rotas e pontuações)
3. `static/estilos.css` – folha de estilos para o layout Web
4. `requirements.txt` – dependências do projeto (Flask)
5. `best_scores.json` – criado automaticamente para guardar os recordes
6. `README.md` – este relatório de projeto

**Como executar:**
```bash
python -m pip install -r requirements.txt
python app.py
```
Abrir no navegador: http://127.0.0.1:5000 (em macOS/Linux, usar `python3` se necessário).

---

## 5. Reflexão Crítica e Aprendizagem

Este projeto permitiu-me pegar em exercícios simples de Python, que antes só funcionavam no terminal, e transformá-los numa aplicação web completa e com bom aspeto. O que correu melhor foi ver a lógica que já conhecia ganhar uma interface: o 2048 e o sistema de Best Scores foram as partes de que mais gostei, porque dão à aplicação um aspeto de produto real e não apenas de exercício de aula. Também gostei de perceber que a lógica de um jogo pode ficar toda em Python e o navegador limitar-se a mostrar o resultado.

A maior dificuldade foi compreender como manter o estado dos jogos. Num programa de terminal, as variáveis ficam em memória enquanto o programa corre, mas numa aplicação web cada clique é um novo pedido ao servidor. Tive de aprender o que são sessões, como funcionam os formulários com `POST` e porque é que é preciso fazer `redirect` depois de cada ação. Houve ainda erros que só descobri ao testar, como o movimento do 2048 repetir-se ao atualizar a página ou o Best Score da idade guardar o pior valor em vez do melhor.

A Inteligência Artificial mudou a minha forma de programar, sobretudo na maneira como resolvo problemas. Em vez de começar do zero, passei a descrever o que queria, analisar o código sugerido e testá-lo. Isso poupou-me muito tempo, mas também me mostrou que não chega copiar: foi preciso ler o código, perceber porque funcionava e voltar a perguntar quando algo falhava. Aprendi que escrever bem um pedido é uma competência importante e que a IA é uma boa ajuda, mas a responsabilidade de compreender e verificar o resultado continua a ser minha.
