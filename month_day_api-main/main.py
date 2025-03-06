from flask import Flask, jsonify, request
from datetime import date, timedelta
from workalendar.america import Brazil

app = Flask(__name__)

cal = Brazil()

def calcular_dias_uteis_no_intervalo(data_inicio, data_fim):
    dias_uteis = 0
    data_atual = data_inicio
    while data_atual <= data_fim:
        if cal.is_working_day(data_atual):
            dias_uteis += 1
        elif data_atual.weekday() == 5:
            dias_uteis += 0.5
        data_atual += timedelta(days=1)
    return dias_uteis

@app.route('/dias-uteis', methods=['GET'])
def calcular_dias_uteis():
    try:
        
        mes = request.args.get('mes', type=int)
        ano = request.args.get('ano', type=int)

        hoje = date.today()
        if not mes:
            mes = hoje.month
        if not ano:
            ano = hoje.year

        primeiro_dia_mes = date(ano, mes, 1)
        ultimo_dia_mes = (primeiro_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)

      
        dias_uteis = calcular_dias_uteis_no_intervalo(primeiro_dia_mes, ultimo_dia_mes)

      
        hoje_no_mes = max(primeiro_dia_mes, hoje) 
        dias_trabalhados = calcular_dias_uteis_no_intervalo(primeiro_dia_mes, hoje_no_mes)
        dias_restantes = calcular_dias_uteis_no_intervalo(hoje_no_mes + timedelta(days=1), ultimo_dia_mes)

        resultado = {
            "ano": ano,
            "mes": mes,
            "dias_uteis": dias_uteis,
            "dias_uteis_trabalhados": dias_trabalhados,
            "dias_uteis_restantes": dias_restantes,
        }

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')