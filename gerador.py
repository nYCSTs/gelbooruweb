import requests
from bs4 import BeautifulSoup 
import numpy as np 
import math

#TROCA SIMBOLOS COMO ; PELOS CORRETOS
def arrumarSimbolos(name):
    orig = ('(',   ')',   '!',   '/',   ':',   '?',   "'",   ';', '+')
    new = ('%28', '%29', '%21', '%2f', '%3a', '%3f', '%27', '%3b', '%2b')
    troca = zip(orig, new)
    for orig, new in troca:
        name = name.replace(orig, new)
    return name

#FORMA A URL
def obterURL(name, rating, tags):
    origUrl = 'https://gelbooru.com/index.php?page=post&s=list&tags='
    parteNome = arrumarSimbolos(name.replace(' ', '_')) + '+' 
    for tag in tags:
        parteTags = tag.strip().replace(' ', '_') + '+'

    url = origUrl + parteNome + rating + parteTags
    if (verificarValidade(obterHTML(url))):
        return url
    elif (name != ''):
        name = name.split(' ')
        if (len(name) == 2):
            parteNome = arrumarSimbolos(name[1] + '_' + name[0]) + '+'
            url = origUrl + parteNome + rating + parteTags
            if (verificarValidade(obterHTML(url))):
                return url
    return -1

#GERA HTML
def obterHTML(url):
    cookies = {"fringeBenefits":"yup", "resize-original":"1", "resize-notification":"1"}
    r = requests.get(url, cookies=cookies)
    content = r.text
    r.close()
    return BeautifulSoup(content, 'html.parser')

#QUANTIDADE DE PAGINAS
def obterQuantidadeDePaginas(html):
    element = str(html.find_all('div', 'pagination')).split('<a ')[-1]
    if (element.find('last page') != -1):
        quantidade = element[element.find('&amp;pid=') + 9:element.find('">»</a>')]
        quantidade = (int(quantidade) / 42) + 1
        if quantidade > 477:
            return 477
        else:
            return quantidade
    elif (element.find('<b>1</b>') != -1):
        return 1
    else:
        quantidade = int(element[element.rfind('">') + 2:element.find('</a>')])
        return quantidade

#QUANTIDADE TOTAL DE IMAGENS
def obterQuantidadeDeImagens(url, quantidadeDePaginas):
    url += f'&pid={(quantidadeDePaginas - 1) * 42}'
    html = obterHTML(url)
    element = str(html.find('div', class_='thumbnail-container')).split('</a>')
    return int(len(element) + ((quantidadeDePaginas - 1) * 42) - 1)

#VERIFICA SE O PERSONAGEM EXISTE
def verificarValidade(html):
    if str(html).find('Nobody here but us chickens!') != -1:
        return False
    else:
        return True

#OBTEM O LINK DA IMAGEM RANDOM
def obterImagemRandomica(origUrl):
    if origUrl == -1:
        return origUrl
    html = obterHTML(origUrl)
    qntImagens = obterQuantidadeDeImagens(origUrl, obterQuantidadeDePaginas(html))
    imagens = np.arange(0, qntImagens)

    imagemSorteada = int(np.random.choice(imagens, 1))
    #REMOVE DA LISTA DE IMAGENS
    imagens = np.delete(imagens, np.argwhere(imagens == imagemSorteada))
    
    imagem, pagina = math.modf(imagemSorteada / 42.0)
    imagem = round(imagem * 42)

    # CONSTROI URL
    url = origUrl + '&pid=' + str((pagina - 1) * 42)

    # OBTEM HTML(1) E DEPOIS PEGA A PARTE DAS IMAGENS(2)
    html = obterHTML(url)
    element = str(html.findAll('div', class_ = 'thumbnail-container')).split('thumbnail-preview')[1:]
    
    element = str(element[imagem])
    code = element[element.find(';id=') + 4:element.find('&amp;tags=')]
    urlPost = 'https://gelbooru.com/index.php?page=post&s=view&id=' + code

    # URL DO POST RANDOMICO OBTIDO
    html = obterHTML(urlPost)

    # GERA O LINK FINAL DA IMAGEM
    img_link = str(html.findAll('meta', property = 'og:image'))
    img_link = img_link[img_link.find('content') + 9:img_link.find('property') - 2]

    return {'linkPostOriginal':urlPost, 'enderecoFinal':img_link}

class URL():
    def __init__(self, name, rating, tags):
        self.name = name
        self.rating = rating
        self.tags = tags
    def link(self):
        self.resultado = obterImagemRandomica(obterURL(self.name, self.rating, self.tags))
