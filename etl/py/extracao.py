import requests
import os


class BaixarRelatorios:

    def __init__(self, url_base: str, path_arquivos: str, extensao: str = '.ods'):
        """
        Inicia a classe BaixarRelatorios, com a URL base, caminho local e extensão
        """
        
        self.url_base = url_base
        self.path_arquivos = path_arquivos
        self.extensao = extensao
        self.relatorios = []

    def set_relatorios(self, relatorios: list):
        """
        Define os relatórios a serem baixados
        """

        self.relatorios = relatorios

    def baixar_relatorios(self):
        """
        Baixar relatórios especificados
        """
        # requests para baixar os arquivos
        for relatorio in self.relatorios:
            
            print("Iniciando o script...")
            url = f"{self.url_base}{relatorio}{self.extensao}"
            arquivo = f"{relatorio}{self.extensao}"
            path = os.path.join(self.path_arquivos, arquivo)

            print(f"Acessando a URL {url}")    
            response = requests.get(url)

            if response.status_code == 200:
                with open(path, 'wb') as f:
                    print(f"Acessando o arquivo {arquivo}...")
                    f.write(response.content)
                print("Arquivo salvo com sucesso...")
            else:
                print(f"Falha ao acessar o arquivo {arquivo}")

