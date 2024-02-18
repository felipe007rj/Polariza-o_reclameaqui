import sqlite3
import pandas as pd

# Função para exportar dados do SQLite para CSV
def export_to_csv(database_name, csv_file):
    connection = sqlite3.connect(database_name)
    query = "SELECT * FROM reclamacoes"
    
    # Usando pandas para ler os dados do SQLite e exportar para CSV
    df = pd.read_sql_query(query, connection)
    df.to_csv(csv_file, index=False)
    
    connection.close()

# Nome do banco de dados SQLite
database_name = 'reclamacoes.db'

# Nome do arquivo CSV de saída
csv_file = 'reclamacoes_data.csv'

# Chamando a função para exportar os dados
export_to_csv(database_name, csv_file)

print(f'Dados exportados com sucesso para: {csv_file}')
