# Mini Arcade — versão Python com Flask

Esta versão executa a lógica dos três jogos em Python no servidor. O navegador apresenta apenas HTML e CSS; não é necessário JavaScript.

## Estrutura
- `app.py` — lógica Python, rotas e pontuações.
- `templates/index.html` — página HTML com modelos Flask/Jinja.
- `static/estilos.css` — design responsivo.
- `requirements.txt` — dependência Flask.
- `best_scores.json` — criado automaticamente para guardar recordes.

## Executar no VS Code
1. Instala Python 3.
2. Abre esta pasta no VS Code.
3. Abre Terminal > New Terminal.
4. Instala a dependência:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Inicia o site:
   ```bash
   python app.py
   ```
6. Abre no navegador: http://127.0.0.1:5000

Em macOS/Linux, se necessário, usa `python3` em vez de `python`.

## Jogos
- 2048: movimentos por botões; a lógica de combinar peças é Python.
- Adivinha o Número: três níveis de dificuldade.
- Adivinha a Idade: perguntas sim/não com pesquisa binária.

## Best Scores
Os melhores resultados são guardados em `best_scores.json` no servidor. Para um site público com vários utilizadores, recomenda-se adicionar uma base de dados e autenticação. O segredo Flask deve ser alterado antes da publicação.
