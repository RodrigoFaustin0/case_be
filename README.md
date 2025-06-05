# Desafio Técnico  <br> Engenheiro de Dados Júnior <br> beAnalytic

Desafio proposto pela beAnalytic para a vaga de Engenheiro de Dados Júnior. Construção de um **Data Mart** para os **Índices de Desempenho no Atendimento (IDA)** dos serviços de telecomunicações no Brasil (SMP, STFC e SCM), extraídos do portal de Dados Abertos da Anatel.


## Tecnologias Utilizadas

- PostgreSQL 17.5 (`postgres:17.5-bookworm`)
- Python 3.11 (`python:3.11.12-bookworm`)
- Docker & Docker Compose
- SQL (modelagem dimensional em estrela)
- OOP em Python para ETL
- Comentários de documentação (`COMMENT ON`, `pydoc`)


## Estrutura do Projeto
- README, com detalhes do projeto
- **docker-compose** que iniciará toda a pipeline
- /db - que contém o init.slq (que criará o Data Mart)
- /etl - que contém os arquivos brutos e códigos python


## Pré-requisitos

- `Docker` e `Docker Compose` instalado


## Execução

1. Clonar o repositório <br>`git clone https://github.com/RodrigoFaustin0/case_be.git`  
2. Entrar na pasta do projeto <br> `cd projeto-beanalytic`
3. Subir todo o projeto com um unico comando Docker <br> `docker-compose up --build`


