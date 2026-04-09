SENHA = "1234"

if input("Senha: ") != SENHA:
    exit()

while True:
    print("""
1 - Estatísticas
2 - Atualizar
3 - Config
4 - Status
5 - Sair
""")

    op = input("> ")

    if op == "1":
        try:
            visitas = len(open("dados/visitas.txt").readlines())
            print("Visitas:", visitas)
        except:
            print("Sem dados")

    elif op == "2":
        print("Atualize recarregando o site")

    elif op == "3":
        SENHA = input("Nova senha: ")

    elif op == "4":
        print("Rodando...")

    elif op == "5":
        break