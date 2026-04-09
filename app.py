from flask import Flask, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

# garantir pastas
os.makedirs("dados", exist_ok=True)
os.makedirs("paginas", exist_ok=True)

# salvar dados
def salvar(nome_arquivo, texto):
    with open(f"dados/{nome_arquivo}", "a", encoding="utf-8") as f:
        f.write(texto + "\n")

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

            valores = ler("subvalor.txt").split(",")

            paginas.append({
                "titulo": ler("titulo.txt"),
                "subtitulo": ler("subtitulo.txt"),
                "valor": valores[0] if valores else "",
                "valor_antigo": valores[1] if len(valores) > 1 else "",
                "botao": ler("botao.txt"),
                "itens": itens
            })

    return paginas

# site
@app.route("/")
def home():
    salvar("visitas.txt", str(datetime.now()))
    return render_template("site.html", paginas=carregar_paginas())

# contato
@app.route("/contato", methods=["POST"])
def contato():
    nome = request.form.get("nome")
    msg = request.form.get("mensagem")

    salvar("contatos.txt", f"{nome} | {msg}")
    salvar("cliques.txt", f"contato | {datetime.now()}")

    return "Mensagem enviada!"

# comprar
@app.route("/comprar")
def comprar():
    salvar("cliques.txt", f"comprar | {datetime.now()}")
    return "ok"

# render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)