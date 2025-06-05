-- View de variação da taxa de resolução em 5 dias úteis por grupo econômico

CREATE OR REPLACE VIEW vw_variacao_taxa_resolucao AS
WITH medias_mensais AS (
    SELECT
        t.data_referencia,
        g.nome AS grupo,
        AVG(f.taxa_resolucao) AS taxa_resolucao_media
    FROM fato_ida f
    JOIN dim_tempo t ON t.id = f.tempo_id
    JOIN dim_grupo g ON g.id = f.grupo_id
    GROUP BY t.data_referencia, g.nome
),

COMMENT ON VIEW vw_variacao_taxa_resolucao IS
    'View que mostra a taxa de variação média mensal da taxa de resolvidas em 5 dias úteis e
    as diferenças dessas taxas para cada grupo econômico (pivotados em colunas).';

com_variacao AS (
    SELECT
        m.*,
        LAG(m.taxa_resolucao_media) OVER (PARTITION BY m.grupo ORDER BY m.data_referencia) AS taxa_anterior
    FROM medias_mensais m
),
variacao_por_grupo AS (
    SELECT
        data_referencia,
        grupo,
        ((taxa_resolucao_media - taxa_anterior) / taxa_anterior) * 100 AS variacao
    FROM com_variacao
    WHERE taxa_anterior IS NOT NULL
),
media_geral AS (
    SELECT
        data_referencia,
        AVG(variacao) AS variacao_media
    FROM variacao_por_grupo
    GROUP BY data_referencia
),
tabela_final AS (
    SELECT
        v.data_referencia,
        m.variacao_media,
        MAX(CASE WHEN v.grupo = 'ALGAR' THEN ROUND(v.variacao - m.variacao_media, 2) END) AS ALGAR,
        MAX(CASE WHEN v.grupo = 'CLARO' THEN ROUND(v.variacao - m.variacao_media, 2) END) AS CLARO,
        MAX(CASE WHEN v.grupo = 'OI' THEN ROUND(v.variacao - m.variacao_media, 2) END) AS OI,
        MAX(CASE WHEN v.grupo = 'TIM' THEN ROUND(v.variacao - m.variacao_media, 2) END) AS TIM,
        MAX(CASE WHEN v.grupo = 'VIVO' THEN ROUND(v.variacao - m.variacao_media, 2) END) AS VIVO
    FROM variacao_por_grupo v
    JOIN media_geral m ON v.data_referencia = m.data_referencia
    GROUP BY v.data_referencia, m.variacao_media
)
SELECT * FROM tabela_final
ORDER BY data_referencia;
