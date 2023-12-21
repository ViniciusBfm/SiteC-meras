from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco_de_dados.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    nome = db.Column(db.String(50))
    dvr = db.Column(db.String(50))
    posicao = db.Column(db.String(50))


# Rota para exibir o formulário de login
@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def exibir_login():
    db.create_all()
    return render_template('login.html')

# Rota para processar os dados do formulário de login
@app.route("/", methods=["POST"])
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        nome = request.form.get('usuario')
        senha = request.form.get('senha')

        if nome == 'admin' and senha == 'acbeubv20':
            # Armazenar o nome do usuário na sessão
            session['username'] = nome
            # Redirecionar para a rota '/home' após o login bem-sucedido
            return redirect("/home")
        else:
            mensagem = "Senha ou usuário incorreto. Tente novamente."

        return render_template("login.html", mensagem=mensagem)

    return render_template('login.html')

# Rota para a página inicial
# Rota para a página inicial
@app.route("/home", methods=['GET', 'POST'])
def home():
    # Verificar se o usuário está logado
    if 'username' in session:
        # Obter o nome do usuário da sessão
        nome_usuario = session['username']
        
        if request.method == 'POST':
            # Processar o formulário de adição de usuário
            ip = request.form['ip']
            nome = request.form['nome']
            dvr = request.form['dvr']
            posicao = request.form['posicao']

            user = User(ip=ip, nome=nome, dvr=dvr, posicao=posicao)
            db.session.add(user)
            db.session.commit()

            # Redirecionar após a adição bem-sucedida
            return redirect("/home")
        
        # Obter a lista de usuários
        users = User.query.all()

        # Renderizar a página home
        return render_template("home.html", nome=nome_usuario, users=users)
    else:
        # Se não estiver logado, redirecionar para a página de login
        return redirect("/login")

# Rota para excluir um usuário
@app.route("/delete_user/<int:user_id>", methods=['GET'])
def delete_user(user_id):
    # Verificar se o usuário está logado
    if 'username' in session:
        # Obter o usuário pelo ID
        user = User.query.get(user_id)

        # Verificar se o usuário existe
        if user:
            # Remover o usuário do banco de dados
            db.session.delete(user)
            db.session.commit()

    # Redirecionar de volta para a página home
    return redirect("/home")
@app.route("/edit_user/<int:user_id>", methods=['POST'])
def edit_user(user_id):
    if 'username' in session:
        user = User.query.get(user_id)
        if user:
            user.ip = request.form['ip']
            user.nome = request.form['nome']
            user.dvr = request.form['dvr']
            user.posicao = request.form['posicao']
            db.session.commit()
    return redirect("/home")

if __name__ == "__main__":
    app.run(host='192.168.8.47', port=5000, debug=True)
    