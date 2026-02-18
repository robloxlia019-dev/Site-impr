import os
import subprocess
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "painelsecret"  # necessário para mensagens flash
app.debug = True

bot_process = None  # controle do processo do bot

# Verifica se o bot está rodando
def is_running():
    return bot_process and bot_process.poll() is None

# Página inicial
@app.route("/")
def home():
    status = "ONLINE" if is_running() else "OFFLINE"
    return render_template("index.html", status=status)

# Upload do bot.py
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file and file.filename.endswith(".py"):
        file.save("bot.py")
        flash("Bot enviado com sucesso!", "success")
    else:
        flash("Envie apenas arquivos .py", "error")
    return redirect("/")

# Start do bot
@app.route("/start")
def start():
    global bot_process
    if not os.path.exists("bot.py"):
        flash("Envie um bot primeiro!", "error")
        return redirect("/")
    if not is_running():
        bot_process = subprocess.Popen(["python3", "bot.py"])
        flash("Bot iniciado!", "success")
    else:
        flash("Bot já está rodando!", "info")
    return redirect("/")

# Stop do bot
@app.route("/stop")
def stop():
    global bot_process
    if is_running():
        bot_process.terminate()
        bot_process = None
        flash("Bot parado!", "success")
    else:
        flash("Nenhum bot rodando.", "info")
    return redirect("/")

# Ping para manter online
@app.route("/ping")
def ping():
    return "alive"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
