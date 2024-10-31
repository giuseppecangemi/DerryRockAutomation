import pandas as pd
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from mail import send_email
from sqlalchemy import create_engine, text

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
numero_tessera = filtered_df['numero_tessera'].max() if not filtered_df['numero_tessera'].isnull().all() else 1200

# Cerco il valore max del numero tessera così da andare in sequenza
#numero_tessera = df['numero_tessera'].max() if not df['numero_tessera'].isnull().all() else 1200

# LOGICA 1
for index, row in df.iterrows():
    if row['approvato'] == 'SI' and pd.isnull(row['numero_tessera']):
        numero_tessera += 1  # Incrementa il numero tessera
        df.at[index, 'numero_tessera'] = numero_tessera
    elif row['approvato'] == 'SI' and row['manuale'] == 'Sì':
        numero_tessera = row['numero_tessera']
        df.at[index, 'numero_tessera'] = numero_tessera

# Filtra soci approvati (quelli non inviati)
soci_approvati = df[(df['approvato'] == 'SI') & (df['inviato'] != 'SI')]

# Creo un PDF per ogni socio approvato non inviato
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
output_excel_file = 'dati_soci.xlsx'
df.to_excel(output_excel_file, index=False)
print(f"Dati esportati in {output_excel_file}.")
print(f"Tessere generate e salvate nella cartella '{pdf_output_folder}'.")