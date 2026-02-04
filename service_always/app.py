from flask import Flask
import pymysql
import threading
from config import Config
from routes.usuarios import usuarios_bp
from cli import menu_usuarios   # importa o menu do cli.py


app = Flask(__name__)
app.config.from_object(Config)

# Registrar blueprint
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")


# Função para obter conexão com MySQL
def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# Rota para testar conexão#
@app.route('/testdb')
def test_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT NOW()")  # Hora atual do servidor MySQL
    result = cur.fetchone()
    conn.close()
    return f"Conexão OK! Hora do servidor MySQL: {result[0]}"

def run_flask():
    # roda o servidor Flask em uma thread separada
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    #print("=== Iniciando servidor Flask em paralelo ===")
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # encerra junto com o programa principal
    flask_thread.start()

    print("=== Iniciando prompt de usuários ===")
    menu_usuarios()




# if __name__ == "__main__":
#     print("=== Iniciando a aplicação API ===")
#     app.run(host="0.0.0.0", port=5000)

#     print("=== Iniciando a aplicação ===")
#     menu_usuarios()