import pandas as pd
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from mail import send_email
import psycopg2
from sqlalchemy import create_engine, text
from urllib.parse import urlparse
import psycopg2

#----------------------------------------------------------------------------------------------------#
## Percorso del file Excel
file_path = 'dati_soci.xlsx'
##richiamo export DB per lavorare sull'excel:
#from export_DB import export_data_to_excel 
#DATABASE_URL = 'postgresql://db_derryrock_user:F3RW728z9Tbhhckj5RwUf2yO3RWCUUnF@dpg-csamt28gph6c73a4ftvg-a.oregon-postgres.render.com/db_derryrock'
### Richiamo la funzione per esportare i dati
#export_data_to_excel(DATABASE_URL, file_path)

#----------------------------------------------------------------------------------------------------#
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
#----------------------------------------------------------------------------------------------------#
# Percorso del file Excel
file_path = 'dati_soci.xlsx'
#richiamo export DB per lavorare sull'excel:
#from export_DB import export_data_to_excel 
#DATABASE_URL = 'postgresql://db_derryrock_user:F3RW728z9Tbhhckj5RwUf2yO3RWCUUnF@dpg-csamt28gph6c73a4ftvg-a.oregon-postgres.render.com/db_derryrock'
## Richiama la funzione per esportare i dati
#export_data_to_excel(DATABASE_URL, file_path)

# Percorso per salvare i PDF
pdf_output_folder = 'tessere'
os.makedirs(pdf_output_folder, exist_ok=True)

# Controlla se il file esiste
if os.path.exists(file_path):
    # Leggi il file Excel
    df = pd.read_excel(file_path)

    # Aggiungi la colonna "Inviato" all'inizio se non esiste
    if 'inviato' not in df.columns:
        df.insert(0, 'inviato', '')  # Inserisci la colonna "Inviato" con valori vuoti

    # Trova il valore massimo nella colonna "Numero Tessera"
    if not df['numero_tessera'].isnull().all():  # Assicurati che non siano tutte nulle
        numero_tessera = df['numero_tessera'].max()
    else:
        numero_tessera = 1200  # Se tutte le celle sono vuote, partiamo da 0

    # Aggiorna la colonna "Numero Tessera" per gli approvati
    for index, row in df.iterrows():
        if row['approvato'] == 'SI' and pd.isnull(row['numero_tessera']):
            numero_tessera += 1  # Incrementa il numero tessera
            df.at[index, 'numero_tessera'] = numero_tessera

    # Salva il DataFrame aggiornato nel file Excel
    df.to_excel(file_path, index=False)
    print("File Excel aggiornato con i numeri tessera.")

    # Filtra solo i soci approvati che non sono stati inviati (colonna "Inviato" vuota)
    soci_approvati = df[(df['approvato'] == 'SI') & (df['inviato'].isnull())]

    # Genera un PDF per ogni socio approvato non inviato
    for index, row in soci_approvati.iterrows():
        pdf_filename = os.path.join(pdf_output_folder, f'tessera_{int(row["numero_tessera"])}.pdf')
        
        # Crea un canvas per il PDF
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        # Imposta uno sfondo colorato
        c.setFillColor(colors.lightgrey)
        c.rect(0, 0, 612, 792, fill=1)  # Riempie lo sfondo

        # Imposta il font per il titolo
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.black)  # Colore del testo
        c.drawString(100, 750, "Tessera Associativa - Derry Rock Pub")

        # Aggiungi più spazio dopo il titolo
        y_position = 720  # Nuova posizione per il testo

        # Passa a un font normale per i dettagli
        c.setFont("Helvetica", 14)

        # Scrivi i dati nel PDF
        c.drawString(100, y_position, f"Nome: {row['nome']}")
        y_position -= 30  # Sposta in basso
        c.drawString(100, y_position, f"Cognome: {row['cognome']}")
        y_position -= 30
        c.drawString(100, y_position, f"Email: {row['email']}")
        y_position -= 30
        c.drawString(100, y_position, f"Numero Tessera: {row['numero_tessera']}")

        # Aggiungi un bordo decorativo
        c.setStrokeColor(colors.black)
        c.rect(50, 50, 500, 700, stroke=1, fill=0)

        # Aggiungi una linea di separazione
        c.setStrokeColor(colors.grey)
        c.line(50, y_position - 10, 550, y_position - 10)

        # Inserisci un'immagine più vicina alla linea
        image_path = '/Users/giuseppecangemi/Desktop/Programming/Python/DerryRockAutomation/uploads/derryrockfoto.jpg'  # Specifica il percorso della tua immagine
        image_y_position = 300  # Posiziona l'immagine 20 unità sotto la linea
        c.drawImage(image_path, 50, image_y_position, width=500, height=300)  # Regola le dimensioni dell'immagine

        # Salva il PDF
        c.save()

        send_email(row['email'], pdf_filename) 

        # Aggiorna la colonna "Inviato" a "SI"
        df.at[index, 'inviato'] = 'SI'


    # Salva il DataFrame aggiornato nel file Excel
    df.to_excel(file_path, index=False)
    #e nel DB
    database_url = "postgresql://db_derryrock_user:F3RW728z9Tbhhckj5RwUf2yO3RWCUUnF@dpg-csamt28gph6c73a4ftvg-a.oregon-postgres.render.com/db_derryrock"
    table_name='users'
    engine = create_engine(database_url)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Tessere generate e salvate nella cartella '{pdf_output_folder}'.")
    print(f"Aggiornato DB '{table_name}'.")
else:
    print("Il file Excel non esiste o problema su DB")
   
    



