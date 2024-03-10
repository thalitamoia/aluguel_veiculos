from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veiculos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    transmissao = db.Column(db.String(20))
    numero_pessoas = db.Column(db.Integer)
    tipo_veiculo = db.Column(db.String(50))

@app.route('/salvar-veiculo', methods=['POST'])
def salvar_veiculo():
    data = request.json
    with app.app_context():  # Garantindo que estamos dentro do contexto da aplicação
        veiculo = Veiculo(
            tipo=data['tipo'],
            marca=data['marca'],
            modelo=data['modelo'],
            transmissao=data['transmissao'],
            numero_pessoas=data['numero_pessoas'],
            tipo_veiculo=definir_tipo_veiculo(data)
        )
        db.session.add(veiculo)
        db.session.commit()
    return jsonify({'message': 'Veículo salvo com sucesso!', 'tipo_veiculo': veiculo.tipo_veiculo})

def definir_tipo_veiculo(data):
    tipo_veiculo = "Outro"
    if data['tipo'] == 'carro':
        if data['numero_pessoas'] <= 5:
            tipo_veiculo = "SUV" if data['transmissao'] == "automatico" else "Carro Pequeno"
        else:
            tipo_veiculo = "Carro Médio" if data['transmissao'] == "automatico" else "Carro de Luxo"
    elif data['tipo'] == 'moto':
        tipo_veiculo = "Moto"
    return tipo_veiculo

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
