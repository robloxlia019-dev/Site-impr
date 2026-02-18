import os
import subprocess
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.debug = True  # Mostra logs detalhados
bot_process = None

def is_running():
    return bot_process and bot_process.poll() is None

@app.route("/")
def home():
    status = "ONLINE" if is_running() else "OFFLINE"
    return render_template("index.html", status=status)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file and file.filename.endswith(".py"):
        file.save("bot.py")
    return redirect("/")

@app.route("/start")
def start():
    global bot_process
    if not os.path.exists("bot.py"):
        return "Envie um bot primeiro."
    if not is_running():
        bot_process = subprocess.Popen(["python", "bot.py"])
    return redirect("/")

@app.route("/stop")
def stop():
    global bot_process
    if is_running():
        bot_process.terminate()
        bot_process = None
    return redirect("/")

@app.route("/ping")
def ping():
    return "alive"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)        bot_process = None
    return redirect("/")

@app.route("/ping")
def ping():
    return "alive"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
