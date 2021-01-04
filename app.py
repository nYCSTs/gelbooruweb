from flask import Flask, render_template, request, redirect
from gerador import URL

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if (request.method == 'POST'):
        name = request.form['nome'].strip()
        rating = request.form['rating'].strip()
        tags = request.form['tags'].split(', ')

        gelbooru = URL(name = name, rating = rating, tags = tags)
        gelbooru.link()
        link = gelbooru.url
        if (link == -1):
            return '<h1 style="text-align: center;">Personagem invalido clique <a href="/">aqui</a> para voltar.<br>Experimente inverter o nome do personagem/anime.</h1>'
        else:
            return redirect(link, code=302)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)