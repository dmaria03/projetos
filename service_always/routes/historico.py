from flask import Blueprint, jsonify
from routes.usuarios import Usuario

historico_bp = Blueprint("historico", __name__)

# listar chamados por pessoa (ORM)
@historico_bp.route("/historico/chamados-por-pessoa", methods=["GET"])
def chamados_por_pessoa():
    usuarios = Usuario.query.all()

    resultado = []

    for usuario in usuarios:
        chamados = []

        for chamado in usuario.chamados:
            chamados.append({
                "chamado_id": chamado.id,
                "titulo": chamado.titulo,
                "status": chamado.status,
                "prioridade": chamado.prioridade,
                "setor": chamado.setor,
                "categoria": chamado.categoria,
                "data_abertura": chamado.data_abertura
            })

        resultado.append({
            "usuario_id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo": usuario.tipo,
            "total_chamados": len(chamados),
            "chamados": chamados
        })

    return jsonify(resultado), 200
