from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import datetime
import os

def crea_pdf(numero_tessera, nome, cognome, path_out):
    # Percorso del PDF originale e del nuovo PDF modificato
    original_pdf_path = "/Users/giuseppecangemi/Desktop/Programming/Python/DerryRockAutomation/tessere/originale/pdf_DRA.pdf"  # Sostituisci con il percorso del tuo PDF esistente
    output_pdf_path = path_out

    # Dati esempio
    data_corrente = datetime.datetime.now().strftime("%d/%m/%Y")

    # Controlla se il font esiste
    font_path = "/Users/giuseppecangemi/Desktop/Programming/Python/DerryRockAutomation/tessere/font/KREDIT1.TTF"
    if not os.path.exists(font_path):
        print(f"Font non trovato: {font_path}")
        return

    # Crea un buffer per la sovrapposizione
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Registra e utilizza il font Kredit
    pdfmetrics.registerFont(TTFont('Kredit', font_path))  # Cambia il percorso con quello corretto
    c.setFont("Kredit", 12)  # Usa il font Kredit

    # Posiziona i dati sul PDF
    c.setFillColorRGB(0.9, 0.9, 0.9)  # Imposta il colore del testo su grigio molto chiaro
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
# crea_pdf("12345", "Giuseppe", "Cangemi", "/path/to/output.pdf")  # Specifica il percorso del file PDF di output
