# Conversão de números inteiros para extensos
Este é um pequeno servidor http usando Flask para converter um número inteiro positivo ou negativo em números extensos dentro do intervalo [-99999, 99999]

Exemplo:
```
$ curl http://localhost:3000/-1042
{ "extenso": "menos mil e quarenta e dois" }
```
## Requisitos
Assumindo que temos o python 3, virtualenv e pip já instalados, vamos criar e ativar nossa variável de ambiente para isolar a aplicação:
```
$ virtualenv -p python3 env
$ source env/bin/activate
```
Instalando o flask com pip...
```
$ pip install flask
```
## Criando o código
Crie um arquivo python e no ínicio faça as importações do flask, do _request_ para utilizarmos a requisição http e jsonify para retornarmos a requisição em formato json:

_extenso.py:_
```python
from flask import Flask, request, jsonify

app = Flask(__name__)
```
Agora iremos utilizar uma tupla para unidades até o número 19 e duas listas para dezenas e centenas, esta será nossa base:
```python
unid = ("zero", "um", "dois", ... "dezoito", "dezenove")

dezen = ["", "", "vinte", "trinta", ... "noventa"]

centen = ["", "cem", "duzentos", ... "novecentos"]
```
A partir daqui criaremos 4 funções, a primeira para unidades até dezenove, a segunda para dezenas, a terceira para centenas e a quarta para milhar até o numero 99999. Em cada função haverá uma condição para verificar se o número é negativo.

Quando o número for negativo, ele irá converter para positivo para localizar a posição na tupla ou lista corretamente e então no output adicionar a palavra "menos" antes do número.

Exemplo:
```python
def first_numbers(num):
    if num > 0:
        result = unid[num]
    else num < 0:
        num = num * (-1)
        result = "menos " + unid[num]
    return result
```
A partir do número vinte, cada função irá verificar se o número é redondo(10,100..) ou não, e irá criar uma condição para adicionar a letra "e" ao resultado quando preciso.    
Exemplo:
```python
def two_numbers(num):
    if num > 0:
        if num % 10 == 0:
            a = num // 10   # parte inteira da divisão por 10
            result = dezen[a]
        else:
            a = num // 10
            b = num % 10    # parte restante da divisão por 10
            result = dezen[a] + " e " + unid[b]
    else num < 0: 
        (...)
```
E a partir da casa das centenas, vamos começar a reutilizar as funções declaradas anteriormente:

Exemplo:
```python
def three_numbers(num):
    if num > 0:
        if num % 100 == 0:
            (...)
        else:
            a = num // 100
            b = num % 100 
            if b < 20:
                c = first_numbers(b)
            else:
                c = two_numbers(b)
            result = centen[a] + " e " + c
```
### Configurando a rota 
Aqui ajustaremos o método http e o _path_, _signed_ como verdadeiro para permitir o recebimento de número negativo.
Declaramos uma função para receber o número no _path_ e retornar o valor em extenso após passar pelas condições recebendo as funções criadas anteriormente: 

```python
@app.route('/<int(signed=True):num>', methods=['GET'])
def global_func(num):
    if 0 <= num < 20 or -20 <= num < 0:
        result = first_numbers(num)
    elif 20 <= num <= 99 or -99 <= num <= -20:
        (...)
    
    return jsonify(extenso=result)    # aqui retornamos o valor no formato JSON
```

Finalizando declaramos o host e a porta do nosso servidor:
```python
(...)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)
```
