-- 1. Demanda total por mês
SELECT
    substr(DataMovimento, 1, 7) AS mes,
    SUM(Demanda) AS demanda_total
FROM demanda
GROUP BY mes
ORDER BY mes;


-- 2. As 10 linhas de ônibus com maior demanda
SELECT
    CodLinha,
    NomeLinha,
    SUM(Demanda) AS demanda_total
FROM demanda
GROUP BY CodLinha, NomeLinha
ORDER BY demanda_total DESC
LIMIT 10;


-- 3. Demanda por tipo de passageiro
SELECT
    TipoPassageiro,
    SUM(Demanda) AS demanda_total
FROM demanda
GROUP BY TipoPassageiro
ORDER BY demanda_total DESC;


-- 4. Demanda média diária por linha de ônibus
SELECT
    CodLinha,
    NomeLinha,
    ROUND(AVG(Demanda), 2) AS demanda_media
FROM demanda
GROUP BY CodLinha, NomeLinha
ORDER BY demanda_media DESC
LIMIT 10;


-- 5. Demanda por dia da semana
SELECT
    CASE strftime('%w', DataMovimento)
        WHEN '0' THEN 'Domingo'
        WHEN '1' THEN 'Segunda-feira'
        WHEN '2' THEN 'Terça-feira'
        WHEN '3' THEN 'Quarta-feira'
        WHEN '4' THEN 'Quinta-feira'
        WHEN '5' THEN 'Sexta-feira'
        WHEN '6' THEN 'Sábado'
    END AS dia_semana,
    SUM(Demanda) AS demanda_total
FROM demanda
GROUP BY strftime('%w', DataMovimento)
ORDER BY strftime('%w', DataMovimento);
