from flask import Flask, render_template, request, redirect
import os
from datetime import datetime

app = Flask(__name__)

os.makedirs("dados", exist_ok=True)
os.makedirs("paginas", exist_ok=True)

# salvar
def salvar(arq, txt):
    with open(f"dados/{arq}", "a", encoding="utf-8") as f:
        f.write(txt + "\n")

# contar
def contar(nome):
    try:
        return len(open(f"dados/{nome}").readlines())
    except:
        return 0

# carregar páginas
def carregar_paginas():
    paginas = []

    for pasta in os.listdir("paginas"):
        caminho = os.path.join("paginas", pasta)

        if os.path.isdir(caminho):

            def ler(arq):
                try:
                    return open(os.path.join(caminho, arq), encoding="utf-8").read().strip()
                except:
                    return ""

            itens = []
            for i in range(1, 20):
                arq = f"{i}_item_menu.txt"
                if os.path.exists(os.path.join(caminho, arq)):
                    itens.append(ler(arq))

            valor = ler("subvalor.txt")

            paginas.append({
                "titulo": ler("titulo.txt"),
                "subtitulo": ler("subtitulo.txt"),
                "valor": valor,
                "botao": ler("botao.txt"),
                "itens": itens,
                "destaque": ler("destaque.txt")
            })

    return paginas

# SITE
@app.route("/")
def home():
    salvar("visitas.txt", str(datetime.now()))
    return render_template("site.html", paginas=carregar_paginas())

# CONTATO
@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome")
        msg = request.form.get("mensagem")

        salvar("contatos.txt", f"{nome} | {msg}")
        salvar("cliques.txt", "contato")

        return "Mensagem enviada!"
    
    return render_template("contato.html")

# ADMIN
@app.route("/admin")
def admin():
    return render_template("admin.html",
        visitas=contar("visitas.txt"),
        cliques=contar("cliques.txt"),
        contatos=contar("contatos.txt")
    )

# COMPRAR
@app.route("/comprar")
def comprar():
    salvar("cliques.txt", "comprar")
    return redirect("/")

# RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)