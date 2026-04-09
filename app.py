from flask import Flask, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

# 📊 salvar visita
def salvar_visita():
    with open("dados/visitas.txt", "a") as f:
        f.write(f"{datetime.now()}\n")

# 📊 salvar clique
def salvar_clique(tipo):
    with open("dados/cliques.txt", "a") as f:
        f.write(f"{tipo} - {datetime.now()}\n")

# 📁 carregar páginas
def carregar_paginas():
    paginas = []

    for pasta in os.listdir("paginas"):
        caminho = os.path.join("paginas", pasta)

        if os.path.isdir(caminho):
            def ler(arq):
                try:
                    return open(os.path.join(caminho, arq), encoding="utf-8").read()
                except:
                    return ""

            itens = []
            for i in range(1, 10):
                nome = f"{i}_item_menu.txt"
                if os.path.exists(os.path.join(caminho, nome)):
                    itens.append(ler(nome))

            valores = ler("subvalor.txt").split(",")

            paginas.append({
                "itens": itens,
                "titulo": ler("titulo.txt"),
                "subtitulo": ler("subtitulo.txt"),
                "valor": valores[0],
                "valor_antigo": valores[1] if len(valores) > 1 else "",
                "botao": ler("botao.txt")
            })

    return paginas

# 🌍 site
@app.route('/')
def home():
    salvar_visita()
    paginas = carregar_paginas()
    return render_template("site.html", paginas=paginas)

# 💬 contato
@app.route('/contato', methods=['POST'])
def contato():
    nome = request.form.get("nome")
    mensagem = request.form.get("mensagem")

    with open("dados/contatos.txt", "a") as f:
        f.write(f"{nome} - {mensagem}\n")

    salvar_clique("contato")
    return "Mensagem enviada!"

# 💰 clique comprar
@app.route('/comprar')
def comprar():
    salvar_clique("comprar")
    return "Redirecionando..."

app.run(host="0.0.0.0", port=5000)