-- Apagar as tabelas caso já existam
DROP TABLE IF EXISTS fato_ida CASCADE;
DROP TABLE IF EXISTS dim_tempo CASCADE;
DROP TABLE IF EXISTS dim_grupo_economico CASCADE;
DROP TABLE IF EXISTS dim_servico CASCADE;
DROP TABLE IF EXISTS dim_uf CASCADE;

-- Tabela dimensão: Tempo
CREATE TABLE dim_tempo (
    id SERIAL PRIMARY KEY,
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    data DATE NOT NULL UNIQUE
);
COMMENT ON TABLE dim_tempo IS 'Dimensão de tempo: mês, ano e data de referência';
COMMENT ON COLUMN dim_tempo.data IS 'Data referente ao primeiro dia do mês (YYYY-MM-01)';

-- Tabela dimensão: Empresa
CREATE TABLE dim_grupo_economico (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);
COMMENT ON TABLE dim_grupo_economico IS 'Dimensão com o nome dos grupos de empresas (ex: CLARO, ALGAR)';

-- Tabela dimensão: Serviço
CREATE TABLE dim_servico (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);
COMMENT ON TABLE dim_servico IS 'Tipo de serviço: SMP (celular), STFC (fixo), SCM (banda larga)';

-- Tabela dimensão: UF
CREATE TABLE dim_uf (
    id SERIAL PRIMARY KEY,
    sigla CHAR(2) NOT NULL UNIQUE,
    nome TEXT
);
COMMENT ON TABLE dim_uf IS 'Unidades Federativas do Brasil';

-- Tabela fato: Índice de Desempenho no Atendimento
CREATE TABLE fato_ida (
    id SERIAL PRIMARY KEY,
    tempo_id INTEGER NOT NULL REFERENCES dim_tempo(id),
    grupo_id INTEGER NOT NULL REFERENCES dim_grupo_economico(id),
    servico_id INTEGER NOT NULL REFERENCES dim_servico(id),
    uf_id INTEGER NOT NULL REFERENCES dim_uf(id),
    taxa_resolvidas_5_dias NUMERIC(5,2) NOT NULL
);
COMMENT ON TABLE fato_ida IS 'Tabela fato com a taxa de reclamações resolvidas em até 5 dias úteis';

-- Índices para otimização
CREATE INDEX idx_fato_ida_tempo ON fato_ida(tempo_id);
CREATE INDEX idx_fato_ida_servico ON fato_ida(servico_id);
CREATE INDEX idx_fato_ida_uf ON fato_ida(uf_id);
CREATE INDEX idx_fato_ida_grupo ON fato_ida(grupo_id);
