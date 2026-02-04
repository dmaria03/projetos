import pymysql
from db import get_db_connection
from routes.usuarios import listar_usuarios_db, criar_usuario_db, atualizar_usuario_db, deletar_usuario_db

from routes.usuarios import (
    listar_usuarios_db,
    criar_usuario_db,
    atualizar_usuario_db,
    deletar_usuario_db
)

def menu_usuarios():
    while True:
        print("\n=== MENU USUÁRIOS ===")
        print("1 - Listar usuários")
        print("2 - Criar usuário")
        print("3 - Atualizar usuário")
        print("4 - Deletar usuário")
        print("5 - Sair")
        print("")

        opcao = input("Escolha uma opção: ")
        print(" ")

        if opcao == "1":
            usuarios = listar_usuarios_db()
            if usuarios:
                for u in usuarios:
                    print(f"{u['id']} - {u['nome']} ({u['email']}) | Setor: {u['setor']} | Tipo: {u['tipo']} | Ativo: {u['ativo']}")
            else:
                print("Nenhum usuário encontrado.")

        elif opcao == "2":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            setor = input("Setor: ")
            tipo = input("Tipo: ")
            ativo = input("Ativo? (s/n): ")
            user_id = criar_usuario_db(nome, email, senha, setor, tipo, ativo.lower() == "s")
            print(f"Usuário {nome} criado com ID {user_id}")

        elif opcao == "3":
            user_id = int(input("Digite o ID do usuário a atualizar: "))
            nome = input("Novo nome: ")
            email = input("Novo email: ")
            setor = input("Novo setor: ")
            tipo = input("Novo tipo: ")
            ativo = input("Ativo? (s/n): ")
            atualizar_usuario_db(user_id, nome, email, setor, tipo, ativo.lower() == "s")
            print(f"Usuário {user_id} atualizado com sucesso!")

        elif opcao == "4":
            user_id = int(input("Digite o ID do usuário a deletar: "))
            deletar_usuario_db(user_id)
            print(f"Usuário {user_id} deletado com sucesso!")

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente.")