import pandas as pd
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from mail import send_email
from sqlalchemy import create_engine, text
from pdf import crea_pdf 

# URL del database
DATABASE_URL = 'postgresql://db_derryrock_user:F3RW728z9Tbhhckj5RwUf2yO3RWCUUnF@dpg-csamt28gph6c73a4ftvg-a.oregon-postgres.render.com/db_derryrock'

# Connessione al database
engine = create_engine(DATABASE_URL)

# Percorso per salvare i PDF
pdf_output_folder = 'tessere'
os.makedirs(pdf_output_folder, exist_ok=True)

# Creo il df come su Excel ma tramite SQL query
with engine.connect() as connection:
    query = "SELECT * FROM users;"
    df = pd.read_sql_query(query, connection)

# Se non esiste la colonna la inseriamo
if 'inviato' not in df.columns:
    df.insert(0, 'inviato', '')

# Converte la colonna 'numero_tessera' in numerico, impostando i valori non validi a NaN
df['numero_tessera'] = pd.to_numeric(df['numero_tessera'], errors='coerce')

# Filtra il DataFrame per escludere le righe dove "manuale" è "Sì"
filtered_df = df[df['manuale'] != 'Sì']

# Calcola il massimo valore di "numero_tessera" nel DataFrame filtrato
# Calcola il massimo valore di numero_tessera escludendo le righe con manuale == 'Sì'
massimo_valore = df.loc[df['manuale'] != 'Sì', 'numero_tessera'].max()
print("Massimo valore: " + str(massimo_valore))
# Inizializza numero_tessera a massimo_valore + 1 se massimo_valore non è nullo, altrimenti a 1
numero_tessera = (massimo_valore + 1) if pd.notnull(massimo_valore) else 1
print("NUMERO TESSERA: " + str(numero_tessera))


# LOGICA 1
for index, row in df.iterrows():
    if row['approvato'] == 'SI' and pd.isnull(row['numero_tessera']):
        df.at[index, 'numero_tessera'] = numero_tessera  # Assegna numero_tessera
        numero_tessera += 1  # Incrementa il numero tessera
    elif row['approvato'] == 'SI' and row['manuale'] == 'Sì':
        numero_tessera_man = row['numero_tessera']  # Assegna il numero_tessera dalla riga corrente
        df.at[index, 'numero_tessera'] = numero_tessera_man

# Filtra soci approvati (quelli non inviati)
soci_approvati = df[(df['approvato'] == 'SI') & (df['inviato'] != 'SI')]

# Creo un PDF per ogni socio approvato non inviato
for index, row in soci_approvati.iterrows():
    pdf_filename = os.path.join(pdf_output_folder, f'tessera_{int(row["numero_tessera"])}.pdf')
    nome_str = row['nome'].split()[0]
    # Crea il PDF
    crea_pdf(int(row['numero_tessera']), nome_str, row['cognome'], str(pdf_filename))  # Passa il percorso del file PDF
    #invia mail
    send_email(row['email'], pdf_filename) 
    # Aggiorna la colonna "Inviato" a "SI"
    df.at[index, 'inviato'] = 'SI'

# Aggiornamento nel database
with engine.connect() as connection:
    with connection.begin():
        for index, row in df.iterrows():
            try:
                update_query = text("""
                    UPDATE users 
                    SET numero_tessera = :numero_tessera,
                        inviato = :inviato
                    WHERE id = :id
                """)
                result = connection.execute(update_query, {
                    'numero_tessera': row['numero_tessera'],
                    'inviato': row['inviato'],
                    'id': row['id']
                })
                print(f"Aggiornate righe: {result.rowcount}")  # Stampa il numero di righe aggiornate
            except Exception as e:
                print(f"Errore durante l'aggiornamento della riga {index}: {e}")

print(f"Tessere generate e salvate nella cartella '{pdf_output_folder}'.")

# Esporta il DataFrame aggiornato in un file Excel
output_excel_file = 'DB/dati_soci.xlsx'
df.to_excel(output_excel_file, index=False)
print(f"Dati esportati in {output_excel_file}.")
print(f"Tessere generate e salvate nella cartella '{pdf_output_folder}'.")