from flask import Blueprint, request, jsonify
import pymysql
from db import get_db_connection   # agora importa do db.py

usuarios_bp = Blueprint("usuarios", __name__)

# # Criar usuário
# # @usuarios_bp.route("/", methods=["POST"])
# # def criar_usuario():
# #     data = request.json
# #     conn = get_db_connection()
# #     cur = conn.cursor()
# #     cur.execute("""
# #         INSERT INTO usuarios (nome, email, senha_hash, setor, tipo)
# #         VALUES (%s, %s, %s, %s, %s)
# #     """, (data["nome"], data["email"], data["senha_hash"], data["setor"], data["tipo"]))
# #     conn.commit()
# #     conn.close()
# #     return jsonify({"message": "Usuário criado com sucesso"}), 201

# @usuarios_bp.route("/", methods=["POST"])
# def criar_usuario():
#     data = request.get_json(force=True)  # força interpretar como JSON
#     print("DEBUG - JSON recebido:", data)  # log no terminal

#     # Validação
#     if not data or not data.get("nome") or not data.get("email") or not data.get("senha_hash"):
#         return jsonify({"status": "error", "message": "Campos obrigatórios faltando"}), 400

#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO usuarios (nome, email, senha_hash, setor, tipo, ativo)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (
#             data["nome"],
#             data["email"],
#             data["senha_hash"],
#             data.get("setor", ""),
#             data.get("tipo", "Solicitante"),
#             1 if data.get("ativo", True) else 0 # garante compatibilidade com TINYINT/BOOLEAN
#         ))
#         conn.commit()
#         user_id = cur.lastrowid
#     except Exception as e:
#         print("ERRO SQL:", e)  # log detalhado no terminal
#         return jsonify({"status": "error", "message": str(e)}), 500
#     finally:
#         conn.close()

#     return jsonify({
#         "status": "success",
#         "message": "Usuário criado com sucesso",
#         "usuario": {
#             "id": user_id,
#             "nome": data["nome"],
#             "email": data["email"],
#             "setor": data.get("setor", ""),
#             "tipo": data.get("tipo", "Solicitante"),
#             "ativo": data.get("ativo", True)
#         }
#     }), 201



# # Listar usuários
# @usuarios_bp.route("/", methods=["GET"])
# def listar_usuarios():
#     conn = get_db_connection()
#     cur = conn.cursor(pymysql.cursors.DictCursor)
#     cur.execute("SELECT id, nome, email, setor, tipo, ativo FROM usuarios")
#     result = cur.fetchall()
#     conn.close()
#     #return jsonify(result), 200
#     return jsonify(result if result else ["sem registro"]), 200

# @usuarios_bp.route("/<int:id>", methods=["GET"])
# def buscar_usuario(id):
#     conn = get_db_connection()
#     cur = conn.cursor(pymysql.cursors.DictCursor)
#     cur.execute("SELECT id, nome, email, setor, tipo, ativo FROM usuarios WHERE id=%s", (id,))
#     usuario = cur.fetchone()
#     conn.close()

#     if usuario:
#         return jsonify({"status": "success", "usuario": usuario}), 200
#     else:
#         return jsonify({"status": "error", "message": "Usuário não encontrado"}), 404


# # Atualizar usuário
# @usuarios_bp.route("/<int:id>", methods=["PUT"])
# def atualizar_usuario(id):
#     data = request.json
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         UPDATE usuarios
#         SET nome=%s, email=%s, setor=%s, tipo=%s, ativo=%s
#         WHERE id=%s
#     """, (data["nome"], data["email"], data["setor"], data["tipo"], data["ativo"], id))
#     conn.commit()
#     conn.close()
#     return jsonify({"message": "Usuário atualizado com sucesso"}), 200

# # Deletar usuário
# @usuarios_bp.route("/<int:id>", methods=["DELETE"])
# def deletar_usuario(id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
#     conn.commit()
#     conn.close()
#     return jsonify({"message": "Usuário deletado com sucesso"}), 200

import pymysql
from flask import Blueprint, request, jsonify
from db import get_db_connection

usuarios_bp = Blueprint("usuarios", __name__)

# Funções independentes (para CLI e rotas)
def listar_usuarios_db():
    conn = get_db_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT id, nome, email, setor, tipo, ativo FROM usuarios")
    result = cur.fetchall()
    conn.close()
    return result

def criar_usuario_db(nome, email, senha_hash, setor, tipo, ativo=True):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO usuarios (nome, email, senha_hash, setor, tipo, ativo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, email, senha_hash, setor, tipo, 1 if ativo else 0))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id

# def atualizar_usuario_db(id, nome, email, setor, tipo, ativo):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         UPDATE usuarios
#         SET nome=%s, email=%s, setor=%s, tipo=%s, ativo=%s
#         WHERE id=%s
#     """, (nome, email, setor, tipo, 1 if ativo else 0, id))
#     conn.commit()
#     conn.close()

def atualizar_usuario_db(id, nome=None, email=None, setor=None, tipo=None, ativo=None):
    conn = get_db_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    # Buscar dados atuais
    cur.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
    usuario = cur.fetchone()
    if not usuario:
        conn.close()
        return False  # usuário não encontrado

    # Se algum campo não foi passado, mantém o valor atual
    nome = nome if nome else usuario["nome"]
    email = email if email else usuario["email"]
    setor = setor if setor else usuario["setor"]
    tipo = tipo if tipo else usuario["tipo"]
    ativo = ativo if ativo is not None else usuario["ativo"]

    cur = conn.cursor()
    cur.execute("""
        UPDATE usuarios
        SET nome=%s, email=%s, setor=%s, tipo=%s, ativo=%s
        WHERE id=%s
    """, (nome, email, setor, tipo, 1 if ativo else 0, id))
    conn.commit()
    conn.close()
    return True

    
def deletar_usuario_db(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conn.commit()
    conn.close()

# Rotas Flask reaproveitando as funções
@usuarios_bp.route("/", methods=["GET"])
def listar_usuarios():
    result = listar_usuarios_db()
    return jsonify(result if result else ["sem registro"]), 200

@usuarios_bp.route("/<int:id>", methods=["GET"])
def listar_usuario_por_id(id):
    conn = get_db_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT id, nome, email, setor, tipo, ativo FROM usuarios WHERE id=%s", (id,))
    usuario = cur.fetchone()
    conn.close()

    if usuario:
        return jsonify(usuario), 200
    else:
        return jsonify({"message": f"Usuário {id} não encontrado"}), 404


@usuarios_bp.route("/", methods=["POST"])
def criar_usuario():
    data = request.get_json(force=True)
    user_id = criar_usuario_db(
        data["nome"], data["email"], data["senha_hash"],
        data.get("setor", ""), data.get("tipo", "Solicitante"),
        data.get("ativo", True)
    )
    return jsonify({"message": "Usuário criado", "id": user_id}), 201

@usuarios_bp.route("/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    data = request.get_json(force=True)
    atualizar_usuario_db(
        id,
        data.get("nome"),
        data.get("email"),
        data.get("setor"),
        data.get("tipo"),
        data.get("ativo", True)
    )
    return jsonify({"message": f"Usuário {id} atualizado com sucesso"}), 200

@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    deletar_usuario_db(id)
    return jsonify({"message": f"Usuário {id} deletado com sucesso"}), 200
