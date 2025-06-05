import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

class CarregarRelatorios:
    """
    Classe para carregar os csvs normalizados no postgres
    """
    
    def __init__(self, csv_path: str):
        load_dotenv()  

        self.db_host = os.getenv("DB_HOST")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_pass = os.getenv("DB_PASS")
        self.csv_path = csv_path

        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_pass
        )
        self.cur = self.conn.cursor()

    def load_csv(self):
        df = pd.read_csv(self.csv_path, sep=";")
        return df

    def insert_data(self, df: pd.DataFrame):
        insert_query = """
        INSERT INTO fato_ida (ano, mes, grupo, uf, servico, taxa_resolvidas_5_dias)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        for row in df.itertuples(index=False):
            self.cur.execute(insert_query, row)
        self.conn.commit()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def run(self):
        self.connect()
        self.create_table()
        df = self.load_csv()
        self.insert_data(df)
        self.close()
        print("Dados inseridos com sucesso!")

