import pandas as pd
import os
import re

def TransformarRelatorios(path_bronze, path_silver):
    for nome_arquivo in os.listdir(path_bronze):
        if nome_arquivo.endswith(".ods"):
            caminho_completo = os.path.join(path_bronze, nome_arquivo)
            print(f"Lendo: {caminho_completo}")
            
            # Extrair o serviço do nome do arquivo
            servico = nome_arquivo[:3].upper()
            
            # Extrair o ano do nome do arquivo
            ano_match = re.search(r"\d{4}", nome_arquivo)
            if not ano_match:
                print(f"Ano não encontrado em {nome_arquivo}. Pulando.")
                continue
            ano = int(ano_match.group())

            # Ler o arquivo .ods
            df = pd.read_excel(caminho_completo, engine="odf", skiprows=8)

            # Renomear colunas 
            df.rename(columns={df.columns[0]: "UF", df.columns[1]: "Grupo Econômico"}, inplace=True)

            # Processar colunas 
            dados_transformados = []

            for col in df.columns[2:]:
                # Extrair mês da coluna (ex: '2019 - 1')
                match = re.search(r'(\d{4})\s*-\s*(\d+)', col)
                if match:
                    mes = int(match.group(2))
                    for _, linha in df.iterrows():
                        taxa = linha[col]
                        if pd.notnull(taxa):
                            dados_transformados.append({
                                "ano": ano,
                                "mes": mes,
                                "grupo": linha["Grupo Econômico"].strip(),
                                "uf": linha["UF"].strip(),
                                "servico": servico,
                                "taxa_resolvidas_5_dias": round(float(taxa), 2)
                            })

            # Criar DataFrame final
            df_final = pd.DataFrame(dados_transformados)

            # Salvar em CSV 
            novo_nome = nome_arquivo.replace(".ods", ".csv")
            caminho_saida = os.path.join(path_silver, novo_nome)
            df_final.to_csv(caminho_saida, index=False, sep=";", encoding="utf-8-sig")

            print(f"Transformado e salvo....")
