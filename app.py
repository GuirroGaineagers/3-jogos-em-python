from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mini-arcade-chave-local-altera-em-producao")
SCORES_FILE = os.path.join(os.path.dirname(__file__), "best_scores.json")

# -------------------- Best Scores --------------------

def load_scores():
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_scores(scores):
    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, ensure_ascii=False, indent=2)

def update_best(game, value, detail, lower_is_better=False):
    scores = load_scores()
    previous = scores.get(game)
    better = (
        previous is None
        or (value < previous["value"] if lower_is_better else value > previous["value"])
    )
    if better:
        scores[game] = {
            "value": value,
            "detail": detail,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        save_scores(scores)
    return better

def get_display_scores():
    scores = load_scores()
    return {
        "2048": scores.get("2048"),
        "number": scores.get("number"),
        "age": scores.get("age")
    }

# -------------------- Estado dos jogos --------------------

def init_games():
    if "game2048" not in session:
        new_2048()
    if "number_game" not in session:
        new_number_game()
    if "age_game" not in session:
        new_age_game()

def new_2048():
    board = [[0] * 4 for _ in range(4)]
    session["game2048"] = {
        "board": board,
        "score": 0,
        "won": False,
        "over": False
    }
    add_tile()
    add_tile()
    session.modified = True

def add_tile():
    game = session["game2048"]
    empty = [(r, c) for r in range(4) for c in range(4) if game["board"][r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        game["board"][r][c] = 4 if random.random() < 0.1 else 2

def compress_line(line):
    values = [value for value in line if value]
    result = []
    gained = 0
    index = 0
    while index < len(values):
        if index + 1 < len(values) and values[index] == values[index + 1]:
            merged = values[index] * 2
            result.append(merged)
            gained += merged
            index += 2
        else:
            result.append(values[index])
            index += 1
    return result + [0] * (4 - len(result)), gained

def can_move(board):
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                return True
            if col < 3 and board[row][col] == board[row][col + 1]:
                return True
            if row < 3 and board[row][col] == board[row + 1][col]:
                return True
    return False

def move_2048(direction):
    game = session["game2048"]
    if game["over"]:
        return
    board = game["board"]
    original = [row[:] for row in board]
    gained_total = 0

    for index in range(4):
        if direction in ("left", "right"):
            line = board[index][:]
        else:
            line = [board[row][index] for row in range(4)]

        if direction in ("right", "down"):
            line.reverse()

        line, gained = compress_line(line)
        gained_total += gained

        if direction in ("right", "down"):
            line.reverse()

        if direction in ("left", "right"):
            board[index] = line
        else:
            for row in range(4):
                board[row][index] = line[row]

    if board == original:
        return

    game["score"] += gained_total
    add_tile()

    if any(2048 in row for row in board) and not game["won"]:
        game["won"] = True
        session["notice"] = "Incrível! Chegaste ao 2048. Podes continuar a jogar."

    if not can_move(board):
        game["over"] = True
        session["notice"] = "Fim do jogo! Já não existem movimentos possíveis."

    update_best("2048", game["score"], max(max(row) for row in board))
    session["game2048"] = game
    session.modified = True

# -------------------- Adivinha o Número --------------------

LEVELS = {
    "easy": {"name": "Fácil", "min": 1, "max": 20, "tries": 10},
    "medium": {"name": "Médio", "min": 1, "max": 50, "tries": 7},
    "hard": {"name": "Difícil", "min": 1, "max": 100, "tries": 5}
}

def new_number_game(level=None):
    level = level or session.get("number_game", {}).get("level", "easy")
    config = LEVELS.get(level, LEVELS["easy"])
    session["number_game"] = {
        "level": level,
        "secret": random.randint(config["min"], config["max"]),
        "remaining": config["tries"],
        "attempts": [],
        "finished": False,
        "message": "Escolhe um número para começar."
    }

# -------------------- Adivinha a Idade --------------------

def new_age_game():
    session["age_game"] = {
        "low": 1,
        "high": 120,
        "questions": 0,
        "finished": False,
        "guess": None,
        "message": "Pensa numa idade entre 1 e 120 anos e responde às perguntas."
    }

# -------------------- Rotas --------------------

@app.route("/", methods=["GET", "POST"])
def index():
    init_games()
    active_game = request.args.get("game", "home")
    notice = session.pop("notice", None)

    if request.method == "POST":
        action = request.form.get("action", "")

        # Controlos do 2048
        if action == "move":
            direction = request.form.get("direction")
            if direction in ("up", "down", "left", "right"):
                move_2048(direction)
            return redirect(url_for("index", game="2048"))

        if action == "restart_2048":
            new_2048()
            session["notice"] = "Novo jogo iniciado!"
            return redirect(url_for("index", game="2048"))

        # Adivinha o Número
        if action == "choose_level":
            level = request.form.get("level", "easy")
            new_number_game(level)
            return redirect(url_for("index", game="number"))

        if action == "guess_number":
            game = session["number_game"]
            config = LEVELS[game["level"]]
            raw_guess = request.form.get("guess", "")
            try:
                guess = int(raw_guess)
            except ValueError:
                game["message"] = "Introduz um número inteiro válido."
                guess = None

            if guess is not None:
                if not config["min"] <= guess <= config["max"]:
                    game["message"] = f"Escolhe um número entre {config['min']} e {config['max']}."
                elif game["finished"]:
                    game["message"] = "Este jogo já terminou. Inicia um novo número."
                elif guess in game["attempts"]:
                    game["message"] = "Já tentaste esse número. Experimenta outro!"
                else:
                    game["attempts"].append(guess)
                    game["remaining"] -= 1
                    if guess == game["secret"]:
                        game["finished"] = True
                        points = max(10, (config["tries"] - len(game["attempts"]) + 1) * 100
                                     + (100 if game["level"] == "hard" else 50 if game["level"] == "medium" else 0))
                        game["message"] = f"Acertaste! O número era {game['secret']}. Ganhaste {points} pontos!"
                        update_best("number", points, f"{len(game['attempts'])} tentativa(s)")
                    elif game["remaining"] == 0:
                        game["finished"] = True
                        game["message"] = f"Ficaste sem tentativas. O número era {game['secret']}."
                    elif guess < game["secret"]:
                        game["message"] = "O número secreto é MAIOR. Tenta novamente!"
                    else:
                        game["message"] = "O número secreto é MENOR. Tenta novamente!"
            session["number_game"] = game
            return redirect(url_for("index", game="number"))

        if action == "restart_number":
            new_number_game()
            return redirect(url_for("index", game="number"))

        # Adivinha a Idade
        if action == "age_answer":
            game = session["age_game"]
            if not game["finished"]:
                answer = request.form.get("answer")
                middle = (game["low"] + game["high"]) // 2
                if answer == "yes":
                    game["low"] = middle + 1
                elif answer == "no":
                    game["high"] = middle
                game["questions"] += 1

                if game["low"] == game["high"]:
                    game["finished"] = True
                    game["guess"] = game["low"]
                    game["message"] = f"A tua idade é {game['guess']} anos? Confirma se acertei!"
                else:
                    next_middle = (game["low"] + game["high"]) // 2
                    game["message"] = f"A tua idade é maior do que {next_middle} anos?"
                session["age_game"] = game
            return redirect(url_for("index", game="age"))

        if action == "age_confirm":
            game = session["age_game"]
            if request.form.get("answer") == "yes":
                game["message"] = f"Consegui! Descobri a tua idade em {game['questions'] + 1} perguntas."
                update_best("age", game["questions"] + 1, str(game["guess"]), lower_is_better=True)
            else:
                game["message"] = "Ups! Parece que uma resposta anterior não estava correta. Recomeça e tenta novamente."
            game["finished"] = True
            game["confirmed"] = True
            session["age_game"] = game
            return redirect(url_for("index", game="age"))

        if action == "restart_age":
            new_age_game()
            return redirect(url_for("index", game="age"))

        if action == "clear_scores":
            save_scores({})
            flash("Os Best Scores foram apagados.")
            return redirect(url_for("index", game="home"))

    return render_template(
        "index.html",
        active_game=active_game,
        game2048=session["game2048"],
        number_game=session["number_game"],
        levels=LEVELS,
        age_game=session["age_game"],
        scores=get_display_scores(),
        notice=notice
    )

if __name__ == "__main__":
    app.run(debug=True)
