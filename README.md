# Projeto Interdisciplinar III - Sistemas de Informação ESPM

<p align="center">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>

# BabySense

### 2025-01

## Integrantes
- [Maria Luiza Oliveira de Souza](https://github.com/MariaLuizazz)
- [Marcela de Martini](https://github.com/marcelademartini)
- [Ana Carolina Frank](https://github.com/bligui)
- [Rafael Lucena](https://github.com/rafaarklu)


## Descrição do Projeto

O ambiente hospitalar deve proporcionar condições adequadas para a recuperação e bem-estar dos pacientes, especialmente em unidades sensíveis, como as salas de maternidade. Um dos principais desafios nesse contexto é garantir que os recém-nascidos recebam atendimento imediato quando necessitam, especialmente quando choram. O choro do bebê é um dos principais sinais de necessidade, podendo indicar fome, desconforto ou problemas de saúde (SILVA, 2025). Assim, a adoção de tecnologias que auxiliem na detecção automática do choro pode otimizar o atendimento e melhorar a qualidade do cuidado neonatal (SOUZA; ALMEIDA, 2025).
Neste contexto, o presente projeto propõe a utilização do sensor MULTISENSOR TP V2 IP UP WS para a detecção e monitoramento do choro dos bebês em salas de maternidade. O sistema identificará sons característicos do choro e acionará alertas automáticos para a equipe de enfermagem, permitindo uma resposta rápida e eficaz. O sensor será posicionado estrategicamente no ambiente hospitalar, captando sons de maneira contínua. Caso o choro seja detectado, um alerta será gerado e enviado ao Sistema de Informação em Saúde (SIS) para notificação da equipe responsável, garantindo que os profissionais possam atender prontamente o bebê (COSTA et al., 2025).
A implementação desse sistema contribuirá para a melhoria do atendimento neonatal, assegurando que os bebês recebam atenção imediata sempre que necessário. Além disso, futuras expansões do projeto poderão permitir a análise de padrões sonoros ao longo do tempo, auxiliando na identificação de comportamentos e necessidades dos recém-nascidos. O sensor também poderá ser integrado a câmeras para verificar a origem do choro e a outros sistemas hospitalares para otimizar a gestão do atendimento (FERREIRA; SANTOS, 2025). A automação proporcionada pelo sistema melhorará a eficiência da equipe médica, reduzindo a necessidade de monitoramento manual e otimizando o tempo dos profissionais (PEREIRA, 2025).


## Configuração do Projeto

Para executar, deve criar o arquivo `config.py` da seguinte forma:

```python
host = '0.0.0.0'
port = 3000
conexao_banco = 'mysql+mysqlconnector://usuario:senha@host/banco'
url_api = 'https://site.com'
```

Todos os comandos abaixo assumem que o terminal esteja com o diretório atual na raiz do projeto.

## Criação e Ativação do venv

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Execução

```
.venv\Scripts\activate
python app.py
```

## Mais Informações

https://flask.palletsprojects.com/en/3.0.x/quickstart/
https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/

# Licença

Este projeto é licenciado sob a [MIT License](https://github.com/tech-espm/inter-3sem-2025-maternidade/blob/main/LICENSE).

<p align="right">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo-si-512.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>
