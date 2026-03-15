from flask import Flask, jsonify, request
from banco import criar_tabela, inicializar_banco

app = Flask(__name__)
app.json.sort_keys = False
criar_tabela()

@app.route("/")
def home():
    return jsonify({
        "mensagem": "Bem-vindo à API de Tarefas!",
        "como_criar_tarefa": {
            "metodo": "POST",
            "endpoint": "/tarefas",
            "headers": {
                "Content-Type": "application/json"
            },
            "body_exemplo": {
                "titulo": "Estudar Flask",
                "tempo_gasto": 60,
                "dia_semana": "segunda",
                "concluida": 0
            }
        }
    })

@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    conexao = inicializar_banco()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM tarefas")
        resultados = cursor.fetchall()
        
        tarefas = [
            {
                "id": tarefa[0],
                "titulo": tarefa[1],
                "tempo_gasto": tarefa[2],
                "dia_semana": tarefa[3],
                "concluida": tarefa[4]
            }
            for tarefa in resultados
        ]
    finally:
        conexao.close()
        return jsonify(tarefas)
        
@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    conexao = inicializar_banco()
    try:
        cursor = conexao.cursor()
        dados = request.get_json()
        cursor.execute("INSERT INTO tarefas (titulo, tempo_gasto, dia_semana, concluida) VALUES (?, ?, ?, ?)",
                       (dados["titulo"], dados["tempo_gasto"], dados["dia_semana"], dados["concluida"]))
        conexao.commit()
        return jsonify({"mensagem": "Tarefa criada com sucesso!"}), 201
    finally:
        conexao.close()
        
@app.route("/tarefas/<int:id>", methods=["PUT"])
def atualizar_tarefa(id):
    conexao = inicializar_banco()
    try:
        cursor = conexao.cursor()
        dados = request.get_json(silent=True)
        if not dados:
            return jsonify({"mensagem": "Envie um JSON válido no corpo da requisição"}), 400
        cursor.execute(
            "UPDATE tarefas SET titulo = ?, tempo_gasto = ?, dia_semana = ?, concluida = ? WHERE id = ?",
            (dados["titulo"], dados["tempo_gasto"], dados["dia_semana"], dados["concluida"], id)
            )
        conexao.commit()
        return jsonify({"mensagem": "Tarefa atualizada com sucesso!"})
    finally:
        conexao.close()

@app.route("/tarefas", methods=["PUT"])
@app.route("/tarefas/", methods=["PUT"])
def atualizar_tarefa_sem_id():
    return jsonify({"mensagem": "Informe o ID na URL para atualizar. Exemplo: /tarefas/1"}), 400
        
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def deletar_tarefa(id):
    conexao = inicializar_banco()
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))
        conexao.commit()
        return jsonify({"mensagem": "Tarefa deletada com sucesso!"})
    finally:
        conexao.close()

@app.route("/tarefas", methods=["DELETE"])
@app.route("/tarefas/", methods=["DELETE"])
def deletar_tarefa_sem_id():
    return jsonify({"mensagem": "Informe o ID na URL para deletar. Exemplo: /tarefas/1"}), 400
    
if __name__ == "__main__":
    app.run(debug=True)
