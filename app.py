from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Listar todos os itens
@app.route('/itens', methods=['GET'])
def listar_itens():
    conn = get_db()
    itens = conn.execute('SELECT * FROM Insumo').fetchall()
    conn.close()
    return jsonify([dict(item) for item in itens])

# Adicionar novo item
@app.route('/itens', methods=['POST'])
def adicionar_item():
    # Pega os dados do formulário
    nome = request.form.get('nome')
    quantidade = request.form.get('quantidade')
    descricao = request.form.get('descricao')
    fornecedor = request.form.get('fornecedor')
    status = request.form.get('status')

    # Conecta ao banco e adiciona o item
    conn = get_db()
    try:
        conn.execute('''
            INSERT INTO Insumo (nomeInsumo, QtdInsumo, descricaoInsumo, fornecedor, Status)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, quantidade, descricao, fornecedor, status))
        conn.commit()
        return jsonify({"mensagem": "Item adicionado com sucesso!"})
    except Exception as e:
        return jsonify({"erro": "Erro ao adicionar item"}), 400
    finally:
        conn.close()

# Excluir item
@app.route('/itens/<int:id>', methods=['DELETE'])
def excluir_item(id):
    conn = get_db()
    try:
        conn.execute('DELETE FROM Insumo WHERE idInsumo = ?', (id,))
        conn.commit()
        return jsonify({"mensagem": "Item excluído com sucesso!"})
    except Exception as e:
        return jsonify({"erro": "Erro ao excluir item"}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)