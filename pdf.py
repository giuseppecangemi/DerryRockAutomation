from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import datetime

def crea_pdf(numero_tessera, nome, cognome, path_out):
    # Percorso del PDF originale e del nuovo PDF modificato
    original_pdf_path = "/Users/giuseppecangemi/Desktop/Programming/Python/DerryRockAutomation/tessere/originale/pdf_DRA.pdf"  # Sostituisci con il percorso del tuo PDF esistente
    output_pdf_path = path_out

    # Dati esempio
    data_corrente = datetime.datetime.now().strftime("%d/%m/%Y")

    # Crea un buffer per la sovrapposizione
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Posiziona i dati sul PDF con un font più grande
    c.setFont("Helvetica", 16)  # Aumentato a 16
    c.setFillColor("black")
    c.drawString(400, 720, f"{data_corrente}")  # Data
    c.drawString(455, 700, f"{numero_tessera}")  # Numero Tessera
    c.drawString(360, 670, f"{nome} {cognome}")  # Nome e Cognome

    # Salva il canvas nel buffer
    c.save()

    # Carica il contenuto della sovrapposizione
    packet.seek(0)
    overlay_pdf = PdfReader(packet)

    # Carica il PDF originale
    original_pdf = PdfReader(original_pdf_path)
    output_pdf = PdfWriter()

    # Applica la sovrapposizione a ogni pagina del PDF originale
    for i in range(len(original_pdf.pages)):
        page = original_pdf.pages[i]
        # Aggiungi la sovrapposizione
        page.merge_page(overlay_pdf.pages[0])
        output_pdf.add_page(page)

    # Salva il PDF risultante
    with open(output_pdf_path, "wb") as output_stream:
        output_pdf.write(output_stream)

    print(f"PDF modificato salvato come '{output_pdf_path}'.")

# Esempio di utilizzo della funzione
#crea_pdf("12345", "Giuseppe", "Cangemi")
