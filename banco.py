# Vamos utilizar o pacote SQLAlchemy para acesso a banco de dados:
# https://docs.sqlalchemy.org
#
# Para isso, ele precisa ser instalado via pip (de preferência com o VS Code fechado):
# python -m pip install SQLAlchemy
#
# Além disso, o SQLAlchemy precisa de um driver do conexão ao banco. Isso depende do servidor
# (MySQL, Postgres, SQL Server, Oracle...) e do driver real. Vamos utilizar o driver MySQL-Connector,
# que também precisa ser instalado (de preferência com o VS Code fechado):
# python -m pip install mysql-connector-python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from config import conexao_banco

# Como criar uma comunicação com o banco de dados:
# https://docs.sqlalchemy.org/en/14/core/engines.html
#
# Detalhes específicos ao MySQL
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqlconnector
#
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine(conexao_banco)




def obterIdMaximo(tabela):
	with Session(engine) as sessao:
		registro = sessao.execute(text(f"SELECT MAX(id) id FROM {tabela}")).first()

		if registro == None or registro.id == None:
			return 0
		else:
			return registro.id

def inserirDados(registros):
	with Session(engine) as sessao, sessao.begin():
		for registro in registros:
			sessao.execute(text("INSERT INTO creative (id, data, id_sensor, delta, luminosidade, umidade, temperatura, voc, co2, pressao_ar, ruido, aerosol_parado, aerosol_risco, ponto_orvalho) VALUES (:id, :data, :id_sensor, :delta, :luminosidade, :umidade, :temperatura, :voc, :co2, :pressao_ar, :ruido, :aerosol_parado, :aerosol_risco, :ponto_orvalho)"), registro)

def listarDados(dataInicial, dataFinal):
	parametros = {
		"dataInicial": dataInicial + " 00:00:00",
		"dataFinal": dataFinal + " 23:59:59"
	}

	with Session(engine) as sessao:
		registros = sessao.execute(text("select date_format(date(data), '%d/%m') dia, extract(hour from data) hora, max(ruido) ruido, avg(luminosidade) luminosidade, avg(umidade) umidade, avg(temperatura) temperatura from creative where data between :dataInicial and :dataFinal group by dia, hora"), parametros)
		dados = []
		for registro in registros:
			dados.append({
				"dia": registro.dia,
				"hora": registro.hora,
				"ruido": registro.ruido,
				"luminosidade": registro.luminosidade,
				"umidade": registro.umidade,
				"temperatura": registro.temperatura,
			})
		return dados


def listarTemperaturaAgrupada(dataInicial, dataFinal):
	parametros = {
		"dataInicial": dataInicial + " 00:00:00",
		"dataFinal": dataFinal + " 23:59:59"
	}

	with Session(engine) as sessao:
		registros = sessao.execute(text("""
			SELECT 
				DATE_FORMAT(data, '%W') AS dia,
				EXTRACT(HOUR FROM data) AS hora,
				ROUND(AVG(temperatura), 2) AS temperatura
			FROM creative
			WHERE data BETWEEN :dataInicial AND :dataFinal
			GROUP BY dia, hora
			ORDER BY 
				FIELD(dia, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'), 
				hora
		"""), parametros)

		dados = []
		for registro in registros:
			dados.append({
				"dia": registro.dia,
				"hora": registro.hora,
				"temperatura": registro.temperatura,
			})

		return dados


def listarUmidadeAgrupada(dataInicial, dataFinal):
	parametros = {
		"dataInicial": dataInicial + " 00:00:00",
		"dataFinal": dataFinal + " 23:59:59"
	}

	with Session(engine) as sessao:
		registros = sessao.execute(text("""
			SELECT 
				DATE_FORMAT(data, '%W') AS dia,
				EXTRACT(HOUR FROM data) AS hora,
				ROUND(AVG(umidade), 2) AS umidade
			FROM creative
			WHERE data BETWEEN :dataInicial AND :dataFinal
			GROUP BY dia, hora
			ORDER BY 
				FIELD(dia, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'), 
				hora
		"""), parametros)

		dados = []
		for registro in registros:
			dados.append({
				"dia": registro.dia,
				"hora": registro.hora,
				"umidade": registro.umidade,
			})

		return dados
	

def listarLuminosidadeAgrupada(dataInicial, dataFinal):
	parametros = {
		"dataInicial": dataInicial + " 00:00:00",
		"dataFinal": dataFinal + " 23:59:59"
	}

	with Session(engine) as sessao:
		registros = sessao.execute(text("""
			SELECT 
				DATE_FORMAT(data, '%W') AS dia,
				EXTRACT(HOUR FROM data) AS hora,
				ROUND(AVG(luminosidade), 2) AS luminosidade
			FROM creative
			WHERE data BETWEEN :dataInicial AND :dataFinal
			GROUP BY dia, hora
			ORDER BY 
				FIELD(dia, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'), 
				hora
		"""), parametros)

		dados = []
		for registro in registros:
			dados.append({
				"dia": registro.dia,
				"hora": registro.hora,
				"luminosidade": registro.luminosidade,
			})

		return dados
