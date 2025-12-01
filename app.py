## Sistema de Gestão de Notas dos Alunos

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# Entrada dos dados gerais do sistema

# 5 disciplinas fixas
disciplinas = [
    "Matemática:",
    "Português:", 
    "História:",
    "Geografia:",
    "Biologia:"
]

# 3 alunos cadastrados 
alunos = [
    {
        "id": 1,
        "nome": "",
        "notas": [],  
        "frequencia": None  
    },
    {
        "id": 2,
        "nome": "",
        "notas": [],
        "frequencia": None
    },
    {
        "id": 3,
        "nome": "",
        "notas": [],
        "frequencia": None
    }
]

professores = {
    "email": "administrador@teste.com",
    "senha": "teste123456"
}


# Login para professores
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    professor_fixo = {
        "email": "administrador@teste.com",
        "senha": "teste123456"
    }

    if email != professor_fixo["email"]:
        return jsonify({"message": "E-mail não cadastrado"}), 400

    if senha != professor_fixo["senha"]:
        return jsonify({"message": "Senha incorreta"}), 401

    return jsonify({"message": "Login autorizado"}), 200




#PUT /alunos/<id> - Atualizar notas e frequência
@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
    dados = request.json

    # Encontrar o aluno
    aluno = next((a for a in alunos if a['id'] == aluno_id), None)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    # Verifica se nome foi enviado
    nome = dados.get('nome')
    if not nome or nome.strip() == "":
        return jsonify({"erro": "O nome do aluno é obrigatório"}), 400

    # Verifica se notas foi enviado
    notas = dados.get('notas')
    if not notas:
        return jsonify({"erro": "As notas devem ser enviadas"}), 400

    # Verifica se é uma lista
    if not isinstance(notas, list):
        return jsonify({"erro": "Notas deve ser uma lista com 5 valores"}), 400

    # Verifica quantidade de notas
    if len(notas) != 5:
        return jsonify({"erro": "Devem existir exatamente 5 notas"}), 400

    # Verifica valores entre 0 e 10
    for nota in notas:
        if not isinstance(nota, (int, float)):
            return jsonify({"erro": "Todas as notas devem ser números"}), 400
        if not (0 <= nota <= 10):
            return jsonify({"erro": "Notas devem estar entre 0 e 10"}), 400

    # Verifica frequência
    frequencia = dados.get('frequencia')
    if frequencia is None:
        return jsonify({"erro": "A frequência é obrigatória"}), 400

    if not isinstance(frequencia, (int, float)):
        return jsonify({"erro": "Frequência deve ser um número"}), 400

    if not (0 <= frequencia <= 100):
        return jsonify({"erro": "Frequência deve estar entre 0 e 100"}), 400

    aluno['nome'] = nome
    aluno['notas'] = notas
    aluno['frequencia'] = frequencia

    return jsonify({
        "mensagem": f"Dados de {aluno['nome']} atualizados com sucesso",
        "aluno": aluno
    }), 200


# GET /estatisticas - Calcular tudo
@app.route('/estatisticas', methods=['GET'])
def calcular_estatisticas():
    # Verificar se todos os alunos têm dados preenchidos
    alunos_completos = [a for a in alunos if len(a['notas']) == 5 and a['frequencia'] is not None]
    
    if len(alunos_completos) == 0:
        return jsonify({"erro": "Nenhum aluno com dados completos"}), 400
    
    # 1. Calcular média de cada aluno
    resultado_alunos = []
    for aluno in alunos_completos:
        media = sum(aluno['notas']) / len(aluno['notas'])
        resultado_alunos.append({
            "nome": aluno['nome'],
            "media": round(media, 2),
            "frequencia": aluno['frequencia']
        })
    
    # 2. Calcular média geral da turma (média de todas as médias dos alunos)
    todas_medias = [item['media'] for item in resultado_alunos]
    media_geral_turma = sum(todas_medias) / len(todas_medias)
    
    # 3. Calcular média por disciplina
    medias_por_disciplina = []
    for i in range(5):
        notas_disciplina = [aluno['notas'][i] for aluno in alunos_completos]
        media_disc = sum(notas_disciplina) / len(notas_disciplina)
        medias_por_disciplina.append({
            "disciplina": disciplinas[i],
            "media": round(media_disc, 2)
        })
    
    # 4. Alunos com média ACIMA da média geral da turma
    alunos_acima_media = []
    for item in resultado_alunos:
        if item['media'] > media_geral_turma:
            alunos_acima_media.append({
                "nome": item['nome'],
                "media": item['media']
            })
    
    # 5. Alunos com frequência ABAIXO de 75%
    alunos_frequencia_baixa = []
    for item in resultado_alunos:
        if item['frequencia'] < 75:
            alunos_frequencia_baixa.append({
                "nome": item['nome'],
                "frequencia": item['frequencia']
            })
    
    # Retornar tudo
    return jsonify({
        "alunos": resultado_alunos,
        "media_geral_turma": round(media_geral_turma, 2),
        "media_por_disciplina": medias_por_disciplina,
        "alunos_acima_media": alunos_acima_media if alunos_acima_media else [],
        "alunos_frequencia_baixa": alunos_frequencia_baixa if alunos_frequencia_baixa else []
    }), 200


if __name__ == '__main__':
    app.run(debug=True)