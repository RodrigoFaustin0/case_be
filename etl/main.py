import os
from py.extracao import BaixarRelatorios
from py.transformacao import TransformarRelatorios
from py.carregamento import CarregarRelatorios
from dotenv import load_dotenv

def main():

    ######################################
    # Variáveis
    ######################################

    # Env
    load_dotenv()

    # path dos arquivos
    path_bronze = os.path.join("data", "bronze")
    os.makedirs(path_bronze, exist_ok=True)
    path_silver = os.path.join("data", "silver")
    os.makedirs(path_silver, exist_ok=True)
    path_gold = os.path.join("data", "gold")
    os.makedirs(path_gold, exist_ok=True)
    
    # url dados abertos
    url_base = 'https://anatel.gov.br/dadosabertos/PDA/IDA/'
    relatorios = ['SCM2019','SMP2019','STFC2019']

    ######################################


    print("######################")
    print("BAIXANDO OS RELATÓRIOS")
    print("######################\n")
    extract = BaixarRelatorios(url_base, path_bronze)
    extract.set_relatorios(relatorios)
    extract.baixar_relatorios()

    print("\n######################")
    print("TRANSFORMANDO OS DADOS")
    print("######################\n")
    transform = TransformarRelatorios(path_bronze, path_silver)


    print("\n######################")
    print("CARREGANDO OS DADOS")
    print("######################\n")
    load = CarregarRelatorios(path_silver)
    load.run()

if __name__=="__main__":
    main()