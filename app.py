from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produto.db'  # Configuração do banco de dados SQLite
db = SQLAlchemy(app)


# Definição da classe de modelo para os produtos
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)


# Rota para pagina principal
@app.route('/')
def index():
    return render_template('index.html')


# Rota para criar um novo produto
@app.route('/criar_produto', methods=['GET', 'POST'])
def criar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])

        novo_produto = Produto(nome=nome, descricao=descricao, preco=preco)
        db.session.add(novo_produto)
        db.session.commit()
        return "Produto criado com sucesso{}".format(render_template('return.html'))  # retorna os dois botões

    return render_template('criar_produto.html')


# Rota para listar todos os produtos
@app.route('/produto')
def listar_produtos():
    produto = Produto.query.all()
    return render_template('lista_produto.html', produto=produto)


# Rota para visualizar detalhes de um produto por ID
@app.route('/produto/<int:produto_id>')
def visualizar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return render_template('visualizar_produto.html', produto=produto)


# Rota para editar um produto por ID
@app.route('/editar_produto/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.preco = float(request.form['preco'])
        db.session.commit()
        return "Produto editado com sucesso!{}".format(render_template('return.html')) # retorna os dois botões

    return render_template('editar_produto.html', produto=produto)


# Rota para deletar um produto por ID
@app.route('/deletar_produto/<int:produto_id>', methods=['GET', 'POST'])
def deletar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    if request.method == 'POST':
        db.session.delete(produto)
        db.session.commit()
        return "Produto deletado com sucesso! {}".format(render_template('return.html')) # retorna os dois botões

    return render_template('deletar_produto.html', produto=produto)


# Criação das tabelas no banco de dados e execução da aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados, se não existirem
    app.run(debug=True)  # Inicia o servidor Flask em modo de depuração
