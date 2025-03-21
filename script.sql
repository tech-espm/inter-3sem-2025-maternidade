CREATE DATABASE IF NOT EXISTS maternidade DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;

-- Todos os deltas estão em segundos

USE maternidade;

-- Só existe id_sensor 1
-- topic espm/stainel/mtp/Brightness1
-- {"Brightness1": 51,"clientId":"mtp"}
-- topic espm/stainel/mtp/Humidity
-- {"Humidity": 65.10,"clientId":"mtp"}
-- topic espm/stainel/mtp/Temperature
-- {"Temperature": 22.41,"clientId":"mtp"}
-- topic espm/stainel/mtp/VOC
-- {"VOC": 102,"clientId":"mtp"}
-- topic espm/stainel/mtp/CO2
-- {"CO2": 465,"clientId":"mtp"}
-- topic espm/stainel/mtp/AirPressure
-- {"AirPressure": 934.50,"clientId":"mtp"}
-- topic espm/stainel/mtp/Noise
-- {"Noise": 44,"clientId":"mtp"}
-- topic espm/stainel/mtp/AerosolStaleAirStatus
-- {"AerosolStaleAirStatus": 1,"clientId":"mtp"}
-- topic espm/stainel/mtp/AerosolRiskOfInfectionStatus
-- {"AerosolRiskOfInfectionStatus": 1,"clientId":"mtp"}
-- topic espm/stainel/mtp/DewPoint
-- {"DewPoint": 15.39,"clientId":"mtp"}
CREATE TABLE creative (
  id bigint NOT NULL AUTO_INCREMENT,
  data datetime NOT NULL,
  id_sensor tinyint NOT NULL,
  delta int NOT NULL,
  luminosidade float NOT NULL,
  umidade float NOT NULL,
  temperatura float NOT NULL,
  voc float NOT NULL,
  co2 float NOT NULL,
  pressao_ar float NOT NULL,
  ruido float NOT NULL,
  aerosol_parado tinyint NOT NULL,
  aerosol_risco tinyint NOT NULL,
  ponto_orvalho float NOT NULL,
  PRIMARY KEY (id),
  KEY creative_data_id_sensor (data, id_sensor),
  KEY creative_id_sensor (id_sensor)
);

-- Query de consolidação de leituras do espaço por dia do mês e por hora, para o heatmap com N colunas e 24 linhas
select date_format(date(data), '%d/%m/%Y') dia, extract(hour from data) hora, max(ruido) ruido, avg(luminosidade) luminosidade, avg(umidade) umidade, avg(temperatura) temperatura
from creative
where data between '2025-03-03 00:00:00' and '2025-03-14 23:59:59'
group by dia, hora;
