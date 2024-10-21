import pandas as pd
import psycopg2
from urllib.parse import urlparse

# Funzione per esportare i dati dal database in un file Excel
def export_data_to_excel(database_url, excel_file_path):
    # Analizza l'URL per ottenere le componenti della connessione
    url = urlparse(database_url)
    conn = psycopg2.connect(
        database=url.path[1:],  # Rimuovi il '/' all'inizio
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    # Query per selezionare i dati che vuoi esportare
    query = "SELECT * FROM users;"

    # Leggi i dati nel DataFrame
    df = pd.read_sql_query(query, conn)

    # Esporta il DataFrame in un file Excel
    df.to_excel(excel_file_path, index=False)
    print(f"Dati esportati in {excel_file_path}.")

    # Chiudi la connessione
    conn.close()

# Esempio di utilizzo
if __name__ == "__main__":
    # Percorso per il file Excel
    excel_file_path = 'dati_soci.xlsx'
    # L'URL del tuo database
    DATABASE_URL = 'postgresql://db_derryrock_user:F3RW728z9Tbhhckj5RwUf2yO3RWCUUnF@dpg-csamt28gph6c73a4ftvg-a.oregon-postgres.render.com/db_derryrock'

    # Richiama la funzione per esportare i dati
    export_data_to_excel(DATABASE_URL, excel_file_path)
