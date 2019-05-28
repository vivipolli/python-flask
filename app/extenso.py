from flask import Flask, request, jsonify

app = Flask(__name__)


unid = ("zero", "um", "dois", "três", "quatro",
        "cinco", "seis", "sete", "oito",
        "nove", "dez", "onze", "doze", "treze", "quatorze", "quinze",
        "dezesseis", "dezessete", "dezoito", "dezenove")
dezen = ["", "", "vinte", "trinta", "quarenta",
         "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
centen = ["", "cem", "duzentos", "trezentos", "quatrocentos", "quinhentos",
          "seiscentos", "setecentos", "oitocentos", "novecentos"]


def first_numbers(num):
    result = unid[num]

    return result


def two_numbers(num):
    if num % 10 == 0:
        a = num // 10
        result = dezen[a]
    else:
        a = num // 10
        b = num % 10
        result = dezen[a] + " e " + unid[b]

    return result


def three_numbers(num):
    if num % 100 == 0:
        a = num // 100
        result = centen[a]
    else:
        a = num // 100
        b = num % 100
        if b < 20:
            c = first_numbers(b)
        else:
            c = two_numbers(b)
        result = centen[a] + " e " + c

    return result


def four_numbers(num):
    if num % 1000 == 0:
        a = num // 1000
        if a < 20:
            tpl = first_numbers(a)
        else:
            tpl = two_numbers(a)
        result = tpl + " mil"
    else:
        a = num // 1000
        if a < 20:
            tpl = first_numbers(a)
        else:
            tpl = two_numbers(a)
        rest = num % 1000
        c = three_numbers(rest)
        result = tpl + " mil" + c

    return result


@app.route('/<int(signed=True):num>', methods=['GET'])
def input_func(num):
    if 0 <= num < 20 or -20 < num < 0:
        if num > 0:
            result = first_numbers(num)
        else:
            num = num * (-1)
            result = "menos " + first_numbers(num)
    elif 20 <= num <= 99 or -99 <= num <= -20:
        if num > 0:
            result = two_numbers(num)
        else:
            num = num * (-1)
            result = "menos " + two_numbers(num)
    elif 100 <= num <= 999 or -999 <= num <= -100:
        if num > 0:
            result = three_numbers(num)
        else:
            num = num * (-1)
            result = "menos " + three_numbers(num)
    elif 1000 <= num <= 99999 or -99999 <= num <= -1000:
        if num > 0:
            result = four_numbers(num)
        else:
            num = num * (-1)
            result = "menos " + four_numbers(num)
    else:
        result = "Você deve digitar um número entre [-99999, 99999]"

    return jsonify(extenso=result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)
