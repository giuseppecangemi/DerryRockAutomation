import pandas as pd
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Percorso del file Excel
file_path = 'dati.xlsx'

# Percorso per salvare i PDF
pdf_output_folder = 'tessere'
os.makedirs(pdf_output_folder, exist_ok=True)

# Controlla se il file esiste
if os.path.exists(file_path):
    # Leggi il file Excel
    df = pd.read_excel(file_path)

    # Filtra solo i soci approvati
    soci_approvati = df[df['Approvato'] == 'SI']

    # Genera un PDF per ogni socio approvato
    for index, row in soci_approvati.iterrows():
        pdf_filename = os.path.join(pdf_output_folder, f'tessera_{int(row["Numero Tessera"])}.pdf')
        
        # Crea un canvas per il PDF
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Scrivi i dati nel PDF
        c.drawString(100, 750, f"Nome: {row['Nome']}")
        c.drawString(100, 730, f"Cognome: {row['Cognome']}")
        c.drawString(100, 710, f"Email: {row['Email']}")
        c.drawString(100, 690, f"Numero Tessera: {row['Numero Tessera']}")

        # Aggiungi un bordo
        c.setStrokeColor(colors.black)
        c.rect(50, 50, 500, 700, stroke=1, fill=0)

        # Salva il PDF
        c.save()

    print(f"Tessere generate e salvate nella cartella '{pdf_output_folder}'.")
else:
    print("Il file Excel non esiste.")
