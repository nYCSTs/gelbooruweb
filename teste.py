lista = [{'linkPostOriginal':'A', 'enderecoFinal':'1'}, {'linkPostOriginal':'B', 'enderecoFinal':'2'}, {'linkPostOriginal':'C', 'enderecoFinal':'3'}]

def teste(quantidade, quantidadeTotal, lista):
    if (quantidade < quantidadeTotal):
        teste(quantidade + 1, quantidadeTotal, lista)
    print(lista[quantidadeTotal - quantidade]['enderecoFinal'])

teste(0, 2, lista)