from flask import Blueprint, request, jsonify
from db import get_db_connection
import pymysql

chamados_bp = Blueprint("chamados", __name__)

# criar chamado
@chamados_bp.route("/", methods=["POST"])
def criar_chamado():
    dados = request.json

    if not dados:
        return jsonify({"erro": "Dados não enviados"}), 400

    campos_obrigatorios = [
        "titulo",
        "descricao",
        "prioridade",
        "setor",
        "categoria",
        "usuario_abertura_id"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo {campo} é obrigatório"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Verifica se o usuário existe
    cursor.execute(
        "SELECT id FROM usuarios WHERE id = %s",
        (dados["usuario_abertura_id"],)
    )
    usuario = cursor.fetchone()

    if not usuario:
        conn.close()
        return jsonify({"erro": "Usuário não encontrado"}), 404

    sql = """
        INSERT INTO chamados
        (titulo, descricao, prioridade, status, setor, categoria, usuario_abertura_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (
        dados["titulo"],
        dados["descricao"],
        dados["prioridade"],
        "Aberto",
        dados["setor"],
        dados["categoria"],
        dados["usuario_abertura_id"]
    ))

    conn.commit()
    chamado_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "mensagem": "Chamado criado com sucesso",
        "id": chamado_id
    }), 201


# listar chamados
@chamados_bp.route("/", methods=["GET"])
def listar_chamados():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM chamados")
    chamados = cursor.fetchall()

    conn.close()

    return jsonify(chamados)


# atualizar chamado
@chamados_bp.route("/<int:id>", methods=["PUT"])
def atualizar_chamado(id):
    dados = request.json

    if not dados:
        return jsonify({"erro": "Dados não enviados"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Verifica se chamado existe
    cursor.execute("SELECT id FROM chamados WHERE id = %s", (id,))
    chamado = cursor.fetchone()

    if not chamado:
        conn.close()
        return jsonify({"erro": "Chamado não encontrado"}), 404

    # =========================
    # 🔽 MUDANÇA COMEÇA AQUI
    # =========================

    status_validos = ["Aberto", "Em Atendimento", "Concluído", "Cancelado"]

    campos = []
    valores = []

    # valida e adiciona status (ENUM)
    if "status" in dados:
        if dados["status"] not in status_validos:
            conn.close()
            return jsonify({
                "erro": "Status inválido",
                "status_permitidos": status_validos
            }), 400
        campos.append("status = %s")
        valores.append(dados["status"])

    # Verifica se técnico existe (se enviado)
    if "tecnico_responsavel_id" in dados:
        if dados["tecnico_responsavel_id"] is not None:
            cursor.execute(
                "SELECT id FROM usuarios WHERE id = %s",
                (dados["tecnico_responsavel_id"],)
            )
            tecnico = cursor.fetchone()

            if not tecnico:
                conn.close()
                return jsonify({"erro": "Técnico não encontrado"}), 404

        campos.append("tecnico_responsavel_id = %s")
        valores.append(dados["tecnico_responsavel_id"])

    if not campos:
        conn.close()
        return jsonify({"erro": "Nenhum campo para atualizar"}), 400

    sql = f"""
        UPDATE chamados
        SET {', '.join(campos)}
        WHERE id = %s
    """

    valores.append(id)
    cursor.execute(sql, valores)

    # =========================
    # 🔼 MUDANÇA TERMINA AQUI
    # =========================

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Chamado atualizado com sucesso"})


# deletar chamado
@chamados_bp.route("/<int:id>", methods=["DELETE"])
def deletar_chamado(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica se existe antes de deletar
    cursor.execute("SELECT id FROM chamados WHERE id = %s", (id,))
    chamado = cursor.fetchone()

    if not chamado:
        conn.close()
        return jsonify({"erro": "Chamado não encontrado"}), 404

    cursor.execute("DELETE FROM chamados WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Chamado deletado com sucesso"})
