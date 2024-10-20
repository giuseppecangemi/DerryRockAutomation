import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os

def send_email(to_address, pdf_filename):
    from_address = 'derryrockfidelity@gmail.com'  # Sostituisci con il tuo indirizzo email
    password = 'hhofvmvwrhreijba'          # Sostituisci con la tua password email

    # Creazione del messaggio
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = 'Tessera Associativa - Derry Rock Pub'

    # Corpo del messaggio
    body = 'In allegato trovi la tua tessera associativa.'
    msg.attach(MIMEText(body, 'plain'))

    # Aggiunta del PDF come allegato
    attachment = MIMEBase('application', 'octet-stream')
    with open(pdf_filename, 'rb') as attachment_file:
        attachment.set_payload(attachment_file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_filename)}')
    msg.attach(attachment)

    # Invio dell'email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Usa il server SMTP che preferisci
            server.starttls()  # Attiva la crittografia
            server.login(from_address, password)  # Effettua il login
            server.send_message(msg)  # Invia il messaggio
        print(f"Email inviata a {to_address} con successo!")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")
