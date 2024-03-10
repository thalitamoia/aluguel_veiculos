from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import re
import json

# Criar uma instância do SQLAlchemy
db = SQLAlchemy()

# Função para criar o aplicativo Flask
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'NIGHTWOLF'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veiculos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar a aplicação do SQLAlchemy com o app Flask
    db.init_app(app)

    # Definir o modelo de dados para as opções de pesquisa do veículo
    class OpcoesVeiculo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        tipo = db.Column(db.String(50))
        marca = db.Column(db.String(100))
        modelo = db.Column(db.String(100))
        transmissao = db.Column(db.String(20))
        numero_pessoas = db.Column(db.Integer)
        tipo_veiculo = db.Column(db.String(50))

    # Página inicial direcionada para o login
    @app.route('/', methods=['GET','POST'])
    def home():
        return render_template('login.html')

    # Rota para o login
    @app.route('/login', methods=['POST'])
    def login():
        email = request.form.get('email')
        senha = request.form.get('senha')
        with open('usuarios.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)
            cont = 0
            for usuario in usuarios:
                cont += 1
                if usuario['email'] == email and usuario['senha'] == senha:
                    return render_template('veiculos.html')
                if cont >= len(usuarios):
                    flash('Usuario Inválido')
                    return redirect('/')

    # Rota para redirecionar para o cadastro
    @app.route('/cadastro_user', methods=['GET', 'POST'])
    def cadastro_user():
        if request.method == 'GET':
            return render_template('cadastro.html')
        elif request.method == 'POST':
            return cadastrarUsuario()

    # Página de cadastro
    @app.route('/cadastro')
    def cadastro():
        return render_template('cadastro.html')

    # Rota para cadastrar usuário
    @app.route("/cadastro", methods=['POST'])
    def cadastrarUsuario():
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirm_senha = request.form.get('conf_senha')

        if senha != confirm_senha:
            return render_template('cadastro.html', erro='As senhas não coincidem. Tente novamente.')

        # Verifica se a senha é forte
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}:<>?]).{8,}$", senha):
            return render_template('cadastro.html', erro='A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.')

        user = {
            'nome': nome,
            'email': email,
            'senha': senha
        }

        with open('usuarios.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)
            for usuario in usuarios:
                if usuario['email'] == email:
                    return render_template('cadastro.html', erro='Este email já está cadastrado')

        usuarios.append(user)

        with open('usuarios.json', 'w') as gravarUser:
            json.dump(usuarios, gravarUser, indent=4)

        return render_template('login.html')

    # Rota para a página inicial (formulário de pesquisa)
    @app.route('/pesquisa-veiculo', methods=['GET', 'POST'])
    def pagina_de_pesquisa():
        if request.method == 'GET':
            return render_template('pesquisar-veiculo.html')
        elif request.method == 'POST':
            return pesquisar_veiculo()

    # Rota para salvar as opções de pesquisa do veículo
    @app.route('/salvar-veiculo', methods=['POST'])
    def salvar_opcoes_veiculo():
        tipo = request.form.get('tipo')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        transmissao = request.form.get('transmissao')
        numero_pessoas = request.form.get('numero_pessoas')
        tipo_veiculo = request.form.get('tipo_veiculo')

        opcoes_veiculo = OpcoesVeiculo(
            tipo=tipo,
            marca=marca,
            modelo=modelo,
            transmissao=transmissao,
            numero_pessoas=numero_pessoas,
            tipo_veiculo=tipo_veiculo
        )

        db.session.add(opcoes_veiculo)
        db.session.commit()  # Aqui está o commit após adicionar o objeto ao banco de dados

        flash('Opções de veículo salvas com sucesso!')

        return redirect(url_for('pagina_de_pesquisa'))

    # Função para pesquisar veículos
    def pesquisar_veiculo():
        # Adicione aqui a lógica para pesquisar veículos
        return 'Página de resultado da pesquisa'

    return app

# Seu código existente...

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados
    app.run(debug=True)
