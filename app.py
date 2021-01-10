from flask import Flask, render_template, request, redirect, url_for
from gerador import URL
import webbrowser
import time
import requests
from bs4 import BeautifulSoup

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

        if (resultados == -1):
            return '<h1 style="text-align: center;">Personagem invalido clique <a href="/">aqui</a> para voltar.<br>Experimente inverter o nome do personagem/anime.</h1>'

        return redirect(resultados['enderecoFinal'])
        #return render_template('imagensResultados.html', resultados = resultados)
    else:
        return render_template('index.html')


@app.route('/buscador', methods = ['POST', 'GET'])
def buscarTag():
    if request.method == 'POST':
        tag = request.form['campo-busca']
        url = 'https://gelbooru.com/index.php?page=tags&s=list&tags=' + tag + '*&sort=desc&order_by=index_count'
        
        r = requests.get(url)
        html = BeautifulSoup(r.text, 'html.parser')
        html = str(html.find_all('table', class_='highlightable')[0])
        return render_template('tagsResultados.html', html = html)
    else:
        return render_template('buscadorTags.html')


if __name__ == '__main__':
    app.run(debug=True)

# Adicionar pagina de ajuda
# Adicionar pagina de tags         X