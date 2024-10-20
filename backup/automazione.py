import pandas as pd
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from mail import send_email

# Percorso del file Excel
file_path = 'dati.xlsx'

# Percorso per salvare i PDF
pdf_output_folder = 'tessere'
os.makedirs(pdf_output_folder, exist_ok=True)

# Controlla se il file esiste
if os.path.exists(file_path):
    # Leggi il file Excel
    df = pd.read_excel(file_path)

    # Aggiungi la colonna "Inviato" all'inizio se non esiste
    if 'Inviato' not in df.columns:
        df.insert(0, 'Inviato', '')  # Inserisci la colonna "Inviato" con valori vuoti

    # Trova il valore massimo nella colonna "Numero Tessera"
    if not df['Numero Tessera'].isnull().all():  # Assicurati che non siano tutte nulle
        numero_tessera = df['Numero Tessera'].max()
    else:
        numero_tessera = 0  # Se tutte le celle sono vuote, partiamo da 0

    # Aggiorna la colonna "Numero Tessera" per gli approvati
    for index, row in df.iterrows():
        if row['Approvato'] == 'SI' and pd.isnull(row['Numero Tessera']):
            numero_tessera += 1  # Incrementa il numero tessera
            df.at[index, 'Numero Tessera'] = numero_tessera

    # Salva il DataFrame aggiornato nel file Excel
    df.to_excel(file_path, index=False)
    print("File Excel aggiornato con i numeri tessera.")

    # Filtra solo i soci approvati che non sono stati inviati (colonna "Inviato" vuota)
    soci_approvati = df[(df['Approvato'] == 'SI') & (df['Inviato'].isnull())]

    # Genera un PDF per ogni socio approvato non inviato
    for index, row in soci_approvati.iterrows():
        pdf_filename = os.path.join(pdf_output_folder, f'tessera_{int(row["Numero Tessera"])}.pdf')
        
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
        c.drawString(100, y_position, f"Nome: {row['Nome']}")
        y_position -= 30  # Sposta in basso
        c.drawString(100, y_position, f"Cognome: {row['Cognome']}")
        y_position -= 30
        c.drawString(100, y_position, f"Email: {row['Email']}")
        y_position -= 30
        c.drawString(100, y_position, f"Numero Tessera: {row['Numero Tessera']}")

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

        send_email(row['Email'], pdf_filename) 

        # Aggiorna la colonna "Inviato" a "SI"
        df.at[index, 'Inviato'] = 'SI'

    # Salva il DataFrame aggiornato nel file Excel
    df.to_excel(file_path, index=False)
    print(f"Tessere generate e salvate nella cartella '{pdf_output_folder}'.")
else:
    print("Il file Excel non esiste.")