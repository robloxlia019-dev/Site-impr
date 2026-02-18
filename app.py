import os
import subprocess
from flask import Flask, render_template, redirect, flash

app = Flask(__name__)
app.secret_key = "painelsecret"
app.debug = True

bot_process = None  # Variável global do processo

def is_running():
    return bot_process and bot_process.poll() is None

@app.route("/")
def home():
    status = "ONLINE" if is_running() else "OFFLINE"
    return render_template("index.html", status=status)

# Start do bot (usa o bot.py que já está na pasta)
@app.route("/start")
def start():
    global bot_process
    if not os.path.exists("bot.py"):
        flash("bot.py não encontrado no servidor!", "error")
        return redirect("/")
    if not is_running():
        bot_process = subprocess.Popen(["python3", "bot.py"])
        flash("Bot iniciado!", "success")
    else:
        flash("Bot já está rodando!", "info")
    return redirect("/")

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

@app.route("/ping")
def ping():
    return "alive"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
