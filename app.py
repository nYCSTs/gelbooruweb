from flask import Flask, render_template, request, redirect, url_for
from gerador import URL
import time
import requests
from bs4 import BeautifulSoup
import sys

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if (request.method == 'POST'):
        resultados = []
        name = request.form['nome'].strip()
        rating = request.form['rating'].strip()
        tags = request.form['tags'].split(', ')
        #quantidade = int(request.form['quantidade'])

        gelbooru = URL(name = name, rating = rating, tags = tags)
        gelbooru.link()
        resultados = gelbooru.resultado

        sys.stdout.write(f'name: {name} | rating: {rating} | tags: {tags}')

        if (resultados == -1):
            return '<h1 style="text-align: center;">Personagem invalido clique <a href="/">aqui</a> para voltar.<br>Experimente usar a <a href="https://gelboorusearcher.herokuapp.com/buscador">pesquisa de tags</a> para verificar pelo personagem desejado.</h1>'

        return redirect(resultados['enderecoFinal'])
        #return render_template('imagensResultados.html', resultados = resultados)
    else:
        return render_template('index.html')


@app.route('/buscador', methods = ['POST', 'GET'])
def buscarTag():
    if request.method == 'POST':
        tag = request.form['campo-busca']
        url = 'https://gelbooru.com/index.php?page=tags&s=list&tags=' + tag + '*&sort=desc&order_by=index_count'
        
        sys.stdout.write(f'search: {tag}')

        r = requests.get(url)
        html = BeautifulSoup(r.text, 'html.parser')
        html = str(html.find_all('table', class_='highlightable')[0])
        return render_template('tagsResultados.html', html = html)
    else:
        return render_template('buscadorTags.html')


if __name__ == '__main__':
    app.run(debug=True)