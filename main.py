from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

livros = []
contador_id = 1

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/livros')
def listar_livros():
    return render_template('livro.html', livros=livros)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    global contador_id
    if request.method == 'POST':
        novo = {
            'id': contador_id,
            'titulo': request.form['titulo'],
            'autor': request.form['autor'],
            'emprestado': False,
            'data_emprestimo': None,
            'data_devolucao': None,
            'multa': 0
        }
        livros.append(novo)
        contador_id += 1
        return redirect(url_for('listar_livros'))
    return render_template('adicionar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    livro = next((l for l in livros if l['id'] == id), None)
    if request.method == 'POST':
        livro['titulo'] = request.form['titulo']
        livro['autor'] = request.form['autor']
        return redirect(url_for('listar_livros'))
    return render_template('adicionar.html', livro=livro)

@app.route('/excluir/<int:id>')
def excluir(id):
    global livros
    livros = [l for l in livros if l['id'] != id]
    return redirect(url_for('listar_livros'))

@app.route('/emprestar/<int:id>')
def emprestar(id):
    for livro in livros:
        if livro['id'] == id:
            hoje = datetime.now().date()
            devolucao = hoje + timedelta(days=7)
            livro['emprestado'] = True
            livro['data_emprestimo'] = str(hoje)
            livro['data_devolucao'] = str(devolucao)
            livro['multa'] = 0
            break
    return redirect(url_for('listar_livros'))

@app.route('/devolver/<int:id>')
def devolver(id):
    for livro in livros:
        if livro['id'] == id and livro['emprestado']:
            hoje = datetime.now().date()
            data_dev = datetime.strptime(livro['data_devolucao'], '%Y-%m-%d').date()
            atraso = (hoje - data_dev).days
            multa = 0
            if atraso > 0:
                multa = 10 + (0.01 * atraso * 10)
            livro['emprestado'] = False
            livro['data_emprestimo'] = None
            livro['data_devolucao'] = None
            livro['multa'] = round(multa, 2)
            break
    return redirect(url_for('listar_livros'))

if __name__ == '__main__':
    app.run(debug=True)
