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

# A função text(), utilizada ao longo desse código, serve para encapsular um comando
# SQL qualquer, de modo que o SQLAlchemy possa entender!

def listarPessoas():
	# O with do Python é similar ao using do C#, ou o try with resources do Java.
	# Ele serve para limitar o escopo/vida do objeto automaticamente, garantindo
	# que recursos, como uma conexão com o banco, não sejam desperdiçados!
	with Session(engine) as sessao:
		pessoas = sessao.execute(text("SELECT id, nome, email FROM pessoa ORDER BY nome"))

		# Como cada registro retornado é uma tupla ordenada, é possível
		# utilizar a forma de enumeração de tuplas:
		for (id, nome, email) in pessoas:
			print(f'\nid: {id} / nome: {nome} / email: {email}')

		# Ou, se preferir, é possível retornar cada tupla, o que fica mais parecido
		# com outras linguagens de programação:
		#for pessoa in pessoas:
		#	print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

def obterPessoa(id):
	with Session(engine) as sessao:
		parametros = {
			'id': id
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		pessoa = sessao.execute(text("SELECT id, nome, email FROM pessoa WHERE id = :id"), parametros).first()

		if pessoa == None:
			print('Pessoa não encontrada!')
		else:
			print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

def criarPessoa(nome, email):
	# É importante utilizar o método begin() para que a sessão seja comitada
	# automaticamente ao final, caso não ocorra uma exceção!
	# Isso não foi necessário nos outros exemplos porque nenhum dado estava sendo
	# alterado lá! Caso alguma exceção ocorra, rollback() será executado automaticamente,
	# e nenhuma alteração será persistida. Para mais informações de como explicitar
	# esse processo de commit() e rollback():
	# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#framing-out-a-begin-commit-rollback-block
	with Session(engine) as sessao, sessao.begin():
		pessoa = {
			'nome': nome,
			'email': email
		}

		sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), pessoa)

		# Para inserir, ou atualizar, vários registros ao mesmo tempo, a forma mais rápida
		# é passar uma lista como segundo parâmetro:
		# lista = [ ... ]
		# sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), lista)

# Para mais informações:
# https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html

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
		registros = sessao.execute(text("select date_format(date(data), '%d/%m/%Y') dia, extract(hour from data) hora, max(ruido) ruido, avg(luminosidade) luminosidade, avg(umidade) umidade, avg(temperatura) temperatura from creative where data between :dataInicial and :dataFinal group by dia, hora"), parametros)
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
