-- ============================================================
-- VIEW 1: TEMPERATURA MÉDIA POR LOCALIZAÇÃO
-- ============================================================

CREATE OR REPLACE VIEW avg_temp_por_localizacao AS
SELECT
    location,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    COUNT(*) AS total_readings
FROM temperature_readings
GROUP BY location
ORDER BY location;


-- ============================================================
-- VIEW 2: QUANTIDADE DE LEITURAS POR HORA
-- ============================================================

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM reading_timestamp)::INTEGER AS hora,
    COUNT(*) AS total_readings
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM reading_timestamp)
ORDER BY hora;


-- ============================================================
-- VIEW 3: TEMPERATURA MÍNIMA E MÁXIMA POR DIA
-- ============================================================

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    DATE(reading_timestamp) AS data,
    MIN(temperature) AS temperatura_minima,
    MAX(temperature) AS temperatura_maxima,
    ROUND(AVG(temperature), 2) AS temperatura_media
FROM temperature_readings
GROUP BY DATE(reading_timestamp)
ORDER BY data;
