import os
import subprocess
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.debug = True  # Mostra logs detalhados

# Variável global que controla o bot
bot_process = None

# Função para verificar se o bot está rodando
def is_running():
    return bot_process and bot_process.poll() is None

# Página inicial do painel
@app.route("/")
def home():
    status = "ONLINE" if is_running() else "OFFLINE"
    return render_template("index.html", status=status)

# Upload do arquivo bot.py
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file and file.filename.endswith(".py"):
        file.save("bot.py")
    return redirect("/")

# Start do bot
@app.route("/start")
def start():
    global bot_process
    if not os.path.exists("bot.py"):
        return "Envie um bot primeiro."
    if not is_running():
        bot_process = subprocess.Popen(["python", "bot.py"])
    return redirect("/")

# Stop do bot
@app.route("/stop")
def stop():
    global bot_process
    if is_running():
        bot_process.terminate()
        bot_process = None
    return redirect("/")

# Endpoint de ping para manter online
@app.route("/ping")
def ping():
    return "alive"

# Inicia o Flask no Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
