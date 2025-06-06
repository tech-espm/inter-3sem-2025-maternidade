from flask import Flask, render_template, json, request, Response
import config
import requests
import banco
from datetime import datetime
import flask_socketio

app = Flask(__name__)
socketio = flask_socketio.SocketIO(app, cors_allowed_origins="*")

#rotas flask

@app.get('/monitoramento')
def monitoramento():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/monitoramento.html', hoje=hoje)

@app.get('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

@app.get('/analise')
def analise():
    return render_template('analise.html', titulo='Análise Gráfica')

@app.get('/')
def index():
    return render_template('index/landing.html', titulo='Landing Page')

@app.get('/status')
def azul():
    return render_template('index/status.html', titulo='Status')


@app.get('/obterDados')
def obterDados():
    # Obter o maior id do banco
    maior_id = banco.obterIdMaximo("creative")

    resultado = requests.get(f'{config.url_api}?sensor=creative&id_inferior={maior_id}')
    dados_novos = resultado.json()

	# Inserir os dados novos no banco
    if dados_novos and len(dados_novos) > 0:
        banco.inserirDados(dados_novos)

    dataInicial = request.args["dataInicial"]
    dataFinal = request.args["dataFinal"]
    dados = banco.listarDados(dataInicial, dataFinal)

    return json.jsonify(dados)

@app.get('/obterTemperaturaAgrupada')
def obterTemperaturaAgrupada():
	dataInicial = request.args.get("dataInicial")
	dataFinal = request.args.get("dataFinal")

	if not dataInicial or not dataFinal:
		return json.jsonify(({"erro": "Parâmetros inválidos"}), 400)

	dados = banco.listarTemperaturaAgrupada(dataInicial, dataFinal)
	return json.jsonify(dados)

@app.get('/obterUmidadeAgrupada')
def obterUmidadeAgrupada():
    dataInicial = request.args.get("dataInicial")
    dataFinal = request.args.get("dataFinal")
    
    if not dataInicial or not dataFinal:
        return json.jsonify(({"erro": "Parâmetros inválidos"}), 400)

    dados = banco.listarUmidadeAgrupada(dataInicial, dataFinal)  
    return json.jsonify(dados)


@app.get('/obterLuminosidadeAgrupada')
def obterLuminosidadeAgrupada():
    dataInicial = request.args.get("dataInicial")
    dataFinal = request.args.get("dataFinal")
    
    if not dataInicial or not dataFinal:
        return json.jsonify(({"erro": "Parâmetros inválidos"}), 400)

    dados = banco.listarLuminosidadeAgrupada(dataInicial, dataFinal)  
    return json.jsonify(dados)

@app.get('/statusbom')
def statusBom():
    # Broadcast the notification to all connected clients
    flask_socketio.emit('notificacao', {"status": "bom"}, namespace='/', broadcast=True)
    return json.jsonify({"status": "bom"})

@app.get('/statusruim')
def statusRuim():
    # Broadcast the notification to all connected clients
    flask_socketio.emit('notificacao', {"status": "ruim"}, namespace='/', broadcast=True)
    return json.jsonify({"status": "ruim"})

# Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

if __name__ == '__main__':
    socketio.run(app, host=config.host, port=config.port, debug=True)
