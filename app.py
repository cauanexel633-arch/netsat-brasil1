from flask import Flask, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

# 🔥 GARANTIR PASTAS (IMPORTANTE PRO RENDER)
os.makedirs("dados", exist_ok=True)
os.makedirs("paginas", exist_ok=True)

# 📊 salvar visita
def salvar_visita():
    with open("dados/visitas.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}\n")

# 📊 salvar clique
def salvar_clique(tipo):
    with open("dados/cliques.txt", "a", encoding="utf-8") as f:
        f.write(f"{tipo} - {datetime.now()}\n")

# 📁 carregar páginas
def carregar_paginas():
    paginas = []

    try:
        pastas = os.listdir("paginas")
    except:
        pastas = []

    for pasta in pastas:
        caminho = os.path.join("paginas", pasta)

        if os.path.isdir(caminho):

            def ler(arq):
                try:
                    with open(os.path.join(caminho, arq), encoding="utf-8") as f:
                        return f.read().strip()
                except:
                    return ""

            # 🔹 itens do menu
            itens = []
            for i in range(1, 10):
                nome = f"{i}_item_menu.txt"
                if os.path.exists(os.path.join(caminho, nome)):
                    itens.append(ler(nome))

            # 🔹 valores
            valores = ler("subvalor.txt").split(",")

            paginas.append({
                "itens": itens,
                "titulo": ler("titulo.txt"),
                "subtitulo": ler("subtitulo.txt"),
                "valor": valores[0] if len(valores) > 0 else "",
                "valor_antigo": valores[1] if len(valores) > 1 else "",
                "botao": ler("botao.txt")
            })

    return paginas

# 🌍 SITE PRINCIPAL
@app.route('/')
def home():
    salvar_visita()
    paginas = carregar_paginas()
    return render_template("site.html", paginas=paginas)

# 💬 CONTATO (FORMULÁRIO)
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form.get("nome")
        mensagem = request.form.get("mensagem")

        with open("dados/contatos.txt", "a", encoding="utf-8") as f:
            f.write(f"{nome} - {mensagem}\n")

        salvar_clique("contato")

        return "Mensagem enviada com sucesso! 👍"

    return render_template("contato.html")

# 💰 CLIQUE COMPRAR
@app.route('/comprar')
def comprar():
    salvar_clique("comprar")
    return "Redirecionando..."

# 🚀 RENDER (OBRIGATÓRIO)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)