from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Configuração de conexão com o banco de dados SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.145\srvsql;DATABASE=TCC;UID=sa;PWD=b1admin')

# Rota para criar um novo registro
@app.route('/api/criar', methods=['POST'])
def criar_registro():
    try:
        data = request.json
        cursor = conn.cursor()
        cursor.execute("INSERT INTO LEITURA (KIT, TENSAO, CORRENTE) VALUES (?, ?, ?)", (data['kit'], data['tensao'], data['corrente']))
        conn.commit()
        return jsonify({'message': 'Registro criado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Retorna uma resposta de erro com o tipo de exceção

# Rota para listar todos os registros
@app.route('/api/listar', methods=['GET'])
def listar_registros():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LEITURA")
        registros = cursor.fetchall()
        return jsonify({'registros': [dict(zip([column[0] for column in cursor.description], row)) for row in registros]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Retorna uma resposta de erro com o tipo de exceção

# Rota para atualizar um registro por ID
@app.route('/api/atualizar/<int:id>', methods=['PUT'])
def atualizar_registro(id):
    try:
        data = request.json
        cursor = conn.cursor()
        cursor.execute("UPDATE LEITURA SET KIT = ?, TENSAO = ?, CORRENTE = ? WHERE id = ?", (data['kit'], data['tensao'], data['corrente']))
        conn.commit()
        return jsonify({'message': 'Registro atualizado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Retorna uma resposta de erro com o tipo de exceção

# Rota para excluir um registro por ID
@app.route('/api/excluir/<int:id>', methods=['DELETE'])
def excluir_registro(id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LEITURA WHERE id = ?", (id,))
        conn.commit()
        return jsonify({'message': 'Registro excluído com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Retorna uma resposta de erro com o tipo de exceção

if __name__ == '__main__':
    app.run(host='192.168.1.41', port=5000)